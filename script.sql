-- Habilitar la extensión AGE
CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

-- Crear un nuevo grafo
SELECT create_graph('el_grefo');

-- Crear nodos (ciudades/estaciones)
SELECT * FROM cypher('el_grefo', $$
    CREATE (:Estacion {
        id: 1,
        nombre: 'Estación A',
        ciudad: 'Madrid',
        pais: 'España',
        latitud: 40.4168,
        longitud: -3.7038,
        tipo: 'tren'
    }),
    (:Estacion {
        id: 2,
        nombre: 'Aeropuerto B',
        ciudad: 'Barcelona',
        pais: 'España',
        latitud: 41.3851,
        longitud: 2.1734,
        tipo: 'avion'
    }),
    (:Estacion {
        id: 3,
        nombre: 'Estación C',
        ciudad: 'Paris',
        pais: 'Francia',
        latitud: 48.8566,
        longitud: 2.3522,
        tipo: 'tren'
    }),
    (:Estacion {
        id: 4,
        nombre: 'Estación D',
        ciudad: 'Londres',
        pais: 'Reino Unido',
        latitud: 51.5074,
        longitud: -0.1278,
        tipo: 'metro'
    }),
    (:Estacion {
        id: 5,
        nombre: 'Estación E',
        ciudad: 'Berlin',
        pais: 'Alemania',
        latitud: 52.5200,
        longitud: 13.4050,
        tipo: 'tren'
    }),
    (:Estacion {
        id: 6,
        nombre: 'Aeropuerto F',
        ciudad: 'Roma',
        pais: 'Italia',
        latitud: 41.9028,
        longitud: 12.4964,
        tipo: 'avion'
    }),
    (:Estacion {
        id: 7,
        nombre: 'Estación G',
        ciudad: 'Lisboa',
        pais: 'Portugal',
        latitud: 38.7223,
        longitud: -9.1393,
        tipo: 'metro'
    }),
    (:Estacion {
        id: 8,
        nombre: 'Aeropuerto H',
        ciudad: 'Amsterdam',
        pais: 'Países Bajos',
        latitud: 52.3676,
        longitud: 4.9041,
        tipo: 'avion'
    }),
    (:Estacion {
        id: 9,
        nombre: 'Estación I',
        ciudad: 'Bruselas',
        pais: 'Bélgica',
        latitud: 50.8503,
        longitud: 4.3517,
        tipo: 'tren'
    }),
    (:Estacion {
        id: 10,
        nombre: 'Estación J',
        ciudad: 'Zurich',
        pais: 'Suiza',
        latitud: 47.3769,
        longitud: 8.5417,
        tipo: 'tren'
    }),
    (:Estacion {
        id: 11,
        nombre: 'Aeropuerto K',
        ciudad: 'Viena',
        pais: 'Austria',
        latitud: 48.2082,
        longitud: 16.3738,
        tipo: 'avion'
    }),
    (:Estacion {
        id: 12,
        nombre: 'Estación L',
        ciudad: 'Estocolmo',
        pais: 'Suecia',
        latitud: 59.3293,
        longitud: 18.0686,
        tipo: 'metro'
    })
$$) as (a agtype);

-- Crear aristas (conexiones entre estaciones)
SELECT * FROM cypher('el_grefo', $$
    MATCH (a:Estacion {id: 1}), (b:Estacion {id: 2})
    CREATE (a)-[:Conexion {
        id: 1,
        fecha_hora_salida: '2024-10-10 08:00:00',
        fecha_hora_llegada: '2024-10-10 10:00:00',
        precio_billete: 50.00,
        distancia_km: 500,
        duracion_h: 2,
        tipo: 'tren'
    }]->(b),
    (b)-[:Conexion {
        id: 2,
        fecha_hora_salida: '2024-10-10 12:00:00',
        fecha_hora_llegada: '2024-10-10 14:00:00',
        precio_billete: 120.00,
        distancia_km: 1000,
        duracion_h: 2,
        tipo: 'avion'
    }]->(a),
    (a)-[:Conexion {
        id: 3,
        fecha_hora_salida: '2024-10-11 09:00:00',
        fecha_hora_llegada: '2024-10-11 15:00:00',
        precio_billete: 200.00,
        distancia_km: 800,
        duracion_h: 6,
        tipo: 'tren'
    }]->(c),
    (c)-[:Conexion {
        id: 4,
        fecha_hora_salida: '2024-10-12 07:00:00',
        fecha_hora_llegada: '2024-10-12 08:30:00',
        precio_billete: 60.00,
        distancia_km: 400,
        duracion_h: 1.5,
        tipo: 'metro'
    }]->(d),
    (d)-[:Conexion {
        id: 5,
        fecha_hora_salida: '2024-10-13 11:00:00',
        fecha_hora_llegada: '2024-10-13 13:00:00',
        precio_billete: 75.00,
        distancia_km: 500,
        duracion_h: 2,
        tipo: 'avion'
    }]->(e),
    (e)-[:Conexion {
        id: 6,
        fecha_hora_salida: '2024-10-14 06:00:00',
        fecha_hora_llegada: '2024-10-14 09:00:00',
        precio_billete: 150.00,
        distancia_km: 700,
        duracion_h: 3,
        tipo: 'tren'
    }]->(f),
    (f)-[:Conexion {
        id: 7,
        fecha_hora_salida: '2024-10-15 14:00:00',
        fecha_hora_llegada: '2024-10-15 15:30:00',
        precio_billete: 45.00,
        distancia_km: 300,
        duracion_h: 1.5,
        tipo: 'metro'
    }]->(g),
    (g)-[:Conexion {
        id: 8,
        fecha_hora_salida: '2024-10-16 09:00:00',
        fecha_hora_llegada: '2024-10-16 11:00:00',
        precio_billete: 85.00,
        distancia_km: 550,
        duracion_h: 2,
        tipo: 'tren'
    }]->(h),
    (h)-[:Conexion {
        id: 9,
        fecha_hora_salida: '2024-10-17 08:00:00',
        fecha_hora_llegada: '2024-10-17 10:00:00',
        precio_billete: 95.00,
        distancia_km: 600,
        duracion_h: 2,
        tipo: 'avion'
    }]->(i),
    (i)-[:Conexion {
        id: 10,
        fecha_hora_salida: '2024-10-18 12:00:00',
        fecha_hora_llegada: '2024-10-18 14:00:00',
        precio_billete: 70.00,
        distancia_km: 400,
        duracion_h: 2,
        tipo: 'metro'
    }]->(j),
    (j)-[:Conexion {
        id: 11,
        fecha_hora_salida: '2024-10-19 07:00:00',
        fecha_hora_llegada: '2024-10-19 09:00:00',
        precio_billete: 130.00,
        distancia_km: 750,
        duracion_h: 2,
        tipo: 'tren'
    }]->(k),
    (k)-[:Conexion {
        id: 12,
        fecha_hora_salida: '2024-10-20 10:00:00',
        fecha_hora_llegada: '2024-10-20 13:00:00',
        precio_billete: 160.00,
        distancia_km: 900,
        duracion_h: 3,
        tipo: 'avion'
    }]->(l),
    (l)-[:Conexion {
        id: 13,
        fecha_hora_salida: '2024-10-21 08:00:00',
        fecha_hora_llegada: '2024-10-21 10:30:00',
        precio_billete: 100.00,
        distancia_km: 500,
        duracion_h: 2.5,
        tipo: 'metro'
    }]->(a),
    (a)-[:Conexion {
        id: 14,
        fecha_hora_salida: '2024-10-22 07:00:00',
        fecha_hora_llegada: '2024-10-22 09:30:00',
        precio_billete: 120.00,
        distancia_km: 650,
        duracion_h: 2.5,
        tipo: 'tren'
    }]->(b),
    (b)-[:Conexion {
        id: 15,
        fecha_hora_salida: '2024-10-23 10:00:00',
        fecha_hora_llegada: '2024-10-23 13:00:00',
        precio_billete: 150.00,
        distancia_km: 700,
        duracion_h: 3,
        tipo: 'avion'
    }]->(c),
    (c)-[:Conexion {
        id: 16,
        fecha_hora_salida: '2024-10-24 12:00:00',
        fecha_hora_llegada: '2024-10-24 15:00:00',
        precio_billete: 180.00,
        distancia_km: 800,
        duracion_h: 3,
        tipo: 'tren'
    }]->(d),
    (d)-[:Conexion {
        id: 17,
        fecha_hora_salida: '2024-10-25 09:00:00',
        fecha_hora_llegada: '2024-10-25 12:00:00',
        precio_billete: 100.00,
        distancia_km: 600,
        duracion_h: 3,
        tipo: 'avion'
    }]->(e),
    (e)-[:Conexion {
        id: 18,
        fecha_hora_salida: '2024-10-26 08:00:00',
        fecha_hora_llegada: '2024-10-26 10:00:00',
        precio_billete: 85.00,
        distancia_km: 450,
        duracion_h: 2,
        tipo: 'metro'
    }]->(f),
    (f)-[:Conexion {
        id: 19,
        fecha_hora_salida: '2024-10-27 14:00:00',
        fecha_hora_llegada: '2024-10-27 17:00:00',
        precio_billete: 140.00,
        distancia_km: 750,
        duracion_h: 3,
        tipo: 'tren'
    }]->(g),
    (g)-[:Conexion {
        id: 20,
        fecha_hora_salida: '2024-10-28 11:00:00',
        fecha_hora_llegada: '2024-10-28 13:00:00',
        precio_billete: 90.00,
        distancia_km: 500,
        duracion_h: 2,
        tipo: 'avion'
    }]->(h),
    (h)-[:Conexion {
        id: 21,
        fecha_hora_salida: '2024-10-29 16:00:00',
        fecha_hora_llegada: '2024-10-29 19:00:00',
        precio_billete: 160.00,
        distancia_km: 800,
        duracion_h: 3,
        tipo: 'tren'
    }]->(i),
    (i)-[:Conexion {
        id: 22,
        fecha_hora_salida: '2024-10-30 09:00:00',
        fecha_hora_llegada: '2024-10-30 11:30:00',
        precio_billete: 110.00,
        distancia_km: 600,
        duracion_h: 2.5,
        tipo: 'avion'
    }]->(j),
    (j)-[:Conexion {
        id: 23,
        fecha_hora_salida: '2024-10-31 10:00:00',
        fecha_hora_llegada: '2024-10-31 12:00:00',
        precio_billete: 90.00,
        distancia_km: 500,
        duracion_h: 2,
        tipo: 'metro'
    }]->(k),
    (k)-[:Conexion {
        id: 24,
        fecha_hora_salida: '2024-11-01 08:00:00',
        fecha_hora_llegada: '2024-11-01 11:00:00',
        precio_billete: 130.00,
        distancia_km: 700,
        duracion_h: 3,
        tipo: 'tren'
    }]->(l),
    (l)-[:Conexion {
        id: 25,
        fecha_hora_salida: '2024-11-02 09:00:00',
        fecha_hora_llegada: '2024-11-02 11:00:00',
        precio_billete: 95.00,
        distancia_km: 400,
        duracion_h: 2,
        tipo: 'avion'
    }]->(a),
    (a)-[:Conexion {
        id: 26,
        fecha_hora_salida: '2024-11-03 07:00:00',
        fecha_hora_llegada: '2024-11-03 09:30:00',
        precio_billete: 110.00,
        distancia_km: 650,
        duracion_h: 2.5,
        tipo: 'tren'
    }]->(b),
    (b)-[:Conexion {
        id: 27,
        fecha_hora_salida: '2024-11-04 06:00:00',
        fecha_hora_llegada: '2024-11-04 08:00:00',
        precio_billete: 120.00,
        distancia_km: 450,
        duracion_h: 2,
        tipo: 'metro'
    }]->(c),
    (c)-[:Conexion {
        id: 28,
        fecha_hora_salida: '2024-11-05 11:00:00',
        fecha_hora_llegada: '2024-11-05 13:00:00',
        precio_billete: 140.00,
        distancia_km: 550,
        duracion_h: 2,
        tipo: 'avion'
    }]->(d),
    (d)-[:Conexion {
        id: 29,
        fecha_hora_salida: '2024-11-06 07:00:00',
        fecha_hora_llegada: '2024-11-06 09:30:00',
        precio_billete: 130.00,
        distancia_km: 700,
        duracion_h: 2.5,
        tipo: 'tren'
    }]->(e),
    (e)-[:Conexion {
        id: 30,
        fecha_hora_salida: '2024-11-07 15:00:00',
        fecha_hora_llegada: '2024-11-07 17:00:00',
        precio_billete: 100.00,
        distancia_km: 500,
        duracion_h: 2,
        tipo: 'metro'
    }]->(f)
$$) as (a agtype);

-- Verificar nodos y aristas creados
SELECT * FROM cypher('el_grefo', $$
    MATCH (n)
    RETURN n
$$) as (n agtype);

SELECT * FROM cypher('el_grefo', $$
    MATCH ()-[r]->()
    RETURN r
$$) as (r agtype);

