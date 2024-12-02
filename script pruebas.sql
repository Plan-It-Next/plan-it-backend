SELECT *
FROM user_group
WHERE group_id = '3864dfc4-c9ca-4929-966e-717e7269e69c'

select * from polls
select * from users
select * from calendar
SELECT
    COUNT(*) AS total_usuarios
FROM user_group ug
JOIN polls vt ON vt.group_id = ug.group_id
WHERE vt.poll_id = (select poll_id from polls where poll_name = 'Concierto');

SELECT
    COUNT(*) AS total_votos
FROM user_polls v
WHERE v.poll_id = (select poll_id from polls where poll_name = 'Concierto') AND vote = true ;

select * from user_polls where poll_id = '32986119-968c-48f1-90b5-ae26b2e46a3d'




SELECT
    available_day,
    COUNT(DISTINCT user_id) AS usuarios_disponibles
FROM calendar
WHERE group_id = (SELECT group_id FROM groups WHERE name = 'Grupo A')
GROUP BY available_day
ORDER BY usuarios_disponibles DESC;


select g.group_id, g.name, sum( ug.user_group_budget) as total_budget
from groups g join user_group ug ON g.group_id = ug.group_id
group by g.group_id


select * from user_group
where user_id = (SELECT user_id FROM users WHERE email = 'juan.perez@example.com')
and group_id = (SELECT group_id FROM groups WHERE name = 'Grupo A')

update user_group
set user_group_budget = 80
where user_id = (SELECT user_id FROM users WHERE email = 'juan.perez@example.com')
and group_id = (SELECT group_id FROM groups WHERE name = 'Grupo A')

select * from polls
delete from polls where poll_id = 'accabe88-fc60-49ec-b319-aafc2bd4d9e7'
INSERT INTO polls (group_id, poll_name) VALUES
((SELECT group_id FROM groups WHERE name = 'Grupo A'), 'PruebaJavi2')
RETURNING poll_id, group_id, poll_name, poll_date;

UPDATE polls
                    SET poll_name = 'pjavi3'
                    WHERE poll_id = 'c15b0456-897b-4161-9c2a-67e268d0af3c'
                    RETURNING poll_id, group_id, poll_name, poll_date

delete from polls where poll_id = '1179b9fb-f7a5-4256-a6dd-e299ae6454ab'