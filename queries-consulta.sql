-- Ejemplos de uso
-- Nombre del archivo: 03_example_queries.sql

-- Encontrar rutas más baratas
SELECT * FROM obtener_rutas_mas_baratas(1, 6, 3);

-- Encontrar rutas más cortas
SELECT * FROM obtener_rutas_mas_cortas(1, 6, 3);

-- Consulta personalizada con el algoritmo A*
SELECT
    camino_id as "ID del Camino",
    camino as "Ruta",
    ROUND(costo_total::numeric, 2) as "Costo Total (€)",
    ROUND(distancia_total::numeric, 2) as "Distancia Total (km)",
    ROUND(duracion_total::numeric, 2) as "Duración Total (h)"
FROM encontrar_camino_astar(1, 6, 'precio', 3)
ORDER BY costo_total;