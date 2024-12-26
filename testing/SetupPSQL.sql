create sequence siak."User_userid_seq"
    as integer;

create sequence siak."SelectedClass_scid_seq"
    as integer;

create sequence siak."Schedule_scheduleid_seq"
    as integer;

create sequence siak."Class_class_id_seq"
    as integer;

create table siak.account
(
    user_id serial,
    uname   varchar(50)                                                   not null,
    pass    varchar(50)                                                   not null,
    created timestamp default now()                                       not null,
    constraint user_id
        primary key (user_id),
    constraint username_pk
        unique (uname)
);
oc
alter sequence siak."User_userid_seq" owned by siak.account.user_id;

create table siak.class
(
    class_id serial,
    class_code    varchar(50) not null,
    cname    varchar(50) not null,
    sks      integer     not null,
    created timestamp default now()                                       not null,
    constraint cid
        primary key (class_code)
);

alter sequence siak."Class_class_id_seq" owned by siak.class.class_id;

create table siak.selected_class
(
    sc_id    serial,
    semester integer                                                              not null,
    user      varchar(50),
    class      varchar(50),
    created  timestamp default now()                                              not null,
    constraint sc_pk
        primary key (sc_id),
    constraint sc_user_fk
        foreign key (user) references siak.account
            on update cascade on delete cascade,
    constraint sc_class_fk
        foreign key (class) references siak.class
            on update cascade on delete cascade
);

alter sequence siak."SelectedClass_scid_seq" owned by siak.selected_class.sc_id;

create table siak.schedule
(
    schedule_id serial,
    cid         varchar(50)                                                             not null,
    time_start  time                                                                not null,
    time_end    time                                                                not null,
    created timestamp default now()                                       not null,
    constraint schedule_pk
        primary key (schedule_id),
    constraint schedule_class_classid_fk
        foreign key (cid) references siak.class
            on update cascade on delete cascade
);

alter sequence siak."Schedule_scheduleid_seq" owned by siak.schedule.schedule_id;

create table siak.grades
(
    grade_id     serial,
    cid          varchar(50)    not null,
    uid          integer    not null,
    sc_id        integer    not null,
    created timestamp default now()                                       not null,
    semester     integer,
    grade_number integer,
    grade_letter varchar(2) not null,
    constraint grades_pk
        primary key (grade_id),
    constraint grades_class_fk
        foreign key (cid) references siak.class,
    constraint grades_user_fk
        foreign key (uid) references siak.account,
    constraint grades_selected_fk
        foreign key (sc_id) references siak.selected_class
);

comment on column siak.grades.grade_number is '0 to 100';

comment on column siak.grades.grade_letter is 'E to A';

