from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-later'

# Demo credentials - replace with AWS Cognito later
DEMO_USERS = {
    'admin': {'password': 'password', 'role': 'admin', 'name': 'Admin User', 'image': 'https://ui-avatars.com/api/?name=Admin+User&background=0c2340&color=C99700'},
    'client': {'password': 'password', 'role': 'client', 'name': 'John Doe', 'image': 'https://ui-avatars.com/api/?name=John+Doe&background=0c2340&color=C99700'},
    'mcostello': {'password': 'miller64', 'role': 'client', 'name': 'Matt Costello', 'image': 'https://ui-avatars.com/api/?name=John+Doe&background=0c2340&color=C99700'},
}

USER_DOCUMENTS = {
    'mcostello': [
        {
            'filename': 'PA_Drivers_License.jpg',
            'filepath': 'static/documents/mcostello/PA_Drivers_License.jpg',
            'type': 'image'
        },
        {
            'filename': 'LeaseHCV.pdf',
            'filepath': 'static/documents/mcostello/LeaseHCV.pdf',
            'type': 'pdf'
        }
    ]
}

# Decorator for route protection
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def client_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session.get('role') != 'client':
            flash('Client access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in DEMO_USERS and DEMO_USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = DEMO_USERS[username]['role']
            session['name'] = DEMO_USERS[username]['name']
            session['image'] = DEMO_USERS[username]['image']
            flash(f'Welcome back, {session["name"]}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Try username: admin or client, password: password', 'danger')
    
    return render_template('login.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        flash('Account creation will be integrated with AWS Cognito.', 'info')
        return redirect(url_for('login'))
    return render_template('create_account.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

# Public routes
@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Client routes
@app.route('/transactions')
@login_required
@client_required
def transactions():
    return render_template('transactions.html')

@app.route('/policy-documents')
@login_required
@client_required
def policy_documents():
    documents = USER_DOCUMENTS[session.get('username')]
    return render_template('policy_documents.html', documents=documents)

@app.route('/services')
@login_required
@client_required
def services():
    return render_template('services.html')

# Admin routes
@app.route('/user-management')
@login_required
@admin_required
def user_management():
    return render_template('user_management.html')

@app.route('/payroll')
@login_required
@admin_required
def payroll():
    return render_template('payroll.html')

@app.route('/dashboards')
@login_required
@admin_required
def dashboards():
    return render_template('dashboards.html')

@app.route('/auto')
@login_required
@admin_required
def auto():
    return render_template('auto.html')

@app.route('/home-insurance')
@login_required
@admin_required
def home_insurance():
    return render_template('home_insurance.html')

@app.route('/life-insurance')
def life_insurance():
    return render_template('life_insurance.html')

@app.route('/auto-insurance')
def auto_insurance():
    return render_template('auto_insurance.html')

@app.route('/home-insurance-info')
def home_insurance_info():
    return render_template('home_insurance.html')

@app.route('/life')
@login_required
@admin_required
def life():
    return render_template('life.html')

# Shared profile route
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Document upload
@app.route('/document-upload')
@login_required
def document_upload():
    return render_template('document_upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    # app.run(debug=True, port=5000)