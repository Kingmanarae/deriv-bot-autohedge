from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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
    if 'deriv_token' not in session:
        return redirect(url_for('login'))
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
        session['deriv_token'] = token1
        session['deriv_account'] = acct1
        if token2:
            session['deriv_token_demo'] = token2
        return redirect(url_for('index'))
    
    return 'Authentication failed. Please try again.', 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/token')
def get_token():
    account_type = request.args.get('type', 'real')
    token_key = 'deriv_token' if account_type == 'real' else 'deriv_token_demo'
    token = session.get(token_key, session.get('deriv_token'))
    
    if token:
        return jsonify({'token': token, 'account': session.get('deriv_account')})
    return jsonify({'error': 'Not authenticated'}), 401

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'version': 'v3'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
