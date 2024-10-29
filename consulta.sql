--Fer MATCH p = (nodo_inicio:Estacion{id:6})-[rel:RUTA*1..5]->(nodo_fin:Estacion{id:11}) i WHERE nodo_inicio.id = 6 AND nodo_fin.id = 11 és el mateix
--No es pot passar a Json: AGE uses a custom data type called agtype, which is the only data type returned by AGE. Agtype is a superset of Json and a custom implementation of JsonB.
--Ordenar abans no té massa sentit i és poc eficient
--Límit es pot ampliar rutes fins a 6

--Primera consulta que torna les etiquetes
SELECT *
FROM cypher(
    'el_grefo',
    $$
    MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..5]->(nodo_fin:Estacion)
    WHERE nodo_inicio.id = 6 AND nodo_fin.id = 11
    UNWIND rel AS r
    WITH nodo_inicio, nodo_fin, p, SUM(r.distancia) AS total_distancia, SUM(r.precio_billete) AS total_precio
    WHERE total_precio <= 300
    RETURN p
    ORDER BY total_distancia ASC
    LIMIT 3
    $$
) AS (camino agtype);


--Torna un format json però molt reduït
SELECT *
FROM cypher(
    'el_grefo',
    $$
    MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..5]->(nodo_fin:Estacion)
    WHERE nodo_inicio.id = 6 AND nodo_fin.id = 11
    UNWIND rel as r
    WITH p, collect({
        desde: startNode(r).id,
        estacion_desde: startNode(r).nombre,
        hasta: endNode(r).id,
        estacion_hasta: endNode(r).nombre,
        distancia: r.distancia,
        precio: r.precio_billete
    }) as segmentos,
    SUM(r.distancia) as total_distancia,
    SUM(r.precio_billete) as total_precio
    WHERE total_precio <= 300
    RETURN {
        ruta: segmentos,
        distancia_total: total_distancia,
        precio_total: total_precio
    } AS resultado
    ORDER BY total_distancia ASC
    LIMIT 3
    $$
) AS (resultado agtype);



--torna una llista ja més detallada
SELECT *
FROM cypher(
    'el_grefo',
    $$
    MATCH p = (nodo_inicio:Estacion{id:6})-[rel:RUTA*1..5]->(nodo_fin:Estacion{id:11})
    UNWIND rel as r
    WITH p, collect({
        origen: {
            id: id(startNode(r)),
            label: labels(startNode(r))[0],
            id_estacion: startNode(r).id,
            pais: startNode(r).pais,
            tipo: startNode(r).tipo,
            ciudad: startNode(r).ciudad,
            nombre: startNode(r).nombre,
            latitud: startNode(r).latitud,
            longitud: startNode(r).longitud
        },
        ruta: {
            id: id(r),
            label: type(r),
            start_id: id(startNode(r)),
            end_id: id(endNode(r)),
            id_ruta: r.id,
            tipo: r.tipo,
            duracion: r.duracion,
            distancia: r.distancia,
            precio_billete: r.precio_billete,
            fecha_hora_salida: r.fecha_hora_salida,
            fecha_hora_llegada: r.fecha_hora_llegada
        },
        destino: {
            id: id(endNode(r)),
            label: labels(endNode(r))[0],
            id_estacion: endNode(r).id,
            pais: endNode(r).pais,
            tipo: endNode(r).tipo,
            ciudad: endNode(r).ciudad,
            nombre: endNode(r).nombre,
            latitud: endNode(r).latitud,
            longitud: endNode(r).longitud
        }
    }) as segmentos,
    SUM(r.distancia) as total_distancia,
    SUM(r.precio_billete) as total_precio
    WHERE total_precio <= 300
    RETURN {
        ruta: segmentos,
        distancia_total: total_distancia,
        precio_total: total_precio
    } AS resultado
    ORDER BY total_distancia ASC, total_precio ASC
    LIMIT 5
    $$
) AS (resultado agtype);



--torna la més barata i la més curta per separat

WITH ruta_barata AS (
    SELECT * FROM cypher('el_grefo', $$
        MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..5]->(nodo_fin:Estacion)
        WHERE nodo_inicio.id = 6 AND nodo_fin.id = 11
        UNWIND rel AS r
        WITH nodo_inicio, nodo_fin, p,
             SUM(r.distancia) AS total_distancia,
             SUM(r.precio_billete) AS total_precio
        WHERE total_precio <= 300
        RETURN p, total_distancia, total_precio
        ORDER BY total_precio ASC
        LIMIT 1
    $$) AS (camino_barato agtype, distancia_barato float, precio_barato float)
),
-- Luego creamos otra para la ruta más corta
ruta_corta AS (
    SELECT * FROM cypher('el_grefo', $$
        MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..5]->(nodo_fin:Estacion)
        WHERE nodo_inicio.id = 6 AND nodo_fin.id = 11
        UNWIND rel AS r
        WITH nodo_inicio, nodo_fin, p,
             SUM(r.distancia) AS total_distancia,
             SUM(r.precio_billete) AS total_precio
        WHERE total_precio <= 300
        RETURN p, total_distancia, total_precio
        ORDER BY total_distancia ASC
        LIMIT 1
    $$) AS (camino_corto agtype, distancia_corto float, precio_corto float)
)
-- Finalmente unimos los resultados
SELECT
    'Más barato' as tipo,
    camino_barato,
    distancia_barato,
    precio_barato
FROM ruta_barata
UNION ALL
SELECT
    'Más corto' as tipo,
    camino_corto,
    distancia_corto,
    precio_corto
FROM ruta_corta;

