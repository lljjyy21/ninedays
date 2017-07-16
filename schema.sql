drop table if exists finance;
create table stock (
  id integer primary key autoincrement,
  stock_title text not null
);