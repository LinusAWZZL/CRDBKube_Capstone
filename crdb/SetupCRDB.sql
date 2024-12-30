CREATE TABLE public.curriculum (
	curriculum_id UUID NOT NULL DEFAULT gen_random_uuid(),
	curriculum_year VARCHAR(50) NOT NULL,
	curriculum_name VARCHAR NULL,
	created TIMESTAMP NULL DEFAULT now():::TIMESTAMP,
	CONSTRAINT curriculum_pk PRIMARY KEY (curriculum_year ASC),
	UNIQUE INDEX curriculum_unique (curriculum_id ASC)
);

CREATE TABLE public.lecturer (
	lecturer_id UUID NOT NULL DEFAULT gen_random_uuid(),
	lecturer_code VARCHAR(20) NOT NULL,
	lecturer_name VARCHAR NOT NULL,
	created TIMESTAMP NULL DEFAULT now():::TIMESTAMP,
	CONSTRAINT lecturer_pk PRIMARY KEY (lecturer_code ASC),
	UNIQUE INDEX lecturer_unique (lecturer_id ASC)
);

CREATE TABLE public.student (
	user_id UUID NOT NULL DEFAULT gen_random_uuid(),
	student_code VARCHAR(10) NOT NULL,
	username VARCHAR NULL,
	pass VARCHAR NULL,
	created TIMESTAMP NULL DEFAULT now():::TIMESTAMP,
	CONSTRAINT student_pk PRIMARY KEY (student_code ASC),
	UNIQUE INDEX student_unique (user_id ASC)
);

CREATE TABLE public.course (
	course_id UUID NOT NULL DEFAULT gen_random_uuid(),
	course_code VARCHAR(10) NOT NULL,
	course_name VARCHAR NULL,
	sks INT8 NULL DEFAULT 3:::INT8,
	course_curriculum VARCHAR(50) NOT NULL,
	prerequisite VARCHAR(10) NULL,
	created TIMESTAMP NULL DEFAULT now():::TIMESTAMP,
	CONSTRAINT course_pk PRIMARY KEY (course_code ASC),
	CONSTRAINT course_curriculum_fk FOREIGN KEY (course_curriculum) REFERENCES public.curriculum(curriculum_year) ON DELETE CASCADE,
	CONSTRAINT course_course_fk FOREIGN KEY (prerequisite) REFERENCES public.course(course_code) ON DELETE SET NULL ON UPDATE CASCADE,
	UNIQUE INDEX course_unique (course_id ASC)
);

CREATE TABLE public.course_offering (
	co_id UUID NOT NULL DEFAULT gen_random_uuid(),
	co_name VARCHAR(10) NOT NULL,
	semester INT8 NOT NULL,
	co_course VARCHAR(10) NOT NULL,
	class_lecturer VARCHAR(20) NOT NULL,
	created TIMESTAMP NULL DEFAULT now():::TIMESTAMP,
	CONSTRAINT course_offering_pk PRIMARY KEY (co_name ASC, semester ASC, co_course ASC),
	CONSTRAINT course_offering_lecturer_fk FOREIGN KEY (class_lecturer) REFERENCES public.lecturer(lecturer_code),
	CONSTRAINT course_offering_course_fk FOREIGN KEY (co_course) REFERENCES public.course(course_code) ON DELETE CASCADE ON UPDATE CASCADE,
	UNIQUE INDEX course_offering_unique (co_id ASC)
);

CREATE TABLE public.course_registration (
	cr_id UUID NOT NULL DEFAULT gen_random_uuid(),
	student_code VARCHAR(10) NOT NULL,
	semester INT8 NOT NULL,
	course_code VARCHAR(10) NOT NULL,
	grade_number INT8 NULL,
	grade_letter VARCHAR NULL,
	course_passed BOOL NOT NULL DEFAULT false,
	created TIMESTAMP NULL DEFAULT now():::TIMESTAMP,
	course_name VARCHAR(10) NOT NULL,
	CONSTRAINT course_registration_pk PRIMARY KEY (cr_id ASC),
	CONSTRAINT course_registration_student_fk FOREIGN KEY (student_code) REFERENCES public.student(student_code) ON DELETE CASCADE,
	CONSTRAINT course_registration_course_offering_fk FOREIGN KEY (course_name, semester, course_code) REFERENCES public.course_offering(co_name, semester, co_course) ON DELETE CASCADE ON UPDATE CASCADE,
	UNIQUE INDEX course_registration_unique (student_code ASC, semester ASC, course_code ASC)
);

CREATE TABLE public.schedule (
	schedule_id UUID NOT NULL DEFAULT gen_random_uuid(),
	schedule_class VARCHAR(10) NOT NULL,
	semester INT8 NOT NULL,
	schedule_course VARCHAR(10) NOT NULL,
	time_start TIME NOT NULL,
	time_end TIME NOT NULL,
	created TIMESTAMP NULL DEFAULT now():::TIMESTAMP,
	CONSTRAINT schedule_pk PRIMARY KEY (schedule_id ASC),
	CONSTRAINT schedule_course_offering_fk FOREIGN KEY (schedule_class, semester, schedule_course) REFERENCES public.course_offering(co_name, semester, co_course) ON DELETE CASCADE ON UPDATE CASCADE
);

TRUNCATE course, course_offering, course_registration, curriculum, lecturer, schedule, student cascade;