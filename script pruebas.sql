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


select * from user_group where group_id = '3864dfc4-c9ca-4929-966e-717e7269e69c'
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


--21af1921-d03d-4ded-ac94-effe087bcf68 poll
--3864dfc4-c9ca-4929-966e-717e7269e69c group_id
--8a3d0cf0-ff29-4485-84d3-bb05e476e430  user_id

select * from user_polls
INSERT INTO user_polls (poll_id, user_id, group_id, vote)
                    VALUES ('21af1921-d03d-4ded-ac94-effe087bcf68', '8a3d0cf0-ff29-4485-84d3-bb05e476e430', '3864dfc4-c9ca-4929-966e-717e7269e69c', true)
                    RETURNING poll_id, user_id, group_id, vote

insert into user_polls (poll_id, user_id, group_id, vote)
values
('6a0e037b-41d8-45bd-8758-90e7a67c9560', '61139221-5e5e-4673-9f9d-7bcc0e2c1eb2', '3864dfc4-c9ca-4929-966e-717e7269e69c', 'true')


UPDATE user_polls
                    SET vote = true
                    WHERE poll_id = '6a0e037b-41d8-45bd-8758-90e7a67c9560'
                    AND user_id = '61139221-5e5e-4673-9f9d-7bcc0e2c1eb2'
                    AND group_id = '3864dfc4-c9ca-4929-966e-717e7269e69c'
                    RETURNING (poll_id, user_id, group_id, vote)


SELECT
    p.poll_id,
    p.poll_name,
    p.poll_date,
    COUNT(up.user_id) AS total_votes, -- Total de votos (incluye TRUE y FALSE)
    COUNT(CASE WHEN up.vote THEN 1 END) AS true_votes -- Solo los votos TRUE
FROM
    polls p
LEFT JOIN
    user_polls up
ON
    p.poll_id = up.poll_id
WHERE
    p.group_id = '3864dfc4-c9ca-4929-966e-717e7269e69c'
GROUP BY
    p.poll_id, p.poll_name, p.poll_date
ORDER BY
    p.poll_date DESC



SELECT up.poll_id, up.user_id, up.group_id, up.vote, (SELECT COUNT(*) FROM user_group ug WHERE ug.group_id = up.group_id) AS total_users_group
                    FROM user_polls up
                    WHERE poll_id = '6a0e037b-41d8-45bd-8758-90e7a67c9560';

select poll_id, user_id, group_id, vote
from user_polls
where poll_id = '6a0e037b-41d8-45bd-8758-90e7a67c9560'
and user_id = '61139221-5e5e-4673-9f9d-7bcc0e2c1eb2'
and group_id = '3865dfc4-c9ca-4929-966e-717e7269e69c'


SELECT up.poll_id, up.user_id, up.group_id, up.vote, (SELECT COUNT(*) FROM user_group ug WHERE ug.group_id = '3864dfc4-c9ca-4929-966e-717e7269e69c') AS total_users_group
                    FROM user_polls up
                    WHERE poll_id = '21af1921-d03d-4ded-ac94-effe087bcf68';

SELECT up.poll_id, up.user_id, up.group_id, up.vote, (SELECT COUNT(*) FROM user_group ug WHERE ug.group_id = '3864dfc4-c9ca-4929-966e-717e7269e69c') AS total_users_group
                    FROM user_polls up
                    WHERE poll_id = '93c7cffd-f04c-42f2-97f2-d1b98afdca6a'