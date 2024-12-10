create table "User"
(
    UserID integer default nextval('users_uid_seq'::regclass) not null
        constraint users_pkey
            primary key,
    UName  varchar(50) not null,
    Pass   varchar(50) not null
);

alter table "User"
    owner to postgres_user;

create table "Class"
(
    ClassID integer generated always as identity
        constraint cid
            primary key,
    CName   varchar(50),
    sks     integer not null
);

alter table "Class"
    owner to postgres_user;

create table "SelectedClass"
(
    SCID serial not null
        constraint SC_pk
            primary key,
    Semester integer,
    UID      integer
        constraint selectedclass_user_userid_fk
            references "User",
    CID      integer
        constraint selectedclass_class_classid_fk
            references class
);

alter table "SelectedClass"
    owner to postgres_user;

create table "Schedule"
(
    ScheduleID serial not null
        constraint schedule_pk
            primary key,
    CID        integer not null
        constraint schedule_class_classid_fk
            references "Class",
    start      time    not null,
    end      time    not null
);

alter table "Schedule"
    owner to postgres_user;

