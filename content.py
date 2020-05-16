from flask import Flask
# from account.account_main import Account
from user.user_main import User

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# Account.setup(application)
User.setup(app)
 

@app.route('/')
def home():
    return 'home_page'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True, processes=1)
    # application.run(host='127.0.0.1', port=8002, debug=True, processes=1)
