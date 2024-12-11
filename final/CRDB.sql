create table siak.account
(
    user_id bigint default unique_rowid() not null
        constraint user_pk
            primary key
        constraint user_userid_uindex
            unique,
    uname   varchar(50)                   not null
        constraint username_pk
            unique,
    pass    varchar(50)                   not null
);

alter table siak.account
    owner to pgadmin;

create table siak.class
(
    classid bigint default unique_rowid() not null
        constraint cid
            primary key
        constraint class_classid_uindex
            unique,
    cname   varchar(50)                   not null,
    sks     bigint                        not null
);

alter table siak.class
    owner to pgadmin;

create table siak.selected_class
(
    sc_id    bigint default unique_rowid() not null
        constraint sc_pk
            primary key,
    uid      bigint default unique_rowid() not null
        constraint selected_class_user_userid_fk
            references siak.account,
    cid      bigint default unique_rowid() not null
        constraint selected_class_class_classid_fk
            references siak.class,
    semester bigint                        not null
);

alter table siak.selected_class
    owner to pgadmin;

create table siak.schedule
(
    scheduleid bigint default unique_rowid() not null
        constraint schedule_pk
            primary key,
    cid        bigint default unique_rowid() not null
        constraint schedule_class_classid_fk
            references siak.class,
    time_start time                          not null,
    time_end   time                          not null
);

alter table siak.schedule
    owner to pgadmin;


