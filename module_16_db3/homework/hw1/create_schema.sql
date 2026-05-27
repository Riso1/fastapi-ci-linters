create table director (
    dir_id integer primary key,
    dir_first_name varchar(50),
    dir_last_name varchar(50)
);

create table movie (
    mov_id integer primary key,
    mov_title varchar(50)
);

create table actors (
    act_id integer primary key,
    act_first_name varchar(50),
    act_last_name varchar(50),
    act_gender varchar(1)
);

CREATE TABLE movie_direction (
    dir_id INTEGER,
    mov_id INTEGER,
    PRIMARY KEY (dir_id, mov_id),
    FOREIGN KEY (dir_id) REFERENCES director(dir_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);

CREATE TABLE oscar_awarded (
    award_id INTEGER PRIMARY KEY,
    mov_id INTEGER,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);

CREATE TABLE movie_cast (
    act_id INTEGER,
    mov_id INTEGER,
    role VARCHAR(50),
    PRIMARY KEY (act_id, mov_id),
    FOREIGN KEY (act_id) REFERENCES actors(act_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);