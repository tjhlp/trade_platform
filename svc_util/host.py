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