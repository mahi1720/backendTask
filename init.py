from flask import Flask

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.headers.get("Authorization"))

@limiter.request_filter
def exempt_users():
    # You may want to exempt some users from rate limiting here
    return False

@limiter.request_method
def get_http_method():
    return request.method
from flask_oauthlib.client import OAuth

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='YOUR_CLIENT_ID',
    consumer_secret='YOUR_CLIENT_SECRET',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('index'))

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    # Save user_info in your database or session as needed

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
