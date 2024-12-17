INSERT INTO account (Uname, Pass) VALUES ('admin', 'password123'), ('user1', 'pass456');

DO $$
BEGIN
  FOR i IN 1..300 LOOP
    INSERT INTO account (Uname, Pass)
    VALUES (
      'user' || i, -- Generates usernames like user1, user2, ...
      md5(random()::text) -- Generates a random hashed password
    );
  END LOOP;
END $$;

DO $$
BEGIN
  FOR i IN 1..300 LOOP
    INSERT INTO class (cname, sks)
    VALUES (
      'class' || i,
      trunc(random() * (6 - 2 + 1) + 2)::int
    );
  END LOOP;
END $$;

DO $$
BEGIN
  FOR i IN 1..300 LOOP
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
  FOR i IN 1..900 LOOP
    INSERT INTO selected_class (semester, uid, cid)
    VALUES (
            i,
      trunc(random() * 302 + 1)::int,
      trunc(random() * 300 + 1)::int
    );
  END LOOP;
END $$;
