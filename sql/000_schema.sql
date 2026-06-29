DROP TABLE IF EXISTS dim_match;
DROP TABLE IF EXISTS dim_team;
DROP TABLE IF EXISTS dim_player;

CREATE TABLE dim_match (
    match_id BIGINT PRIMARY KEY,
    raw_match_json JSON
);

CREATE TABLE dim_team (
    team_id BIGINT,
    match_id BIGINT,
    team_name VARCHAR,
    side VARCHAR
);

CREATE TABLE dim_player (
    player_id BIGINT,
    match_id BIGINT,
    team_id BIGINT,
    player_name VARCHAR,
    jersey_number VARCHAR,
    position VARCHAR
);