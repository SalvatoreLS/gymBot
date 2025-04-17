# Queries

### Get Programs Associated with a Specific User
```SQL
SELECT *
FROM program
WHERE owner_id = [:user_id];
```

### Get Data for Plotting the Progression of Weight for an Exercise
```SQL
SELECT w.workout_time, ws.weight
FROM workout_set ws
JOIN workout w ON ws.workout_id = w.id
WHERE ws.exercise_id = [:exercise_id]
ORDER BY w.workout_time ASC;
```

### Get Progression of Repetitions Over Time for an Exercise
```SQL
SELECT 
    w.workout_time,
    ws.reps
FROM workout_set ws
JOIN workout w ON ws.workout_id = w.id
WHERE ws.exercise_id = :exercise_id
ORDER BY w.workout_time;
```

### Get a Summary of Programs and Their Days for a User
```SQL
SELECT 
    p.id AS program_id,
    p.name AS program_name,
    pd.day_number,
    pd.name AS day_name
FROM program p
JOIN program_day pd ON p.id = pd.program_id
WHERE p.owner_id = :user_id
ORDER BY p.id, pd.day_number;
```

### Get all the exercises in a program
```SQL
SELECT 
    pd.id AS program_day_id,
    pd.day_number,
    pd.name AS day_name,
    e.id AS exercise_id,
    e.name AS exercise_name
FROM program_day pd
JOIN program_day_exercise pde ON pd.id = pde.program_day_id
JOIN exercise e ON pde.exercise_id = e.id
WHERE pd.program_id = :program_id
  AND pd.day_number = :day_number
ORDER BY e.id; --- Order by the id of the exercise in the day program
--- (check the correctness of id usage)
```

### Get all the sets of an exercise
```SQL
SELECT 
    sequence_number AS set_number,
    weight,
    reps,
    rest
FROM workout_set
WHERE exercise_id = :exercise_id
ORDER BY sequence_number;
```

### Calculate Total Volume for a Specific Workout
```SQL
SELECT 
    w.id AS workout_id,
    w.workout_time,
    SUM(ws.weight * ws.reps) AS total_volume
FROM workout w
JOIN workout_set ws ON w.id = ws.workout_id
WHERE w.id = :workout_id
GROUP BY w.id, w.workout_time;
```

### Get Maximum Weight per Exercise for a User
```SQL
SELECT 
    ws.exercise_id,
    MAX(ws.weight) AS max_weight
FROM workout_set ws
JOIN workout w ON ws.workout_id = w.id
WHERE w.user_id = :user_id
GROUP BY ws.exercise_id;
```

### Get Detailed Workout Data for a User's Session
```SQL
SELECT
    w.id AS workout_id,
    w.workout_time,
    w.duration,
    ws.sequence_number,
    e.name AS exercise_name,
    ws.weight,
    ws.reps,
    ws.rest
FROM workout w
JOIN workout_set ws ON w.id = ws.workout_id
JOIN exercise e ON ws.exercise_id = e.id
WHERE w.id = :workout_id
ORDER BY ws.sequence_number;
```

### Get the last workout id
```SQL
SELECT