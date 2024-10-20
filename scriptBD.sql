CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),        -- ID auto-incremental como clave primaria
    name VARCHAR(100) NOT NULL,   -- Nombre del usuario, no puede ser nulo
    email VARCHAR(255) UNIQUE NOT NULL -- Email único, obligatorio
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
INSERT INTO users (name, email) VALUES
('Juan Pérez', 'juan.perez@example.com'),
('María López', 'maria.lopez@example.com'),
('Carlos García', 'carlos.garcia@example.com'),
('Ana Sánchez', 'ana.sanchez@example.com'),
('Pedro Martínez', 'pedro.martinez@example.com');

-- Insertar datos en la tabla groups
INSERT INTO groups (name, budget) VALUES
('Grupo A', 1000.00),
('Grupo B', 1500.50),
('Grupo C', 2000.00);

-- Insertar datos en la tabla user_group
-- Asegúrate de usar los user_id y group_id correctos
INSERT INTO user_group (user_id, group_id) VALUES
((SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A')),
((SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B')),
((SELECT user_id FROM users WHERE email = 'maria.lopez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B')),
((SELECT user_id FROM users WHERE email = 'carlos.garcia@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A')),
((SELECT user_id FROM users WHERE email = 'ana.sanchez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo C')),
((SELECT user_id FROM users WHERE email = 'pedro.martinez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B'));

