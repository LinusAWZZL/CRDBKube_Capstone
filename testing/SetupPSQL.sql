create sequence siak."User_userid_seq"
    as integer;

create sequence siak."Class_classid_seq";

create sequence siak."SelectedClass_scid_seq"
    as integer;

create sequence siak."Schedule_scheduleid_seq"
    as integer;

create sequence siak.class_class_id_seq
    as integer;

create table siak.account
(
    user_id integer   default nextval('siak."User_userid_seq"'::regclass) not null,
    uname   varchar(50)                                                   not null,
    pass    varchar(50)                                                   not null,
    created timestamp default now()                                       not null,
    constraint user_pk
        primary key (user_id),
    constraint username_pk
        unique (uname)
);

alter sequence siak."User_userid_seq" owned by siak.account.user_id;

create table siak.class
(
    class_id integer generated always as identity,
    cname    varchar(50) not null,
    sks      integer     not null,
    constraint cid
        primary key (class_id)
);

alter sequence siak."Class_classid_seq" owned by siak.class.class_id;

create table siak.selected_class
(
    sc_id    integer   default nextval('siak."SelectedClass_scid_seq"'::regclass) not null,
    semester integer                                                              not null,
    uid      integer,
    cid      integer,
    created  timestamp default now()                                              not null,
    constraint sc_pk
        primary key (sc_id),
    constraint selected_class_user_userid_fk
        foreign key (uid) references siak.account
            on update cascade on delete cascade,
    constraint selected_class_class_classid_fk
        foreign key (cid) references siak.class
            on update cascade on delete cascade
);

alter sequence siak."SelectedClass_scid_seq" owned by siak.selected_class.sc_id;

create table siak.schedule
(
    schedule_id integer default nextval('siak."Schedule_scheduleid_seq"'::regclass) not null,
    cid         integer                                                             not null,
    time_start  time                                                                not null,
    time_end    time                                                                not null,
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
    cid          integer    not null,
    uid          integer    not null,
    sc_id        integer    not null,
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

