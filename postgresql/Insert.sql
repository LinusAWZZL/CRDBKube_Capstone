INSERT INTO "User" (Uname, Pass) VALUES ('admin', 'password123'), ('user1', 'pass456');

DO $$
BEGIN
  FOR i IN 1..300 LOOP
    INSERT INTO "User" (Uname, Pass)
    VALUES (
      'user' || i, -- Generates usernames like user1, user2, ...
      md5(random()::text) -- Generates a random hashed password
    );
  END LOOP;
END $$;

DO $$
BEGIN
  FOR i IN 1..300 LOOP
    INSERT INTO "class" (cname, sks)
    VALUES (
      'class' || i,
      trunc(random() * (6 - 2 + 1) + 2)::int
    );
  END LOOP;
END $$;

DO $$
BEGIN
  FOR i IN 1..300 LOOP
    INSERT INTO "schedule" (cid, start, "End")
    VALUES (
      i,
      (time '00:00:00' + random() * interval '23 hours 59 minutes 59 seconds')::time,
        (time '00:00:00' + random() * interval '23 hours 59 minutes 59 seconds')::time
    );
    INSERT INTO "schedule" (cid, start, "End")
    VALUES (
      i,
      (time '00:00:00' + random() * interval '23 hours 59 minutes 59 seconds')::time,
        (time '00:00:00' + random() * interval '23 hours 59 minutes 59 seconds')::time
    );
  END LOOP;
END $$;

DO $$
BEGIN
  FOR i IN 1..900 LOOP
    INSERT INTO "SelectedClass" (semester, uid, cid)
    VALUES (
            i,
      trunc(random() * 302 + 1)::int,
      trunc(random() * 300 + 1)::int
    );
  END LOOP;
END $$;
