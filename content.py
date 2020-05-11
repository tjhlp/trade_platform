from flask import Flask
from account.account_main import Account
from user.user_main import User

application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
Account.setup(application)
User.setup(application)


@application.route('/')
def home():
    return 'home_page'


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8002, debug=True, processes=1)
    # application.run(host='127.0.0.1', port=8002, debug=True, processes=1)
