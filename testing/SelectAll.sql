SELECT user_id, username, pass, created
FROM public.account;

SELECT class_id, class_code, class_name, sks, created
FROM public.course;

SELECT sc_id, semester, sc_user, sc_class, created
FROM public.selected_class;

SELECT schedule_id, schedule_class, time_start, time_end, created
FROM public.schedule;

SELECT grade_id, grade_class, grade_user, semester, grade_number, grade_letter, created
FROM public.grades;