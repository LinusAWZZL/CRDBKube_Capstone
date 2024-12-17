SELECT setval(pg_get_serial_sequence('account', 'user_id'), MAX(user_id)) FROM account;
SELECT setval(pg_get_serial_sequence('class', 'class_id'), MAX(class_id)) FROM class;
SELECT setval(pg_get_serial_sequence('selected_class', 'sc_id'), MAX(sc_id)) FROM selected_class;
SELECT setval(pg_get_serial_sequence('schedule', 'schedule_id'), MAX(schedule_id)) FROM schedule;
SELECT setval(pg_get_serial_sequence('grades', 'grade_id'), MAX(grade_id)) FROM grades;


DO $$
BEGIN
  FOR i IN 301..3300 LOOP
    INSERT INTO account (Uname, Pass)
    VALUES (
      'user' || i, -- Generates usernames like user1, user2, ...
      md5(random()::text) -- Generates a random hashed password
    );
  END LOOP;
END $$;

DO $$
BEGIN
  FOR i IN 301..3300 LOOP
    INSERT INTO class (cname, sks)
    VALUES (
      'class' || i,
      trunc(random() * (6 - 2 + 1) + 2)::int
    );
  END LOOP;
END $$;

DO $$
BEGIN
  FOR i IN 601..3300 LOOP
    FOR j IN 1..2 LOOP
      DECLARE
        start_time time;
        end_time time;
      BEGIN
        -- Generate the start time
        start_time := (time '00:00:00' + random() * interval '23 hours 59 minutes 59 seconds')::time;

        -- Generate the end time (start time + random interval between 50 and 150 minutes)
        end_time := start_time + (random() * (150 - 50) + 50) * interval '1 minute';

        -- Insert the values into the schedule table
        INSERT INTO schedule (cid, time_start, time_end)
        VALUES (
          i,
          start_time,
          end_time
        );
      END;
    END LOOP;
  END LOOP;
END $$;


DO $$
BEGIN
  FOR i IN 301..3300 LOOP
      FOR j in 1..12::int LOOP
        INSERT INTO selected_class (semester, uid, cid)
        VALUES (
                trunc(random() * 12 + 1)::int,
          i,
          TRUNC(RANDOM() * (3300 - 301) + 301) :: INT
        );
      END LOOP;
  END LOOP;
END $$;

DO $$
DECLARE
    sc_class_id   INTEGER;
    sem   INTEGER;
    grade_num  INTEGER;
    g_letter VARCHAR(2);
    scid INTEGER;
    class_sks INTEGER;
BEGIN
    scid = 3601;
    -- Outer loop for 300 users
    FOR i IN 301...3300 LOOP
        -- Inner loop for a random number of classes (1 to 30)
        FOR j IN 1..12 LOOP
--             RAISE NOTICE 'uid % sc_id %', i, scid;

            -- Get class_id and semester from selected_class table
            SELECT cid, semester
            INTO sc_class_id, sem
            FROM selected_class
            WHERE uid = i AND sc_id = scid
            LIMIT 1;

            SELECT sks
            INTO class_sks
            FROM class
            WHERE class_id = sc_class_id
            LIMIT 1;

--             RAISE NOTICE '-- sem % class % sks %', sem, sc_class_id, class_sks;

            -- Generate a random grade number (0 to 100)
            grade_num := FLOOR(RANDOM() * 101);

            -- Determine grade letter based on grade number
            g_letter := CASE
                WHEN grade_num BETWEEN 85 AND 100 THEN 'A'
                WHEN grade_num BETWEEN 80 AND 84 THEN 'A-'
                WHEN grade_num BETWEEN 75 AND 79 THEN 'B+'
                WHEN grade_num BETWEEN 70 AND 74 THEN 'B'
                WHEN grade_num BETWEEN 65 AND 69 THEN 'B-'
                WHEN grade_num BETWEEN 60 AND 64 THEN 'C+'
                WHEN grade_num BETWEEN 55 AND 59 THEN 'C'
                WHEN grade_num BETWEEN 40 AND 54 THEN 'D'
                ELSE 'E'
            END;

            -- Insert generated data into the grades table
            INSERT INTO grades (cid, uid, sc_id, semester, grade_letter, grade_number)
            VALUES (sc_class_id, i, scid, sem, g_letter, grade_num);
        scid = scid +1;

        END LOOP; -- End inner loop
    END LOOP; -- End outer loop
END $$;

-- 300 + 300 + 600 + 3600 + 3600 = 8400