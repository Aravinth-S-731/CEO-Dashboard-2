from flask import Flask, session, redirect, url_for
from datetime import timedelta

from landingPage.landingPage import landing_page, init_mysql_auth
from authentication.authentication import auth, init_mysql_auth
from homePage.homePage import homePage
from financialPage.financialPage import financialPage
from marketingPage.marketingPage import marketingPage
from operationalPage.operatingPage import operationalPage
from communicationPage.communicationPage import communicationPage

from adminDashboard.adminDashboard import adminDashboard

app = Flask(__name__)
app.secret_key = 'r$W9#kLp2&QnX@5*8yZ$'

init_mysql_auth(app)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect (url_for('auth.login'))

app.register_blueprint(landing_page)
app.register_blueprint(auth)
app.register_blueprint(homePage)
app.register_blueprint(financialPage)
app.register_blueprint(marketingPage)
app.register_blueprint(operationalPage)
app.register_blueprint(communicationPage)

app.register_blueprint(adminDashboard)


if __name__ == "__main__":
    [app.run(host="0.0.0.0", port=5000, debug=True)]