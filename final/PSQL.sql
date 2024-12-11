create sequence siak."User_userid_seq"
    as integer;

alter sequence siak."User_userid_seq" owner to postgres_user;

create sequence siak."Class_classid_seq";

alter sequence siak."Class_classid_seq" owner to postgres_user;

create sequence siak."SelectedClass_scid_seq"
    as integer;

alter sequence siak."SelectedClass_scid_seq" owner to postgres_user;

create sequence siak."Schedule_scheduleid_seq"
    as integer;

alter sequence siak."Schedule_scheduleid_seq" owner to postgres_user;

create table siak.account
(
    user_id integer default nextval('siak."User_userid_seq"'::regclass) not null
        constraint user_pk
            primary key,
    uname   varchar(50)                                                 not null
        constraint username_pk
            unique,
    pass    varchar(50)                                                 not null
);

alter table siak.account
    owner to postgres_user;

alter sequence siak."User_userid_seq" owned by siak.account.user_id;

create table siak.class
(
    class_id integer generated always as identity
        constraint cid
            primary key,
    cname    varchar(50) not null,
    sks      integer     not null
);

alter table siak.class
    owner to postgres_user;

alter sequence siak."Class_classid_seq" owned by siak.class.class_id;

create table siak.selected_class
(
    sc_id    integer not null
        constraint sc_pk
            primary key,
    semester integer not null,
    uid      integer
        constraint selected_class_user_userid_fk
            references siak.account,
    cid      integer
        constraint selected_class_class_classid_fk
            references siak.class
);

alter table siak.selected_class
    owner to postgres_user;

alter sequence siak."SelectedClass_scid_seq" owned by siak.selected_class.sc_id;

create table siak.schedule
(
    schedule_id integer default nextval('siak."Schedule_scheduleid_seq"'::regclass) not null
        constraint schedule_pk
            primary key,
    cid         integer                                                             not null
        constraint schedule_class_classid_fk
            references siak.class,
    time_start  time                                                                not null,
    time_end    time                                                                not null
);

alter table siak.schedule
    owner to postgres_user;

alter sequence siak."Schedule_scheduleid_seq" owned by siak.schedule.schedule_id;


