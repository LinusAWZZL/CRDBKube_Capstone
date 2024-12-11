create table account
(
    user_id bigint default unique_rowid() not null
        constraint user_pk
            primary key
        constraint user_userid_uindex
            unique,
    uname  varchar(50)                   not null,
    pass   varchar(50)                   not null
);

alter table account
    owner to pgadmin;

create table class
(
    class_id bigint default unique_rowid() not null
        constraint cid
            primary key
        constraint class_classid_uindex
            unique,
    cname   varchar(50)                   not null,
    sks     bigint                        not null
);

alter table class
    owner to pgadmin;

create table selected_class
(
    sc_id     bigint default unique_rowid() not null
        constraint sc_pk
            primary key,
    uid      bigint default unique_rowid() not null
        constraint selectedclass_user_userid_fk
            references account,
    cid      bigint default unique_rowid() not null
        constraint selectedclass_class_classid_fk
            references class,
    semester bigint                        not null
);

alter table selectedclass
    owner to pgadmin;

create table schedule
(
    schedule_id bigint default unique_rowid() not null
        constraint schedule_pk
            primary key,
    cid        bigint default unique_rowid() not null
        constraint schedule_class_classid_fk
            references class,
    time_start time                          not null,
    time_end   time                          not null
);

alter table schedule
    owner to pgadmin;
