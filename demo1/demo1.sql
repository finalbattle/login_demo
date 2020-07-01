create table user(
  id INT(11) auto_increment,
  username varchar(20) not null,
  password varchar(100) not null,
  create_time datetime not null default current_time,
  primary key (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
