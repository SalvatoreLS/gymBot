# Tables

1. users
2. training_programs
3. training_days
4. exercises
5. training_day_exercises
6. exercise_sets
7. exercise_progressions
8. exercise_logs

# Tables definition

users (id [k], name, email, created_at)

training_programs (id [k], name, description, created_by, created_at)
training_days (id [k], program_id, day_number, name)
exercises (id [k], name, description, category)

training_day_exercises (id [k], training_day_id, exercise_id, order_in_day)
exercise_sets (id [k], training_day_exercise_id, set_number, reps, weight, rest_time)
exercise_progressions (id [k], exercise_id, progression_type, value_change)
exercise_logs (id [k], user_id, exercise_set_id, date, completed_reps, completed_weight, actual_rest_time)

# Foreign keys references

training_programs (created_by) REFERENCES users(id)
training_days (program_id) REFERENCES training_programs(id)
training_day_exercises (training_day_id) REFERENCES training_days(id)
training_day_exercises (exercise_id) REFERENCES exercises(id)
exercise_sets (training_day_exercise_id) REFERENCES training_day_exercises(id)
exercise_progressions (exercise_id) REFERENCES exercises(id)
exercise_logs (user_id) REFERENCES users(id)
exercise_logs (exercise_set_id) REFERENCES exercise_sets(id)

# Possible triggers
1. If set 2 is in DB, also set 1 has to be inside
