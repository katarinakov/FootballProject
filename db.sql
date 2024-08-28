/*
DROP TABLE team_coach;
DROP TABLE team_player;
DROP TABLE team;
DROP TABLE player;
DROP TABLE coach;
DROP TABLE position;
*/


CREATE TABLE team 
(
    team_id SERIAL NOT NULL,
    team_name VARCHAR(20) NOT NULL,
    stadion_name VARCHAR(100),
    PRIMARY KEY(team_id)
);

CREATE TABLE player
(
    player_id SERIAL NOT NULL,
    player_name VARCHAR(20),
    nationality VARCHAR(30),
    PRIMARY KEY(player_id)
);

CREATE TABLE coach 
(
    coach_id SERIAL NOT NULL,
    coach_name VARCHAR(20),
    PRIMARY KEY(coach_id)
);

CREATE TABLE position
(
    position_id SERIAL NOT NULL,
    position_name VARCHAR(20),
    PRIMARY KEY(position_id)
);

CREATE TABLE team_player
(
    team_id INT NOT NULL,
    player_id INT NOT NULL,
    position_id INT NOT NULL,
    PRIMARY KEY (team_id, player_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES position(position_id) ON DELETE CASCADE
);

CREATE TABLE team_coach
(
    team_id INT NOT NULL,
    coach_id INT NOT NULL,
    PRIMARY KEY (team_id, coach_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (coach_id) REFERENCES coach(coach_id) ON DELETE CASCADE
);


INSERT INTO player (player_name, nationality) VALUES ('Luka', 'Croatian');
INSERT INTO team (team_name, stadion_name) VALUES ('Real Madrid', 'Santiago Bernabéu');
INSERT INTO coach (coach_name) VALUES ('Carlo Ancelloti');
INSERT INTO position (position_name) VALUES ('Midfielder');
INSERT INTO position (position_name) VALUES ('Goalkeeper');
INSERT INTO position (position_name) VALUES ('Right Fullback');
INSERT INTO position (position_name) VALUES ('Left Fullback');
INSERT INTO position (position_name) VALUES ('Center Back');
INSERT INTO position (position_name) VALUES ('Wing');
INSERT INTO position (position_name) VALUES ('Forward');
INSERT INTO position (position_name) VALUES ('Left Wing');
INSERT INTO position (position_name) VALUES ('Right Wing');



INSERT INTO team_coach (team_id, coach_id) VALUES (1, 1)
INSERT INTO team_player (team_id, player_id, position_id) VALUES (1, 1, 1)