from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import secrets
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))
CORS(app, supports_credentials=True)

DERIV_APP_ID = os.environ.get('DERIV_APP_ID', 'YOUR_APP_ID')
DERIV_OAUTH_URL = f'https://oauth.deriv.com/oauth2/authorize?app_id={DERIV_APP_ID}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html', oauth_url=DERIV_OAUTH_URL)

@app.route('/callback')
def callback():
    token1 = request.args.get('token1')
    token2 = request.args.get('token2')
    acct1 = request.args.get('acct1')
    
    if token1:
        # Store in session
        session['deriv_token'] = token1
        session['deriv_account'] = acct1
        if token2:
            session['deriv_token_demo'] = token2
        
        # Redirect to success page that shows token
        return redirect(url_for('show_token'))
    
    return 'Authentication failed. Please try again.', 400

@app.route('/show-token')
def show_token():
    token = session.get('deriv_token')
    demo_token = session.get('deriv_token_demo')
    account = session.get('deriv_account')
    
    if not token:
        return redirect(url_for('login'))
    
    return render_template('show_token.html', 
                         token=token, 
                         demo_token=demo_token,
                         account=account)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/health')
def health():
    return {'status': 'ok', 'version': 'v3-token-display'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
