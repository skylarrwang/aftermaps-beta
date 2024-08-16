create table Road_Seg
(
    Road_ID         int auto_increment
        primary key,
    Street          varchar(50)     null,
    State           varchar(50)     null,
    County          varchar(50)     null,
    City            varchar(50)     null,
    Zipcode         varchar(10)     null,
    Avg_Passability float default 0 null,
    Ground_Truth    int   default 0 null
);

create table users
(
    ID                    int auto_increment
        primary key,
    Username              varchar(50)                         null,
    Password              varchar(200)                        null,
    Account_Creation_Time timestamp default CURRENT_TIMESTAMP null,
    ReportQuantity        int       default 0                 null,
    Credibility           float     default 0.5               null
);

create table Pass_Log
(
    PassLog_ID    int auto_increment
        primary key,
    Segment_ID    int                                 null,
    Previous_Pass float                               null,
    Curr_Pass     float                               null,
    Change_Time   timestamp default CURRENT_TIMESTAMP null,
    Last_User     int                                 null,
    constraint Pass_Log_users_ID_fk
        foreign key (Last_User) references users (ID),
    constraint pass_log_ibfk_1
        foreign key (Segment_ID) references Road_Seg (Road_ID)
);

create index Segment_ID
    on Pass_Log (Segment_ID);

create table Reports
(
    Report_ID              int auto_increment
        primary key,
    User_ID                int                                 null,
    Report_Cred            float     default 0.5               null,
    Report_Origin_Location point                               null,
    Subject_Location       point                               null,
    Origin_Subj_Distance   float                               null,
    Subject_Type           varchar(50)                         null,
    Passability            int                                 null,
    Submit_Time            timestamp default CURRENT_TIMESTAMP null,
    Seg_ID                 int                                 null,
    constraint Reports_Road_Seg_Road_ID_fk
        foreign key (Seg_ID) references Road_Seg (Road_ID),
    constraint reports_ibfk_1
        foreign key (User_ID) references users (ID)
);

create index User_ID
    on Reports (User_ID);

create table User_Cred_Log
(
    UserLog_ID  int auto_increment
        primary key,
    User_ID     int                                 null,
    Old_Cred    float                               null,
    New_Cred    float                               null,
    Change_Time timestamp default CURRENT_TIMESTAMP null,
    constraint User_Cred_Log_users_ID_fk
        foreign key (User_ID) references users (ID)
);
