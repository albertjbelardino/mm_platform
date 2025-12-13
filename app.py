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

# Business Nav Pages
# Auto Insurance Routes
@app.route('/auto-insurance/accident-forgiveness')
def auto_accident_forgiveness():
    return render_template('auto_insurance/accident_forgiveness.html')

@app.route('/auto-insurance/collision-coverage')
def auto_collision_coverage():
    return render_template('auto_insurance/collision_coverage.html')

@app.route('/auto-insurance/comprehensive-coverage')
def auto_comprehensive_coverage():
    return render_template('auto_insurance/comprehensive_coverage.html')

@app.route('/auto-insurance/diminishing-deductible')
def auto_diminishing_deductible():
    return render_template('auto_insurance/diminishing_deductible.html')

@app.route('/auto-insurance/liability-coverage')
def auto_liability_coverage():
    return render_template('auto_insurance/liability_coverage.html')

@app.route('/auto-insurance/medical-payments-coverage')
def auto_medical_payments():
    return render_template('auto_insurance/medical_payments_coverage.html')

@app.route('/auto-insurance/personal-injury-protection')
def auto_personal_injury():
    return render_template('auto_insurance/personal_injury_protection.html')

@app.route('/auto-insurance/rental-reimbursement')
def auto_rental_reimbursement():
    return render_template('auto_insurance/rental_reimbursement.html')

@app.route('/auto-insurance/roadside-assistance')
def auto_roadside_assistance():
    return render_template('auto_insurance/roadside_assistance.html')

@app.route('/auto-insurance/towing')
def auto_towing():
    return render_template('auto_insurance/towing.html')

@app.route('/auto-insurance/uninsured-and-underinsured-motorist-coverage')
def auto_uninsured_motorist():
    return render_template('auto_insurance/uninsured_and_underinsured_motorist_coverage.html')

# Business and Commercial Routes
@app.route('/business-and-commercial/builders-risk-insurance')
def business_builders_risk():
    return render_template('business_and_commercial/builders_risk_insurance.html')

@app.route('/business-and-commercial/commercial-auto')
def business_commercial_auto():
    return render_template('business_and_commercial/commercial_auto.html')

@app.route('/business-and-commercial/commercial-property-insurance')
def business_commercial_property():
    return render_template('business_and_commercial/commercial_property_insurance.html')

@app.route('/business-and-commercial/commercial-umbrella-insurance')
def business_commercial_umbrella():
    return render_template('business_and_commercial/commercial_umbrella_insurance.html')

@app.route('/business-and-commercial/cyber-insurance')
def business_cyber():
    return render_template('business_and_commercial/cyber_insurance.html')

@app.route('/business-and-commercial/directors-and-officers-insurance')
def business_directors_officers():
    return render_template('business_and_commercial/directors_and_officers_insurance.html')

@app.route('/business-and-commercial/epli-insurance')
def business_epli():
    return render_template('business_and_commercial/epli_insurance.html')

@app.route('/business-and-commercial/errors-and-omissions-insurance')
def business_errors_omissions():
    return render_template('business_and_commercial/errors_and_omissions_insurance.html')

@app.route('/business-and-commercial/general-liability')
def business_general_liability():
    return render_template('business_and_commercial/general_liability.html')

@app.route('/business-and-commercial/inland-marine-insurance')
def business_inland_marine():
    return render_template('business_and_commercial/inland_marine_insurance.html')

@app.route('/business-and-commercial/medical-malpractice-insurance')
def business_medical_malpractice():
    return render_template('business_and_commercial/medical_malpractice_insurance.html')

@app.route('/business-and-commercial/workers-compensation')
def business_workers_comp():
    return render_template('business_and_commercial/workers_compensation.html')

# Employee Coverage Routes
@app.route('/employee-coverage/disability-insurance-for-employees')
def employee_disability():
    return render_template('employee_coverage/disability_insurance_for_employees.html')

@app.route('/employee-coverage/group-benefits')
def employee_group_benefits():
    return render_template('employee_coverage/group_benefits.html')

@app.route('/employee-coverage/group-disability-insurance')
def employee_group_disability():
    return render_template('employee_coverage/group_disability_insurance.html')

@app.route('/employee-coverage/group-health-insurance')
def employee_group_health():
    return render_template('employee_coverage/group_health_insurance.html')

@app.route('/employee-coverage/individual-life-insurance-for-employees')
def employee_individual_life():
    return render_template('employee_coverage/individual_life_insurance_for_employees.html')

@app.route('/employee-coverage/retiree-health-coverage')
def employee_retiree_health():
    return render_template('employee_coverage/retiree_health_coverage.html')

@app.route('/employee-coverage/voluntary-benefits')
def employee_voluntary_benefits():
    return render_template('employee_coverage/voluntary_benefits.html')

# Health Insurance Routes
@app.route('/health-insurance/child-health-insurance')
def health_child():
    return render_template('health_insurance/child_health_insurance.html')

@app.route('/health-insurance/dental-insurance')
def health_dental():
    return render_template('health_insurance/dental_insurance.html')

@app.route('/health-insurance/disability-health-insurance')
def health_disability():
    return render_template('health_insurance/disability_health_insurance.html')

@app.route('/health-insurance/group-health-insurance')
def health_group():
    return render_template('health_insurance/group_health_insurance.html')

@app.route('/health-insurance/hsas-insurance')
def health_hsas():
    return render_template('health_insurance/hsas_insurance.html')

@app.route('/health-insurance/individual-and-family-health-insurance')
def health_individual_family():
    return render_template('health_insurance/individual_and_family_health_insurance.html')

@app.route('/health-insurance/longterm-care-health-insurance')
def health_longterm_care():
    return render_template('health_insurance/longterm_care_health_insurance.html')

@app.route('/health-insurance/medical-expense-insurance')
def health_medical_expense():
    return render_template('health_insurance/medical_expense_insurance.html')

@app.route('/health-insurance/prescription-insurance')
def health_prescription():
    return render_template('health_insurance/prescription_insurance.html')

@app.route('/health-insurance/vision-insurance')
def health_vision():
    return render_template('health_insurance/vision_insurance.html')

# Home Insurance Routes
@app.route('/home-insurance/condo-insurance')
def home_condo():
    return render_template('home_insurance/condo_insurance.html')

@app.route('/home-insurance/homeowners-liability')
def home_homeowners_liability():
    return render_template('home_insurance/homeowners_liability.html')

@app.route('/home-insurance/landlords-insurance')
def home_landlords():
    return render_template('home_insurance/landlords_insurance.html')

@app.route('/home-insurance/property-insurance')
def home_property():
    return render_template('home_insurance/property_insurance.html')

@app.route('/home-insurance/renters-insurance')
def home_renters():
    return render_template('home_insurance/renters_insurance.html')

@app.route('/home-insurance/scheduled-property-insurance')
def home_scheduled_property():
    return render_template('home_insurance/scheduled_property_insurance.html')

# Life Insurance Routes
@app.route('/life-insurance/disability-insurance')
def life_disability():
    return render_template('life_insurance/disability_insurance.html')

@app.route('/life-insurance/group-life-insurance')
def life_group():
    return render_template('life_insurance/group_life_insurance.html')

@app.route('/life-insurance/individual-life-insurance')
def life_individual():
    return render_template('life_insurance/individual_life_insurance.html')

@app.route('/life-insurance/key-person-insurance')
def life_key_person():
    return render_template('life_insurance/key_person_insurance.html')

@app.route('/life-insurance/longterm-care-insurance')
def life_longterm_care():
    return render_template('life_insurance/longterm_care_insurance.html')

@app.route('/life-insurance/mortgage-protection-instruction')
def life_mortgage_protection():
    return render_template('life_insurance/mortgage_protection_instruction.html')

@app.route('/life-insurance/second-to-die-policy')
def life_second_to_die():
    return render_template('life_insurance/second_to_die_policy.html')

# Other Personal Insurance Routes
@app.route('/other-personal-insurance/data-backup')
def other_data_backup():
    return render_template('other_personal_insurance/data_backup.html')

@app.route('/other-personal-insurance/identity-theft-coverage')
def other_identity_theft():
    return render_template('other_personal_insurance/identity_theft_coverage.html')

@app.route('/other-personal-insurance/personal-umbrella-insurance')
def other_personal_umbrella():
    return render_template('other_personal_insurance/personal_umbrella_insurance.html')

# Recreational Vehicle Insurance Routes
@app.route('/recreational-vehicle-insurance/atv-insurance')
def recreational_atv():
    return render_template('recreational_vehicle_insurance/atv_insurance.html')

@app.route('/recreational-vehicle-insurance/boat-insurance')
def recreational_boat():
    return render_template('recreational_vehicle_insurance/boat_insurance.html')

@app.route('/recreational-vehicle-insurance/motorcycle-insurance')
def recreational_motorcycle():
    return render_template('recreational_vehicle_insurance/motorcycle_insurance.html')

@app.route('/recreational-vehicle-insurance/motorhome-insurance')
def recreational_motorhome():
    return render_template('recreational_vehicle_insurance/motorhome_insurance.html')

@app.route('/recreational-vehicle-insurance/snowmobile-insurance')
def recreational_snowmobile():
    return render_template('recreational_vehicle_insurance/snowmobile_insurance.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    # app.run(debug=True, port=5000)