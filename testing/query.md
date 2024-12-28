# Lectures

```
SELECT Course Offering
FROM Course Offering
WHERE lecturer_code = Me
AND semester = now
```

```
SELECT schedule
FROM JOIN schedule + course offering
WHERE lecturer = me
AND semester = now
SORT BY created
```

```
SELECT student
FROM JOIN student + course offering
WHERE lecturer = me
AND semester = now
GROUP BY course offering
```

# Students

```
SELECT Course registration
FROM Course registration
WHERE student_code = Me
SORT BY semester
```

```
SELECT sum(sks) + average(grade)
FROM JOIN Course + Course registration
WHERE student_code = Me
AND course_passed = true
```

```
SELECT Schedule
FROM JOIN Schedule + Course registration
WHERE student_code = Me
AND semester = now
```

# Registration

```
SELECT student
FROM student
WHERE name = me
AND pass = right
```

```
SELECT student
FROM student
WHERE name = me
AND pass = wrong
```

```
SELECT course offering
FROM course offering
WHERE semester = now
```

```
INSERT TO course registration
student = me
semester = now
```

```
SELECT schedule
FROM JOIN schedule + course registration
WHERE semester = now
AND student = me
```

```
UPDATE course registration
student = me
semester = now
``` 
(Add and Drop)

# Grading

```
SELECT student
FROM JOIN course offering + course registration + student
WHERE lecturer = me
AND semester = now
```
(Trigger course passed)

```
UPDATE grades 
IN course registration
grade letter = random
if c or better course passed = true
WHERE class = mine
lecturer = me
```

```
SELECT grades
FROM JOIN course offering + course registration
WHERE lecturer = me
AND semester = now
```

```
UPDATE grades 
IN course registration
grade number = random
WHERE class = mine
lecturer = me
```

```
SELECT average(grades)
FROM JOIN course offering + course registration
WHERE lecturer = me
AND semester = now
GROUP BY course offering
```