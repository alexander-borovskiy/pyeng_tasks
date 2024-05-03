-- Schema for dhcp-snopping parsing example.

create table if not exists switches (
    hostname    text not null primary key,
    location    text
);

create table if not exists dhcp (
    mac          text primary key,
    ip           text,
    vlan         text,
    interface    text,
    switch       text not null references switches(hostname)
);
