set names utf8;
use active;
drop table account;

create table account(
	id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '自增id',
    name VARCHAR(20) NOT NULL COMMENT '创建者',
	account_condition VARCHAR(4096) DEFAULT NULL COMMENT '账单信息',
    account_attr TINYINT(3) NOT NULL DEFAULT 0 COMMENT '0:私有；1:公共',
	created_time DATETIME NOT NULL DEFAULT '2000-01-01 00:00:00'
) charset='utf8';

ALTER TABLE account
    ADD COLUMN user_id BIGINT(20) NOT NULL COMMENT '用户id' default 0;

ALTER TABLE account
    ADD COLUMN state VARCHAR(10) NOT NULL COMMENT '状态' DEFAULT '正常';



