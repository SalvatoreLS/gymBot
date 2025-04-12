-- Table for application users.
CREATE TABLE gym_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL  -- passwords should be stored as hashed values.
);

-- Table for exercises.
CREATE TABLE exercise (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    comment TEXT,
    extra_info TEXT,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table for workout programs.
CREATE TABLE program (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES gym_user(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table for days within a workout program.
CREATE TABLE program_day (
    id SERIAL PRIMARY KEY,
    program_id INTEGER NOT NULL,
    day_number INTEGER NOT NULL,  -- e.g., 1 for day one, 2 for day two, etc.
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (program_id) REFERENCES program(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table for recording workouts.
CREATE TABLE workout (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    workout_time TIMESTAMP NOT NULL,
    duration INTEGER NOT NULL,  -- duration in minutes (or another unit)
    FOREIGN KEY (user_id) REFERENCES gym_user(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table for logging individual sets within a workout.
CREATE TABLE workout_set (
    id SERIAL PRIMARY KEY,
    workout_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    sequence_number INTEGER NOT NULL,  -- the order of the set within a workout
    weight INTEGER NOT NULL,  -- weight used (e.g., in kilograms or pounds)
    reps INTEGER NOT NULL,
    rest INTEGER NOT NULL,  -- rest time in seconds (or another unit)
    FOREIGN KEY (workout_id) REFERENCES workout(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercise(id)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- Table for linking exercises to a program day (i.e., the planned routine for that day).
CREATE TABLE program_day_exercise (
    id SERIAL PRIMARY KEY,
    program_day_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    FOREIGN KEY (program_day_id) REFERENCES program_day(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercise(id)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);