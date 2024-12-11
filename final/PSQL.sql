create table account
(
    user_id integer default nextval('users_uid_seq'::regclass) not null
        constraint users_pkey
            primary key,
    UName  varchar(50) not null,
    Pass   varchar(50) not null
);

alter table account
    owner to postgres_user;

create table class
(
    class_id integer generated always as identity
        constraint cid
            primary key,
    cname   varchar(50),
    sks     integer not null
);

alter table class
    owner to postgres_user;

create table selected_class
(
    sc_id serial not null
        constraint SC_pk
            primary key,
    semester integer,
    uid      integer
        constraint selectedclass_user_userid_fk
            references account,
    cid      integer
        constraint selectedclass_class_classid_fk
            references class
);

alter table selected_class
    owner to postgres_user;

create table schedule
(
    schedule_id serial not null
        constraint schedule_pk
            primary key,
    cid        integer not null
        constraint schedule_class_classid_fk
            references class,
    time_start time not null,
    time_end time not null
);

alter table schedule
    owner to postgres_user;

