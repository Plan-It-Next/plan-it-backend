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

/* try:
        # Ejecutar la consulta
        query = """
        SELECT jsonb_build_object(
            'start_node', nodo_inicio::text,
            'end_node', nodo_fin::text,
            'total_distance', total_distancia,
            'total_price', total_precio,
            'path', jsonb_agg(jsonb_strip_nulls(jsonb_build_object('properties', propiedades::text::jsonb)))
        ) AS resultado
        FROM (
            -- Subconsulta aquí...
        ) AS resultado_data
        GROUP BY nodo_inicio, nodo_fin, total_distancia, total_precio;
        """
        result = await conn.fetch(query)

        # Limpiar y formatear el resultado
        cleaned_results = []
        for record in result:
            raw_data = record['resultado']

            # Convertir a cadena de texto
            raw_data_str = str(raw_data)

            # Usar regex para eliminar "::vertex", "::edge", "::path"
            cleaned_data_str = re.sub(r'::(vertex|edge|path)', '', raw_data_str)

            # Convertir a JSON
            cleaned_data = json.loads(cleaned_data_str)
            cleaned_results.append(cleaned_data)

        # Mostrar los resultados limpios
        for res in cleaned_results:
            print(json.dumps(res, indent=4)) */
