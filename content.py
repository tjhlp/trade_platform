from flask import Flask
from account.account_main import Account

application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
Account.setup(application)

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8002, debug=True, processes=1)