CREATE TABLE public.student (
	user_id serial NOT NULL,
	student_code varchar(10) NOT NULL,
	username varchar NULL,
	pass varchar NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT student_unique UNIQUE (user_id),
	CONSTRAINT student_pk PRIMARY KEY (student_code)
);

CREATE TABLE public.curriculum (
	curriculum_id serial NOT NULL,
	curriculum_year varchar(50) NOT NULL,
	curriculum_name varchar NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT curriculum_unique UNIQUE (curriculum_id),
	CONSTRAINT curriculum_pk PRIMARY KEY (curriculum_year)
);

CREATE TABLE public.lecturer (
	lecturer_id serial NOT NULL,
	lecturer_code varchar(20) NOT NULL,
	lecturer_name varchar NOT NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT lecturer_unique UNIQUE (lecturer_id),
	CONSTRAINT lecturer_pk PRIMARY KEY (lecturer_code)
);

CREATE TABLE public.course (
	course_id serial NOT NULL,
	course_code varchar(10) NOT NULL,
	course_name varchar NULL,
	sks int DEFAULT 3 NULL,
	course_curriculum varchar NOT NULL,
	prerequisite varchar NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT course_unique UNIQUE (course_id),
	CONSTRAINT course_pk PRIMARY KEY (course_code),
	CONSTRAINT course_curriculum_fk FOREIGN KEY (course_curriculum) REFERENCES public.curriculum(curriculum_year) ON DELETE CASCADE,
	CONSTRAINT course_course_fk FOREIGN KEY (prerequisite) REFERENCES public.course(course_code) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE public.course_offering (
	co_id serial NOT NULL,
	co_name varchar(10) NOT NULL,
	semester int NOT NULL,
	co_course varchar NOT NULL,
	class_lecturer varchar NOT NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT course_offering_unique UNIQUE (co_id),
	CONSTRAINT course_offering_pk PRIMARY KEY (co_name,semester,co_course),
	CONSTRAINT course_offering_lecturer_fk FOREIGN KEY (class_lecturer) REFERENCES public.lecturer(lecturer_code) ON DELETE SET NULL,
	CONSTRAINT course_offering_course_fk FOREIGN KEY (co_name) REFERENCES public.course(course_code) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE public.schedule (
	schedule_id serial NOT NULL,
	schedule_class varchar NOT NULL,
	semester int NOT NULL,
	schedule_course varchar NOT NULL,
	time_start time NOT NULL,
	time_end time NOT NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT schedule_pk PRIMARY KEY (schedule_id),
	CONSTRAINT schedule_course_offering_fk FOREIGN KEY (schedule_class,semester,schedule_course) REFERENCES public.course_offering(co_name,semester,co_course) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE public.course_registration (
	cr_id serial NOT NULL,
	student_code varchar NOT NULL,
	semester int NOT NULL,
	course_code varchar NOT NULL,
	grade_number int NULL,
	grade_letter varchar NULL,
	course_passed bool DEFAULT FALSE NOT NULL,
	created timestamp DEFAULT now() NULL,
	course_name varchar NOT NULL,
	CONSTRAINT course_registration_pk PRIMARY KEY (cr_id),
	CONSTRAINT course_registration_unique UNIQUE (student_code,semester,course_code),
	CONSTRAINT course_registration_student_fk FOREIGN KEY (student_code) REFERENCES public.student(student_code) ON DELETE CASCADE,
	CONSTRAINT course_registration_course_offering_fk FOREIGN KEY (course_name,semester,course_code) REFERENCES public.course_offering(co_name,semester,co_course) ON DELETE CASCADE ON UPDATE CASCADE
);