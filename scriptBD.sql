CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),        -- ID auto-incremental como clave primaria
    name VARCHAR(100) NOT NULL,   -- Nombre del usuario, no puede ser nulo
    email VARCHAR(255) UNIQUE NOT NULL, -- Email único, obligatorio
    password VARCHAR(255)
);

CREATE TABLE groups (
    group_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    budget FLOAT
);

CREATE TABLE user_group (
    user_id UUID REFERENCES users (user_id),
    group_id UUID REFERENCES groups (group_id),
    PRIMARY KEY (user_id, group_id)
);

-- Insertar datos en la tabla users
INSERT INTO users (user_id, name, email, password) VALUES
('61139221-5e5e-4673-9f9d-7bcc0e2c1eb2', 'Juan Pérez', 'juan.perez@example.com', '$2b$12$uocUSooIPBRnWzIIsO1QnOiigvjXeWswKFSQMo5owYr9Ugje2Cvb6'), --juanperez123
('f0c4c25f-8c2f-4e94-b375-d9e0a40b5c36', 'María López', 'maria.lopez@example.com', '$2b$12$QIDhCif1AZz8zBkZwFXPfuItTJZBuThv7bMBSpGFDivhn0LPKVWaG'), --marialopezz
('8a3d0cf0-ff29-4485-84d3-bb05e476e430', 'Carlos García', 'carlos.garcia@example.com', '$2b$12$UXEIZH40jBlBo.JOg0jRL.ACLOOsFVs.fymy/ju4xMHL/37qeFIzG'), --carlosGARCIA
('5513721c-1e99-447c-90a1-640bef82b834', 'Ana Sánchez', 'ana.sanchez@example.com', '$2b$12$5JDYXenot1lFr/HFD7tsj.5LZHCXfacjOZiJlCApV4SY8bKg8H9H2'), --anasanchez999
('e0b4c95d-5b2e-405f-bc79-e9e3d6320d20', 'Pedro Martínez', 'pedro.martinez@example.com', '$2b$12$5SJ5h5hszkbU9uNP9NWmU.OE8z5Lz29Zu/ARPVxzriLf4aDxZcj6a'); --pedrito

-- Insertar datos en la tabla groups
INSERT INTO groups (group_id, name, budget) VALUES
('3864dfc4-c9ca-4929-966e-717e7269e69c', 'Grupo A', 1000.00),
('d5a1c93b-bf3f-4d3b-bb3c-3d4018f15b82', 'Grupo B', 1500.50),
('ef1d0c62-f536-4786-87d1-1b9f07abf2a8', 'Grupo C', 2000.00);

-- Insertar datos en la tabla user_group
-- Asegúrate de usar los user_id y group_id correctos
INSERT INTO user_group (user_id, group_id) VALUES
((SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A')),
((SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B')),
((SELECT user_id FROM users WHERE email = 'maria.lopez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B')),
((SELECT user_id FROM users WHERE email = 'carlos.garcia@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A')),
((SELECT user_id FROM users WHERE email = 'ana.sanchez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo C')),
((SELECT user_id FROM users WHERE email = 'pedro.martinez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B'));

