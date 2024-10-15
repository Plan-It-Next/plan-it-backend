-- Habilitar la extensión AGE
CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

-- Crear un nuevo grafo
SELECT create_graph('el_grefo');

SELECT * FROM cypher('el_grefo', $$
CREATE
  (n1:Estacion {id:1, nombre:'Estacion Central', ciudad:'Madrid', pais:'España', tipo:'tren', latitud:40.4168, longitud:-3.7038}),
  (n2:Estacion {id:2, nombre:'Aeropuerto Internacional', ciudad:'Madrid', pais:'España', tipo:'avion', latitud:40.4983, longitud:-3.5676}),
  (n3:Estacion {id:3, nombre:'Metro Sol', ciudad:'Madrid', pais:'España', tipo:'metro', latitud:40.4169, longitud:-3.7033}),
  (n4:Estacion {id:4, nombre:'Estacion Sants', ciudad:'Barcelona', pais:'España', tipo:'tren', latitud:41.3809, longitud:2.1400}),
  (n5:Estacion {id:5, nombre:'Aeropuerto El Prat', ciudad:'Barcelona', pais:'España', tipo:'avion', latitud:41.2974, longitud:2.0833}),
  (n6:Estacion {id:6, nombre:'Metro Diagonal', ciudad:'Barcelona', pais:'España', tipo:'metro', latitud:41.3922, longitud:2.1650}),
  (n7:Estacion {id:7, nombre:'Estacion Norte', ciudad:'Valencia', pais:'España', tipo:'tren', latitud:39.4667, longitud:-0.3750}),
  (n8:Estacion {id:8, nombre:'Aeropuerto Manises', ciudad:'Valencia', pais:'España', tipo:'avion', latitud:39.4893, longitud:-0.4816}),
  (n9:Estacion {id:9, nombre:'Metro Colon', ciudad:'Valencia', pais:'España', tipo:'metro', latitud:39.4702, longitud:-0.3746}),
  (n10:Estacion {id:10, nombre:'Estacion Sur', ciudad:'Sevilla', pais:'España', tipo:'tren', latitud:37.3886, longitud:-5.9823}),
  (n11:Estacion {id:11, nombre:'Aeropuerto San Pablo', ciudad:'Sevilla', pais:'España', tipo:'avion', latitud:37.4200, longitud:-5.8989}),
  (n12:Estacion {id:12, nombre:'Metro Puerta Jerez', ciudad:'Sevilla', pais:'España', tipo:'metro', latitud:37.3828, longitud:-5.9963})
$$) AS (n agtype);

-- Insertar aristas
SELECT * FROM cypher('el_grefo', $$
MATCH
  (n1:Estacion {id:1}),
  (n2:Estacion {id:2}),
  (n3:Estacion {id:3}),
  (n4:Estacion {id:4}),
  (n5:Estacion {id:5}),
  (n6:Estacion {id:6}),
  (n7:Estacion {id:7}),
  (n8:Estacion {id:8}),
  (n9:Estacion {id:9}),
  (n10:Estacion {id:10}),
  (n11:Estacion {id:11}),
  (n12:Estacion {id:12})
CREATE
(n1)-[:RUTA {id:1, tipo:'tren', fecha_hora_salida:'2023-10-15T08:00:00', fecha_hora_llegada:'2023-10-15T12:00:00', precio_billete:50, distancia:600, duracion:4}]->(n4),
(n1)-[:RUTA {id:2, tipo:'tren', fecha_hora_salida:'2023-10-16T08:00:00', fecha_hora_llegada:'2023-10-16T11:00:00', precio_billete:45, distancia:350, duracion:3}]->(n7),
(n1)-[:RUTA {id:3, tipo:'tren', fecha_hora_salida:'2023-10-17T08:00:00', fecha_hora_llegada:'2023-10-17T12:00:00', precio_billete:60, distancia:550, duracion:4}]->(n10),
(n1)-[:RUTA {id:4, tipo:'tren', fecha_hora_salida:'2023-10-18T08:30:00', fecha_hora_llegada:'2023-10-18T09:00:00', precio_billete:5, distancia:20, duracion:0.5}]->(n2),
(n1)-[:RUTA {id:5, tipo:'metro', fecha_hora_salida:'2023-10-15T08:10:00', fecha_hora_llegada:'2023-10-15T08:20:00', precio_billete:1.5, distancia:2, duracion:0.17}]->(n3),
(n2)-[:RUTA {id:6, tipo:'avion', fecha_hora_salida:'2023-10-15T09:00:00', fecha_hora_llegada:'2023-10-15T10:30:00', precio_billete:80, distancia:500, duracion:1.5}]->(n5),
(n2)-[:RUTA {id:7, tipo:'avion', fecha_hora_salida:'2023-10-16T09:00:00', fecha_hora_llegada:'2023-10-16T09:50:00', precio_billete:60, distancia:300, duracion:0.83}]->(n8),
(n2)-[:RUTA {id:8, tipo:'avion', fecha_hora_salida:'2023-10-17T09:00:00', fecha_hora_llegada:'2023-10-17T10:00:00', precio_billete:70, distancia:400, duracion:1}]->(n11),
(n2)-[:RUTA {id:9, tipo:'avion', fecha_hora_salida:'2023-10-18T10:00:00', fecha_hora_llegada:'2023-10-18T11:00:00', precio_billete:75, distancia:450, duracion:1}]->(n5),
(n3)-[:RUTA {id:10, tipo:'metro', fecha_hora_salida:'2023-10-15T09:00:00', fecha_hora_llegada:'2023-10-15T15:00:00', precio_billete:2, distancia:600, duracion:6}]->(n6),
(n3)-[:RUTA {id:11, tipo:'metro', fecha_hora_salida:'2023-10-16T09:00:00', fecha_hora_llegada:'2023-10-16T12:00:00', precio_billete:2, distancia:350, duracion:3}]->(n9),
(n3)-[:RUTA {id:12, tipo:'metro', fecha_hora_salida:'2023-10-17T09:00:00', fecha_hora_llegada:'2023-10-17T15:00:00', precio_billete:2, distancia:550, duracion:6}]->(n12),
(n3)-[:RUTA {id:13, tipo:'metro', fecha_hora_salida:'2023-10-18T08:30:00', fecha_hora_llegada:'2023-10-18T08:50:00', precio_billete:1.5, distancia:5, duracion:0.33}]->(n1),
(n4)-[:RUTA {id:14, tipo:'tren', fecha_hora_salida:'2023-10-15T14:00:00', fecha_hora_llegada:'2023-10-15T17:00:00', precio_billete:35, distancia:350, duracion:3}]->(n7),
(n4)-[:RUTA {id:15, tipo:'tren', fecha_hora_salida:'2023-10-16T14:00:00', fecha_hora_llegada:'2023-10-16T19:00:00', precio_billete:60, distancia:600, duracion:5}]->(n10),
(n4)-[:RUTA {id:16, tipo:'tren', fecha_hora_salida:'2023-10-17T12:00:00', fecha_hora_llegada:'2023-10-17T12:20:00', precio_billete:5, distancia:15, duracion:0.33}]->(n5),
(n5)-[:RUTA {id:17, tipo:'avion', fecha_hora_salida:'2023-10-15T11:00:00', fecha_hora_llegada:'2023-10-15T11:50:00', precio_billete:50, distancia:300, duracion:0.83}]->(n8),
(n5)-[:RUTA {id:18, tipo:'avion', fecha_hora_salida:'2023-10-16T11:00:00', fecha_hora_llegada:'2023-10-16T12:00:00', precio_billete:65, distancia:500, duracion:1}]->(n11),
(n5)-[:RUTA {id:19, tipo:'avion', fecha_hora_salida:'2023-10-17T12:30:00', fecha_hora_llegada:'2023-10-17T13:30:00', precio_billete:70, distancia:550, duracion:1}]->(n2),
(n6)-[:RUTA {id:20, tipo:'metro', fecha_hora_salida:'2023-10-15T08:30:00', fecha_hora_llegada:'2023-10-15T08:50:00', precio_billete:1.5, distancia:5, duracion:0.33}]->(n4),
(n7)-[:RUTA {id:21, tipo:'tren', fecha_hora_salida:'2023-10-15T16:00:00', fecha_hora_llegada:'2023-10-15T18:00:00', precio_billete:40, distancia:500, duracion:2}]->(n10),
(n7)-[:RUTA {id:22, tipo:'tren', fecha_hora_salida:'2023-10-16T17:00:00', fecha_hora_llegada:'2023-10-16T20:00:00', precio_billete:45, distancia:550, duracion:3}]->(n1),
(n8)-[:RUTA {id:23, tipo:'avion', fecha_hora_salida:'2023-10-15T12:00:00', fecha_hora_llegada:'2023-10-15T12:50:00', precio_billete:55, distancia:350, duracion:0.83}]->(n11),
(n8)-[:RUTA {id:24, tipo:'avion', fecha_hora_salida:'2023-10-16T13:00:00', fecha_hora_llegada:'2023-10-16T13:50:00', precio_billete:60, distancia:400, duracion:0.83}]->(n2),
(n9)-[:RUTA {id:25, tipo:'metro', fecha_hora_salida:'2023-10-15T09:30:00', fecha_hora_llegada:'2023-10-15T10:00:00', precio_billete:1.5, distancia:4, duracion:0.5}]->(n7),
(n10)-[:RUTA {id:26, tipo:'tren', fecha_hora_salida:'2023-10-15T19:00:00', fecha_hora_llegada:'2023-10-15T23:00:00', precio_billete:65, distancia:600, duracion:4}]->(n1),
(n10)-[:RUTA {id:27, tipo:'tren', fecha_hora_salida:'2023-10-16T19:00:00', fecha_hora_llegada:'2023-10-16T22:00:00', precio_billete:50, distancia:450, duracion:3}]->(n4),
(n11)-[:RUTA {id:28, tipo:'avion', fecha_hora_salida:'2023-10-15T14:00:00', fecha_hora_llegada:'2023-10-15T15:00:00', precio_billete:70, distancia:500, duracion:1}]->(n5),
(n11)-[:RUTA {id:29, tipo:'avion', fecha_hora_salida:'2023-10-16T14:00:00', fecha_hora_llegada:'2023-10-16T15:00:00', precio_billete:65, distancia:450, duracion:1}]->(n2),
(n12)-[:RUTA {id:30, tipo:'metro', fecha_hora_salida:'2023-10-15T10:00:00', fecha_hora_llegada:'2023-10-15T10:30:00', precio_billete:1.5, distancia:5, duracion:0.5}]->(n10),
(n4)-[:RUTA {id:31, tipo:'tren', fecha_hora_salida:'2023-10-17T15:00:00', fecha_hora_llegada:'2023-10-17T18:00:00', precio_billete:40, distancia:500, duracion:3}]->(n1),
(n7)-[:RUTA {id:32, tipo:'tren', fecha_hora_salida:'2023-10-17T16:00:00', fecha_hora_llegada:'2023-10-17T19:00:00', precio_billete:45, distancia:550, duracion:3}]->(n4),
(n10)-[:RUTA {id:33, tipo:'tren', fecha_hora_salida:'2023-10-17T20:00:00', fecha_hora_llegada:'2023-10-17T23:00:00', precio_billete:60, distancia:600, duracion:3}]->(n7),
(n5)-[:RUTA {id:34, tipo:'avion', fecha_hora_salida:'2023-10-18T12:00:00', fecha_hora_llegada:'2023-10-18T13:00:00', precio_billete:70, distancia:500, duracion:1}]->(n11),
(n8)-[:RUTA {id:35, tipo:'avion', fecha_hora_salida:'2023-10-18T13:00:00', fecha_hora_llegada:'2023-10-18T13:50:00', precio_billete:60, distancia:400, duracion:0.83}]->(n5),
(n11)-[:RUTA {id:36, tipo:'avion', fecha_hora_salida:'2023-10-18T14:00:00', fecha_hora_llegada:'2023-10-18T15:00:00', precio_billete:75, distancia:550, duracion:1}]->(n8),
(n2)-[:RUTA {id:37, tipo:'avion', fecha_hora_salida:'2023-10-18T15:00:00', fecha_hora_llegada:'2023-10-18T16:00:00', precio_billete:80, distancia:600, duracion:1}]->(n11),
(n4)-[:RUTA {id:38, tipo:'tren', fecha_hora_salida:'2023-10-19T08:00:00', fecha_hora_llegada:'2023-10-19T09:00:00', precio_billete:10, distancia:100, duracion:1}]->(n6),
(n7)-[:RUTA {id:39, tipo:'metro', fecha_hora_salida:'2023-10-19T09:30:00', fecha_hora_llegada:'2023-10-19T10:00:00', precio_billete:1.5, distancia:5, duracion:0.5}]->(n9),
(n10)-[:RUTA {id:40, tipo:'metro', fecha_hora_salida:'2023-10-19T10:30:00', fecha_hora_llegada:'2023-10-19T11:00:00', precio_billete:1.5, distancia:5, duracion:0.5}]->(n12),
(n1)-[:RUTA {id:41, tipo:'tren', fecha_hora_salida:'2023-10-19T11:00:00', fecha_hora_llegada:'2023-10-19T12:00:00', precio_billete:15, distancia:150, duracion:1}]->(n3),
(n2)-[:RUTA {id:42, tipo:'avion', fecha_hora_salida:'2023-10-19T12:00:00', fecha_hora_llegada:'2023-10-19T13:00:00', precio_billete:85, distancia:650, duracion:1}]->(n8),
(n5)-[:RUTA {id:43, tipo:'avion', fecha_hora_salida:'2023-10-19T13:00:00', fecha_hora_llegada:'2023-10-19T14:00:00', precio_billete:90, distancia:700, duracion:1}]->(n2),
(n8)-[:RUTA {id:44, tipo:'avion', fecha_hora_salida:'2023-10-19T14:00:00', fecha_hora_llegada:'2023-10-19T15:00:00', precio_billete:95, distancia:750, duracion:1}]->(n5),
(n11)-[:RUTA {id:45, tipo:'avion', fecha_hora_salida:'2023-10-19T15:00:00', fecha_hora_llegada:'2023-10-19T16:00:00', precio_billete:100, distancia:800, duracion:1}]->(n2),
(n3)-[:RUTA {id:46, tipo:'metro', fecha_hora_salida:'2023-10-19T16:00:00', fecha_hora_llegada:'2023-10-19T16:30:00', precio_billete:1.5, distancia:5, duracion:0.5}]->(n1),
(n6)-[:RUTA {id:47, tipo:'metro', fecha_hora_salida:'2023-10-19T17:00:00', fecha_hora_llegada:'2023-10-19T17:30:00', precio_billete:1.5, distancia:5, duracion:0.5}]->(n4),
(n9)-[:RUTA {id:48, tipo:'metro', fecha_hora_salida:'2023-10-19T18:00:00', fecha_hora_llegada:'2023-10-19T18:30:00', precio_billete:1.5, distancia:5, duracion:0.5}]->(n7)
$$) AS (n agtype);