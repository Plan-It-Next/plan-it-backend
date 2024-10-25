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
