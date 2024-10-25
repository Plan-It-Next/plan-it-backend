SELECT *
FROM cypher(
    'el_grefo',
    $$
    MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..3]->(nodo_fin:Estacion) WHERE nodo_inicio.ciudad = 'Valencia' AND nodo_fin.ciudad = 'Madrid'
    UNWIND rel AS r
    WITH nodo_inicio, nodo_fin, p, SUM(r.distancia) AS total_distancia
    WHERE total_distancia <= 500
    RETURN p
    ORDER BY total_distancia ASC
    LIMIT 3
    $$
) AS (camino agtype);
