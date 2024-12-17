create table siak.account
(
    user_id bigint    default unique_rowid() not null,
    uname   varchar(50)                      not null,
    pass    varchar(50)                      not null,
    created timestamp default now()          not null,
    constraint user_pk
        primary key (user_id),
    constraint username_pk
        unique (uname),
    constraint user_userid_uindex
        unique (user_id)
);

create table siak.class
(
    class_id bigint default unique_rowid() not null,
    cname    varchar(50)                   not null,
    sks      bigint                        not null,
    constraint cid
        primary key (class_id),
    constraint class_class_id_uindex
        unique (class_id)
);

create table siak.selected_class
(
    sc_id    bigint    default unique_rowid() not null,
    uid      bigint    default unique_rowid() not null,
    cid      bigint    default unique_rowid() not null,
    semester bigint                           not null,
    created  timestamp default now()          not null,
    constraint sc_pk
        primary key (sc_id),
    constraint selected_class_user_userid_fk
        foreign key (uid) references siak.account
            on update cascade on delete cascade,
    constraint selected_class_class_classid_fk
        foreign key (cid) references siak.class
            on update cascade on delete cascade
);

create table siak.schedule
(
    schedule_id bigint default unique_rowid() not null,
    cid         bigint default unique_rowid() not null,
    time_start  time                          not null,
    time_end    time                          not null,
    constraint schedule_pk
        primary key (schedule_id),
    constraint schedule_class_classid_fk
        foreign key (cid) references siak.class
            on update cascade on delete cascade
);

create table siak.grades
(
    grade_id     bigint default unique_rowid() not null,
    cid          bigint                        not null,
    uid          bigint                        not null,
    sc_id        bigint                        not null,
    semester     bigint,
    grade_number bigint,
    grade_letter varchar(2)                    not null,
    constraint grades_pk
        primary key (grade_id),
    constraint grades_user_fk
        foreign key (uid) references siak.account
            on update cascade on delete cascade,
    constraint grades_class_fk
        foreign key (cid) references siak.class
            on update cascade on delete cascade,
    constraint grades_selected_fk
        foreign key (sc_id) references siak.selected_class
            on update cascade on delete cascade
);

comment on column siak.grades.grade_number is '0 to 100';

comment on column siak.grades.grade_letter is 'E to A';

