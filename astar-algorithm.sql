-- Primero asegúrate de que AGE está cargado
CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

-- Función auxiliar para calcular distancia euclidiana
-- Función para calcular la distancia euclidiana entre dos puntos
CREATE OR REPLACE FUNCTION calculate_distance(lat1 float, lon1 float, lat2 float, lon2 float)
RETURNS float AS $$
BEGIN
    RETURN SQRT(POW(lat1 - lat2, 2) + POW(lon1 - lon2, 2)) * 111;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para encontrar el mejor camino
CREATE OR REPLACE FUNCTION find_best_path(
    start_id integer,
    end_id integer,
    max_intermediate integer
) RETURNS TABLE (
    path text,
    total_distance float,
    total_price float,
    num_intermediate integer
) AS $$
DECLARE
    current_max_intermediate integer;
    cypher_query text;
    result_record record;
BEGIN
    -- Primero buscamos rutas directas
    cypher_query := format('
        SELECT * FROM cypher(''el_grefo'', $$
            MATCH (start:Estacion {id: %s})-[r:RUTA]->(end:Estacion {id: %s})
            RETURN r
            ORDER BY r.distancia, r.precio_billete
            LIMIT 1
        $$) as (r agtype);
    ', start_id, end_id);

    FOR result_record IN EXECUTE cypher_query
    LOOP
        RETURN QUERY
        SELECT
            result_record.r#>>'{properties,id}' as path,
            (result_record.r#>>'{properties,distancia}')::float as total_distance,
            (result_record.r#>>'{properties,precio_billete}')::float as total_price,
            0 as num_intermediate;
        RETURN;
    END LOOP;

    -- Si no encontramos ruta directa, buscamos rutas con nodos intermedios
    current_max_intermediate := 1;
    WHILE current_max_intermediate <= max_intermediate LOOP
        cypher_query := format('
            SELECT * FROM cypher(''el_grefo'', $$
                MATCH path = (start:Estacion {id: %s})-[r:RUTA*1..%s]->(end:Estacion {id: %s})
                WHERE ALL(x IN nodes(path)[1..-1] WHERE x.id <> %s)
                AND ALL(x IN nodes(path)[1..-1] WHERE x.id <> %s)
                WITH path,
                     reduce(distance = 0, r IN relationships(path) | distance + r.distancia) as total_distance,
                     reduce(price = 0, r IN relationships(path) | price + r.precio_billete) as total_price,
                     [r IN relationships(path) | r.id] as route_ids
                ORDER BY total_distance, total_price
                LIMIT 1
                RETURN route_ids, total_distance, total_price
            $$) as (route_ids agtype, total_distance float, total_price float);
        ', start_id, current_max_intermediate, end_id, end_id, start_id);

        FOR result_record IN EXECUTE cypher_query
        LOOP
            IF result_record.route_ids IS NOT NULL THEN
                RETURN QUERY
                SELECT
                    array_to_string(array_agg(jsonb_array_elements_text(
                        result_record.route_ids::jsonb
                    )), '->'),
                    result_record.total_distance,
                    result_record.total_price,
                    current_max_intermediate;
                RETURN;
            END IF;
        END LOOP;

        current_max_intermediate := current_max_intermediate + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener detalles del camino
CREATE OR REPLACE FUNCTION get_path_details(route_id text)
RETURNS TABLE (
    origen text,
    destino text,
    tipo_transporte text,
    fecha_hora_salida timestamp,
    fecha_hora_llegada timestamp,
    precio float,
    distancia float,
    duracion float
) AS $$
DECLARE
    cypher_query text;
BEGIN
    cypher_query := format('
        SELECT * FROM cypher(''el_grefo'', $$
            MATCH (start:Estacion)-[r:RUTA]->(end:Estacion)
            WHERE r.id = %s
            RETURN start, end, r
        $$) as (start agtype, end agtype, r agtype);
    ', route_id);

    RETURN QUERY
    SELECT
        start#>>'{properties,nombre}' as origen,
        end#>>'{properties,nombre}' as destino,
        r#>>'{properties,tipo}' as tipo_transporte,
        (r#>>'{properties,fecha_hora_salida}')::timestamp as fecha_hora_salida,
        (r#>>'{properties,fecha_hora_llegada}')::timestamp as fecha_hora_llegada,
        (r#>>'{properties,precio_billete}')::float as precio,
        (r#>>'{properties,distancia}')::float as distancia,
        (r#>>'{properties,duracion}')::float as duracion
    FROM EXECUTE cypher_query;
END;
$$ LANGUAGE plpgsql;

-- Ejemplo de uso:
/*
-- Encontrar el mejor camino
SELECT * FROM find_best_path(1, 4, 3);

-- Obtener detalles completos del camino
WITH mejor_ruta AS (
    SELECT * FROM find_best_path(1, 4, 3)
)
SELECT d.*
FROM mejor_ruta r,
LATERAL unnest(string_to_array(r.path, '->')) WITH ORDINALITY AS t(id, ord),
LATERAL get_path_details(id) d
ORDER BY ord;
*/





