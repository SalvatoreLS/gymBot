PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE training_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE training_days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id INTEGER NOT NULL,
    day_number INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (program_id) REFERENCES training_programs(id) ON DELETE CASCADE
);

CREATE TABLE exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT
);

CREATE TABLE training_day_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    training_day_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    order_in_day INTEGER NOT NULL,
    FOREIGN KEY (training_day_id) REFERENCES training_days(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);

CREATE TABLE exercise_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    training_day_exercise_id INTEGER NOT NULL,
    set_number INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight REAL,
    rest_time INTEGER NOT NULL, -- Time in seconds
    FOREIGN KEY (training_day_exercise_id) REFERENCES training_day_exercises(id) ON DELETE CASCADE
);

CREATE TABLE exercise_progressions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_id INTEGER NOT NULL,
    progression_type TEXT CHECK (progression_type IN ('weight', 'reps', 'rest_time')) NOT NULL,
    value_change REAL NOT NULL,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);

CREATE TABLE exercise_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise_set_id INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_reps INTEGER NOT NULL,
    completed_weight REAL,
    actual_rest_time INTEGER NOT NULL, -- Time in seconds
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_set_id) REFERENCES exercise_sets(id) ON DELETE CASCADE
);


