CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),        -- ID auto-incremental como clave primaria
    name VARCHAR(100) NOT NULL,   -- Nombre del usuario, no puede ser nulo
    email VARCHAR(255) UNIQUE NOT NULL, -- Email único, obligatorio
    password VARCHAR(255)
);

CREATE TABLE groups (
    group_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE user_group (
    user_id UUID REFERENCES users (user_id),
    group_id UUID REFERENCES groups (group_id),
    user_group_budget FLOAT,
    PRIMARY KEY (user_id, group_id)
);

CREATE TABLE polls (
    poll_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES groups (group_id),
    poll_name VARCHAR(255) NOT NULL,
    poll_date TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (group_id) REFERENCES groups (group_id) ON DELETE CASCADE,
    CONSTRAINT unique_poll_name_group UNIQUE (group_id, poll_name)
);

CREATE TABLE user_polls (
    poll_id UUID NOT NULL,
    user_id UUID NOT NULL,
    group_id UUID NOT NULL,
    vote BOOLEAN NOT NULL,
    PRIMARY KEY (poll_id, user_id),
    FOREIGN KEY (poll_id) REFERENCES polls (poll_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id, group_id) REFERENCES user_group (user_id, group_id) ON DELETE CASCADE
);

CREATE TABLE calendar (
    user_id UUID NOT NULL,
    group_id UUID NOT NULL,
    available_day DATE NOT NULL,
    PRIMARY KEY (user_id, group_id, available_day),
    FOREIGN KEY (user_id, group_id) REFERENCES user_group (user_id, group_id) ON DELETE CASCADE
);

-- Insertar datos en la tabla users
INSERT INTO users (user_id, name, email, password) VALUES
('61139221-5e5e-4673-9f9d-7bcc0e2c1eb2', 'Juan Pérez', 'juan.perez@example.com', '$2b$12$uocUSooIPBRnWzIIsO1QnOiigvjXeWswKFSQMo5owYr9Ugje2Cvb6'), --juanperez123
('f0c4c25f-8c2f-4e94-b375-d9e0a40b5c36', 'María López', 'maria.lopez@example.com', '$2b$12$QIDhCif1AZz8zBkZwFXPfuItTJZBuThv7bMBSpGFDivhn0LPKVWaG'), --marialopezz
('8a3d0cf0-ff29-4485-84d3-bb05e476e430', 'Carlos García', 'carlos.garcia@example.com', '$2b$12$UXEIZH40jBlBo.JOg0jRL.ACLOOsFVs.fymy/ju4xMHL/37qeFIzG'), --carlosGARCIA
('5513721c-1e99-447c-90a1-640bef82b834', 'Ana Sánchez', 'ana.sanchez@example.com', '$2b$12$5JDYXenot1lFr/HFD7tsj.5LZHCXfacjOZiJlCApV4SY8bKg8H9H2'), --anasanchez999
('e0b4c95d-5b2e-405f-bc79-e9e3d6320d20', 'Pedro Martínez', 'pedro.martinez@example.com', '$2b$12$5SJ5h5hszkbU9uNP9NWmU.OE8z5Lz29Zu/ARPVxzriLf4aDxZcj6a'); --pedrito

-- Insertar datos en la tabla groups
INSERT INTO groups (group_id, name) VALUES
('3864dfc4-c9ca-4929-966e-717e7269e69c', 'Grupo A'),
('d5a1c93b-bf3f-4d3b-bb3c-3d4018f15b82', 'Grupo B'),
('ef1d0c62-f536-4786-87d1-1b9f07abf2a8', 'Grupo C');

-- Insertar datos en la tabla user_group
-- Asegúrate de usar los user_id y group_id correctos
INSERT INTO user_group (user_id, group_id, user_group_budget) VALUES
((SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), 50),
((SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B'), 60),
((SELECT user_id FROM users WHERE email = 'maria.lopez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B'), 566),
((SELECT user_id FROM users WHERE email = 'carlos.garcia@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), 890),
((SELECT user_id FROM users WHERE email = 'ana.sanchez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo C'), 20),
((SELECT user_id FROM users WHERE email = 'pedro.martinez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo B'), 340);


INSERT INTO polls (group_id, poll_name) VALUES
((SELECT group_id FROM groups WHERE name = 'Grupo A'), 'Concierto'),
((SELECT group_id FROM groups WHERE name = 'Grupo A'), 'Comida'),
((SELECT group_id FROM groups WHERE name = 'Grupo A'), 'Safari');

INSERT INTO user_polls(poll_id, user_id, group_id, vote) values
((SELECT poll_id FROM polls WHERE poll_name = 'Concierto'), (SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), true),
((SELECT poll_id FROM polls WHERE poll_name = 'Comida'), (SELECT user_id FROM users WHERE email = 'carlos.garcia@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), true),
((SELECT poll_id FROM polls WHERE poll_name = 'Concierto'), (SELECT user_id FROM users WHERE email = 'carlos.garcia@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), false);

INSERT INTO calendar (user_id, group_id, available_day)
VALUES
((SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), '2024-12-01'),
((SELECT user_id FROM users WHERE email = 'juan.perez@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), '2024-12-02'),
((SELECT user_id FROM users WHERE email = 'carlos.garcia@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), '2024-12-02'),
((SELECT user_id FROM users WHERE email = 'carlos.garcia@example.com'), (SELECT group_id FROM groups WHERE name = 'Grupo A'), '2024-12-03');

