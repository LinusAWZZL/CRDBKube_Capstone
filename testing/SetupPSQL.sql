CREATE TABLE public.account (
	user_id serial NOT NULL,
	username varchar(50) NOT NULL,
	pass varchar NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT account_unique UNIQUE (user_id),
	CONSTRAINT account_pk PRIMARY KEY (username)
);


CREATE TABLE public.course (
	class_id serial NOT NULL,
	class_code varchar(50) NOT NULL,
	class_name varchar NOT NULL,
	sks int DEFAULT 3 NOT NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT class_unique UNIQUE (class_id),
	CONSTRAINT class_pk PRIMARY KEY (class_code)
);

CREATE TABLE public.selected_class (
	sc_id serial NOT NULL,
	semester int NOT NULL,
	sc_user varchar NOT NULL,
	sc_class varchar NOT NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT selected_class_unique UNIQUE (sc_id),
	CONSTRAINT selected_class_pk PRIMARY KEY (semester,sc_user,sc_class),
	CONSTRAINT sc_user FOREIGN KEY (sc_user) REFERENCES public.account(username) ON DELETE CASCADE,
	CONSTRAINT sc_class FOREIGN KEY (sc_class) REFERENCES public.course(class_code) ON DELETE CASCADE
);

CREATE TABLE public.schedule (
	schedule_id serial NOT NULL,
	schedule_class varchar NOT NULL,
	time_start time NOT NULL,
	time_end time NOT NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT schedule_unique UNIQUE (schedule_id),
	CONSTRAINT schedule_pk PRIMARY KEY (schedule_class,schedule_id),
	CONSTRAINT schedule_course_fk FOREIGN KEY (schedule_class) REFERENCES public.course(class_code) ON DELETE CASCADE
);

CREATE TABLE public.grades (
	grade_id serial NOT NULL,
	grade_class varchar NOT NULL,
	grade_user varchar NOT NULL,
	semester int NOT NULL,
	grade_number int NULL,
	grade_letter varchar(2) NOT NULL,
	created timestamp DEFAULT now() NULL,
	CONSTRAINT grades_unique UNIQUE (grade_id),
	CONSTRAINT grades_pk PRIMARY KEY (grade_class,grade_user,semester),
	CONSTRAINT grades_user FOREIGN KEY (grade_user) REFERENCES public.account(username) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT grades_selected_class_fk FOREIGN KEY (semester,grade_class) REFERENCES public.selected_class(semester,sc_class) ON DELETE CASCADE ON UPDATE CASCADE
);

