set names utf8;
use active;
drop table user;

create table user(
	id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '自增id',
    name VARCHAR(128) NOT NULL COMMENT '昵称',
    mobile VARCHAR(20) NOT NULL COMMENT '手机号',
    password VARCHAR(20) NOT NULL COMMENT '密码',
    state VARCHAR(10) NOT NULL COMMENT '状态' DEFAULT '正常',
	created_time DATETIME NOT NULL DEFAULT '2000-01-01 00:00:00',
	UNIQUE (name)
) charset='utf8';

ALTER TABLE user
    DROP INDEX name;

ALTER TABLE user
    ADD COLUMN email VARCHAR(30) NOT NULL COMMENT '手机号' default '';


