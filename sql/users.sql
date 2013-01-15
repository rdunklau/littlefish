begin;
create table "user" (
	login varchar primary key,
	password varchar
);

insert into "user" (login, password) values  ('bleue', '$6$rounds=64927$uTk4QmsranPbk.1i$cQXcydf4GJiZLkjre3lItFNtTDoClxEWyVSWHU4vyl6v2Acbg5L7xIIwQbWIQorRKh/6HSR8uulVv4ZMbpreb/');
insert into "user" (login, password) values ('test', '$6$rounds=60606$hQJZa6u9PqHU4K0V$5dP9mbUUnDkuBw3OB8yH6KE75i9eCOjz6LBtNuNiR0k4sMw9ueEZxLT2/FxtJpo3etY7xcT3VHCq797yxn3bE1')

alter table sequence add column user_login varchar not null references "user"(login) default 'bleue';
alter table seance add column user_login varchar not null references "user"(login) default 'bleue';

alter table etape add column user_login varchar not null references "user"(login) default 'bleue';

alter table etape alter user_login drop default;
alter table seance alter user_login drop default;
alter table sequence alter user_login drop default;

alter table etape add column creation_date date default current_timestamp;
alter table seance add column creation_date date default current_timestamp;
alter table sequence add column creation_date date default current_timestamp;

alter table etape add column copy_of_etape integer references etape(etape_id);
alter table seance add column copy_of_seance integer references seance(id);
alter table sequence add column copy_of_sequence integer references sequence(id);




commit;
