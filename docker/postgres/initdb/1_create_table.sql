CREATE TABLE t_command_list
(
    id serial NOT NULL,
    cmd_name varchar NULL,
    value varchar NULL,
    cmd_type varchar NULL,
    description text NULL,
    CONSTRAINT t_command_list_pk PRIMARY KEY (id)
);

CREATE TABLE t_host_list
(
    id serial NOT NULL,
    ip_address inet NULL,
    mac_address macaddr NULL,
    host_name text NULL,
    state varchar NULL,
    target int NULL,
    ostype varchar NULL,
    osname varchar NULL,
    "timestamp" timestamp NULL,
    CONSTRAINT t_host_list_pk PRIMARY KEY (id)
);

CREATE TABLE t_port_list (
    id serial NOT NULL,
    host_id int NULL,
    protocol varchar NULL,
    port_num varchar NULL,
    state varchar NULL,
    serv_name varchar NULL,
    serv_prod varchar NULL,
    serv_ver varchar NULL,
    extrainfo varchar NULL,
    "timestamp" timestamp NULL,
    CONSTRAINT t_port_list_pk PRIMARY KEY (id)
);

CREATE TABLE t_job_list (
    id serial NOT NULL,
    command text NULL,
    status varchar NULL,
    "timestamp" timestamp NULL,
    CONSTRAINT t_job_list_pk PRIMARY KEY (id)
);

CREATE TABLE t_vuln_list (
    id serial NOT NULL,
    port_id int NULL,
    script_id varchar NULL,
    "output" text NULL,
    "timestamp" timestamp,
    CONSTRAINT t_vuln_list_pk PRIMARY KEY (id)
);

CREATE TABLE t_message_list (
    id serial NOT NULL,
    msgid varchar NULL,
    "token" varchar NULL,
    actor varchar NULL,
    message varchar NULL,
    response varchar NULL,
    CONSTRAINT t_message_list_pk PRIMARY KEY (id)
);