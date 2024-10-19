-- Primero asegúrate de que AGE está cargado
CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

-- Función auxiliar para calcular distancia euclidiana
CREATE OR REPLACE FUNCTION calcular_distancia_euclidiana(
    lat1 float,
    lon1 float,
    lat2 float,
    lon2 float
) RETURNS float AS $$
BEGIN
    RETURN sqrt(power(lat2 - lat1, 2) + power(lon2 - lon1, 2)) * 111.32;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener coordenadas
CREATE OR REPLACE FUNCTION obtener_coordenadas(
    id_estacion INTEGER,
    OUT lat float,
    OUT lon float
) AS $$
DECLARE
    query_text text;
    cypher_query text;
    result record;
BEGIN
    cypher_query := format('MATCH (n:Estacion) WHERE n.id = %s RETURN n.latitud as lat, n.longitud as lon', id_estacion);
    query_text := format('SELECT * FROM cypher(''el_grefo'', $q$%s$q$) as (lat agtype, lon agtype)', cypher_query);

    EXECUTE query_text INTO result;

    -- Convertir directamente los valores de agtype a float
    SELECT
        (result.lat)::float,
        (result.lon)::float
    INTO lat, lon;
END;
$$ LANGUAGE plpgsql;

-- Función principal del algoritmo A*
CREATE OR REPLACE FUNCTION encontrar_camino_astar(
    origen_id INTEGER,
    destino_id INTEGER,
    criterio TEXT DEFAULT 'precio',
    max_alternativas INTEGER DEFAULT 3
) RETURNS TABLE (
    camino_id INTEGER,
    camino TEXT,
    costo_total FLOAT,
    distancia_total FLOAT,
    duracion_total FLOAT,
    score_precio FLOAT,
    score_distancia FLOAT,
    detalles JSONB
) AS $$
DECLARE
    nodo_actual INTEGER;
    mejor_camino TEXT;
    lista_abierta INTEGER[];
    lista_cerrada INTEGER[];
    g_score FLOAT[];
    f_score FLOAT[];
    caminos TEXT[];
    costos FLOAT[];
    distancias FLOAT[];
    duraciones FLOAT[];
    detalles_rutas JSONB[];
    idx INTEGER;
    siguiente_nodo INTEGER;
    temp_g FLOAT;
    heuristica FLOAT;
    temp_f FLOAT;
    lat1 FLOAT;
    lon1 FLOAT;
    lat2 FLOAT;
    lon2 FLOAT;
    query_text text;
    cypher_query text;
    result record;
    ruta_actual RECORD;
BEGIN
    -- Inicializar arrays
    lista_abierta := ARRAY[origen_id];
    lista_cerrada := ARRAY[]::INTEGER[];
    g_score := ARRAY[0.0];

    -- Obtener coordenadas del destino
    SELECT * INTO lat2, lon2 FROM obtener_coordenadas(destino_id);

    -- Obtener coordenadas del origen
    SELECT * INTO lat1, lon1 FROM obtener_coordenadas(origen_id);

    heuristica := calcular_distancia_euclidiana(lat1, lon1, lat2, lon2);
    f_score := ARRAY[heuristica];
    caminos := ARRAY[origen_id::TEXT];
    costos := ARRAY[0.0];
    distancias := ARRAY[0.0];
    duraciones := ARRAY[0.0];
    detalles_rutas := ARRAY['{}'::JSONB];

    -- Bucle principal del algoritmo A*
    WHILE array_length(lista_abierta, 1) > 0 LOOP
        -- Encontrar el nodo con menor f_score
        nodo_actual := lista_abierta[1];
        idx := 1;
        FOR i IN 1..array_length(lista_abierta, 1) LOOP
            IF f_score[i] < f_score[idx] THEN
                idx := i;
                nodo_actual := lista_abierta[i];
            END IF;
        END LOOP;

        -- Si llegamos al destino
        IF nodo_actual = destino_id THEN
            camino_id := array_length(caminos, 1);
            camino := caminos[idx];
            costo_total := costos[idx];
            distancia_total := distancias[idx];
            duracion_total := duraciones[idx];
            score_precio := costos[idx];
            score_distancia := distancias[idx];
            detalles := detalles_rutas[idx];
            RETURN NEXT;

            -- Eliminar este camino
            lista_abierta := array_remove(lista_abierta, nodo_actual);
            g_score := array_remove(g_score, g_score[idx]);
            f_score := array_remove(f_score, f_score[idx]);
            caminos := array_remove(caminos, caminos[idx]);
            costos := array_remove(costos, costos[idx]);
            distancias := array_remove(distancias, distancias[idx]);
            duraciones := array_remove(duraciones, duraciones[idx]);
            detalles_rutas := array_remove(detalles_rutas, detalles_rutas[idx]);

            IF camino_id >= max_alternativas THEN
                RETURN;
            END IF;
            CONTINUE;
        END IF;

        -- Mover el nodo actual
        lista_abierta := array_remove(lista_abierta, nodo_actual);
        lista_cerrada := array_append(lista_cerrada, nodo_actual);

        -- Explorar vecinos
        cypher_query := format('
            MATCH (n1:Estacion)-[r:RUTA]-(n2:Estacion)
            WHERE n1.id = %s
            RETURN n1.id as n1_id,
                   n2.id as n2_id,
                   r.precio_billete as precio,
                   r.distancia as distancia,
                   r.duracion as duracion,
                   r.tipo as tipo,
                   r.fecha_hora_salida as salida,
                   r.fecha_hora_llegada as llegada',
            nodo_actual);

        query_text := format('
            SELECT * FROM cypher(''el_grefo'', $q$%s$q$) as (
                n1_id agtype,
                n2_id agtype,
                precio agtype,
                distancia agtype,
                duracion agtype,
                tipo agtype,
                salida agtype,
                llegada agtype)',
            cypher_query);

        FOR result IN EXECUTE query_text LOOP
            SELECT
                CASE
                    WHEN (result.n1_id)::integer = nodo_actual
                    THEN (result.n2_id)::integer
                    ELSE (result.n1_id)::integer
                END AS siguiente_id,
                (result.precio)::float AS costo,
                (result.distancia)::float AS dist,
                (result.duracion)::float AS dur,
                (result.tipo)::text AS tipo,
                (result.salida)::text AS fecha_hora_salida,
                (result.llegada)::text AS fecha_hora_llegada
            INTO ruta_actual;

            siguiente_nodo := ruta_actual.siguiente_id;

            IF siguiente_nodo = ANY(lista_cerrada) THEN
                CONTINUE;
            END IF;

            IF criterio = 'precio' THEN
                temp_g := g_score[idx] + ruta_actual.costo;
            ELSE
                temp_g := g_score[idx] + ruta_actual.dist;
            END IF;

            -- Obtener coordenadas del siguiente nodo
            SELECT * INTO lat1, lon1 FROM obtener_coordenadas(siguiente_nodo);

            heuristica := calcular_distancia_euclidiana(lat1, lon1, lat2, lon2);
            temp_f := temp_g + heuristica;

            IF NOT (siguiente_nodo = ANY(lista_abierta)) THEN
                lista_abierta := array_append(lista_abierta, siguiente_nodo);
                g_score := array_append(g_score, temp_g);
                f_score := array_append(f_score, temp_f);
                caminos := array_append(caminos, caminos[idx] || ',' || siguiente_nodo::TEXT);
                costos := array_append(costos, costos[idx] + ruta_actual.costo);
                distancias := array_append(distancias, distancias[idx] + ruta_actual.dist);
                duraciones := array_append(duraciones, duraciones[idx] + ruta_actual.dur);
                detalles_rutas := array_append(
                    detalles_rutas,
                    detalles_rutas[idx] || jsonb_build_object(
                        siguiente_nodo::TEXT,
                        jsonb_build_object(
                            'tipo', ruta_actual.tipo,
                            'fecha_hora_salida', ruta_actual.fecha_hora_salida,
                            'fecha_hora_llegada', ruta_actual.fecha_hora_llegada
                        )
                    )
                );
            END IF;
        END LOOP;
    END LOOP;

    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Funciones de utilidad para consultas comunes
CREATE OR REPLACE FUNCTION obtener_rutas_mas_baratas(
    origen_id INTEGER,
    destino_id INTEGER,
    num_alternativas INTEGER DEFAULT 3
) RETURNS TABLE (
    camino_id INTEGER,
    ruta TEXT,
    costo FLOAT,
    distancia FLOAT,
    duracion FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        r.camino_id,
        r.camino,
        r.costo_total,
        r.distancia_total,
        r.duracion_total
    FROM encontrar_camino_astar(origen_id, destino_id, 'precio', num_alternativas) r
    ORDER BY r.costo_total;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION obtener_rutas_mas_cortas(
    origen_id INTEGER,
    destino_id INTEGER,
    num_alternativas INTEGER DEFAULT 3
) RETURNS TABLE (
    camino_id INTEGER,
    ruta TEXT,
    costo FLOAT,
    distancia FLOAT,
    duracion FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        r.camino_id,
        r.camino,
        r.costo_total,
        r.distancia_total,
        r.duracion_total
    FROM encontrar_camino_astar(origen_id, destino_id, 'distancia', num_alternativas) r
    ORDER BY r.distancia_total;
END;
$$ LANGUAGE plpgsql;