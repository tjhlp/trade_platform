set names utf8;
use active;
drop table whitelist;

create table account(
	id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '自增id',
    user_id INT(11) NOT NULL COMMENT '创建者',
	invitor_id INT(11) DEFAULT NULL COMMENT '协作者',
	created_time DATETIME NOT NULL DEFAULT '2000-01-01 00:00:00'
) charset='utf8';





