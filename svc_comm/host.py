APP_NAME = 'account_main'

LOG_SET = {
    'filename': '/data/logs/%s/%s.log' % (APP_NAME, APP_NAME),
    'maxBytes': 1000 * 1024 * 1024,
    'backupCount': 9
}

DLOG_SET = {
    'filename': '/data/logs/dlog/%s.log' % APP_NAME,
    'maxBytes': 100 * 1024 * 1024,
    'backupCount': 9
}

DB_ACCOUNT_RELEASE = {
    'host': '18.163.103.171',
    'port': 3306,
    'user': 'root',
    'password': 'mysql',
    'database': 'active',
    'charset': 'utf8',
    'autocommit': True,
    'connect_timeout': 3,
    'read_timeout': 10,
    'write_timeout': 5
}

from svc_comm.mysql_control import SimpleDb

model = SimpleDb()
# model.db_insert()
