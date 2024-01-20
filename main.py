from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
from modules.db_schemas import db, Clients, Site_admin
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeSerializer
from modules.client_utils import get_client_project_data, create_client_project, get_client_dashboard_data
from modules.admin_utils import get_admin_project_view_data, admin_update_asset_attributes, admin_create_new_asset, admin_del_project_asset, admin_create_new_project, admin_delete_proj, get_admin_dash_projects
from modules.payment_processor_utils import handle_create_checkout_session

app = Flask(__name__)

#site dev testing Mode varible for testing
dev_testing_mode = True

#Load Enviorment Variables for testing
if dev_testing_mode==True:
	load_dotenv()

#user login
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # change this and add it to an enviorment variable
digital_ocean_db_URI = os.getenv('DATABASE_URI')
#local_dev_db = os.getenv('DEV_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = digital_ocean_db_URI # Create Database and change name if needed
db.init_app(app)
login_manager = LoginManager(app)

digital_ocean_cors_config = {
    "origins": ["https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com", ""]
}

cors= CORS(app, resources={r"/deliverables": {"origins": "https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com"}})


#load user details
@login_manager.user_loader
def load_user(user_id):
    #check if user is an admin
    if 'Site_admin' in user_id:
        extracted_id = int(user_id.split(' ')[5].replace('>','')) # extract user_id and convert to int
        return Site_admin.query.get(extracted_id)
    else:
        return Clients.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    status_notification = str()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f'Username: {username}, Password: {password}')
        user = Clients.query.filter_by(username=username).first()

        #read hashed password
        #print('Check Hashed pass to entered password : ' + str(check_password_hash(hashed_password, password)))

        #read hashed password
        if user and check_password_hash(user.password, password) :
            login_user(user)
            return redirect('/dashboard')
        else:
            print('Unable to sign in user') #  testing delete later
            status_notification='Username or Password is incorrect.'

    return render_template('/user_templates/login.html',notification=status_notification) # create this file

@app.route('/signup', methods=['GET','POST'])
def signup():
    status_notification = str()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        retyped_password = request.form['re-typed-password']
        print(f'username: {username}\n email: {email}\n password: {password}\n re-typed password: {retyped_password}')
        #check if email and username exist.
        existing_username_test = Clients.query.filter_by(username=username).first()
        existing_email_test = Clients.query.filter_by(email=email).first()

        print(f'Existing User Name: {existing_username_test}\nExisting Email:{existing_email_test}')

        # do conditinal testing for existing email and password if both vars return none continue with signup process
        if existing_username_test == None and existing_email_test == None:
            print(f'Saving email and username to database')
            #hash passwords
            hashed_password = generate_password_hash(password, method='scrypt')
            print('Password : ' +  password + ' Hashed Password : ' + hashed_password)

            # Create a new user
            new_user = Clients(username=username, email=email, password=hashed_password)
            #Add the new user to the session
            db.session.add(new_user)
            # Commit the session to save the data
            db.session.commit()
            # show message
            status_notification = 'successfully created account!'

            #send email confirmation to clients email
            generate_confirmation_token(email)
            # redirect to confirm email.
            return redirect(f'/confirm_email/{email}')
        else:
            print(f'Username and or email already exist {username}, {email}')
            status_notification=f'Username and or email already exist {username}, {email}'

    return render_template('/user_templates/signup.html', notification=status_notification)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# Create Reset Password.

@app.route('/dashboard')
@login_required
def dashboard():
    project_objects = get_client_dashboard_data(current_user).projects
    return render_template('/user_templates/dashboard.html', username=current_user.username,project_objects=project_objects )



@app.route('/project-view/<int:project_id>', methods=['GET'])
@login_required
def project_view(project_id):
    return render_template('/user_templates/project_view.html', username=current_user.username, project_view_data=get_client_project_data(project_id))


@app.route('/profile-settings', methods=['GET','PUT'])
@login_required
def profile_settings():
    
    
    project_data = get_client_dashboard_data(current_user)
    return render_template('/user_templates/profile_settings.html', username=project_data.username, email=project_data.email, phone_number=project_data.phone_number, company=project_data.company)

@app.route('/start-project', methods=['GET', 'POST'])
@login_required
def start_project():
    status_message = str()

    if request.method == 'POST':
        json_data = request.json # Decode bytes to a string if necessary
        json_object = json.loads(json_data) # convert json string to python dict object

        # Gather data
        client_id = current_user.id

        current_datetime = datetime.now()
        current_date = current_datetime.date()

        create_client_project(json_object=json_object, client_id=client_id, current_date=current_date)

        # show message to user that data has been saved to database
        status_message = 'Successfully Created Project!'
        print('uploaded to database')
        return redirect('/dashboard')

    return render_template('/user_templates/start_project.html')


@app.route('/admin-login', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['admin_username']
        password = request.form['admin_password']
        
        # Check if user exist
        admin = Site_admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password) :
            #login
            login_user(admin)
            print('Admin Logged in')
            #redirect to admin dashboard
            return redirect('/admin-dashboard')
        
        print('Admin wrong password')

    return render_template('/admin_templates/admin_login.html')

@app.route('/logout-admin')
@login_required
def admin_logout():
    logout_user()
    return redirect('/admin-login')


@app.route('/admin-dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    admin_dash_data = get_admin_dash_projects()
    return render_template('admin_templates/admin_dashboard.html', username=current_user.username, projects=admin_dash_data.projects_data_obj,  all_clients=admin_dash_data.all_clients_obj)

@app.route('/admin-project-view/<int:project_id>', methods=['GET'])
@login_required
def admin_project_view(project_id):
    # Create Asset Object Models
    return render_template('admin_templates/admin_project_view.html', admin_proj_view_obj=get_admin_project_view_data(project_id), project_id=project_id)

@app.route('/update-asset-attributes', methods=['POST'])
def update_asset_attributes():
    json_data = request.json
    json_object = json.loads(json_data)
    print(json_object) # testing
    admin_update_asset_attributes(json_object)
    return jsonify(message="Saved Model Record to DB") # update this to a dynamic message

#
@app.route('/create-new-asset', methods=['POST'])
def create_new_asset():
    # get new asset json object
    json_data = request.json
    admin_create_new_asset(json_data)
    return jsonify(message="Saved New Asset Record to DB")

@app.route('/delete-project-asset', methods=['POST'])
def delete_project_asset():
    #Get asset to delete data object
    json_data = request.json
    admin_del_project_asset(json_data)
    return jsonify(message="Deleted Asset")

@app.route('/admin-create-new-project', methods=['POST'])
def admin_create_project():
    # Get Data Object
    json_data = request.json

    admin_create_new_project(json_data)

    return jsonify(message=f"Created New Client Project {json_data}")

@app.route('/admin-delete-project', methods=['POST'])
def admin_delete_project():
    # Get Data Object
    json_data = request.json
    admin_delete_proj(json_data)
    return jsonify(message="Deleted Client Project")

#SQL Database Setup



#Mail Setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER_NAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Email Confirmation
serializer = URLSafeSerializer(os.getenv('SECRET_KEY'))


def generate_confirmation_token(email_to):
    print(f'email to : {email_to}')   
    #send confirm token to user email
    #email_to = 'zspynet22@icloud.com'
    subject = 'High Altitude Media - Email Confirmation Token.'

     #generate confirm token
    token = serializer.dumps(email_to, salt='email-confirm-key')
    print(f'token: {token}')

    msg = Message(
        subject,
        recipients=[email_to],
        html=f'<h3 style="color: white; text-align:center; font-weight: bold;" >Token Key : {token}</h3>',
        sender=app.config['MAIL_USERNAME']
    )
    mail.send(msg)

@app.route('/confirm_email/<string:email_to>', methods=["GET","POST"])
def confirm_email(email_to):
    message = ''
    if request.method == 'POST':
        token = request.form["token_key_input"]
        # Confirm Token then log in user if success
        try:
            email = serializer.loads(token, salt="email-confirm-key", max_age=3600)
            print(f'user entered token: {request.form["token_key_input"]}  email: { email }')
            #log in user
            user = Clients.query.filter_by(email=email).first() 
            login_user(user)
            return redirect('/dashboard')
        except:
            print(f'Invalid confirmation Token')
            message=f'Invalid confirmation Token: {token}'
        

    return render_template('authenication/confirm_email.html', email=email_to, notification=message)

#create request feature to update email, password/reset, and username

@app.route('/')
def home():
    title = 'See Your Build'
    # add to the services overview desc
    services_Overview = 'Real Time Drone Services for Construction Progress Monitoring'
    return render_template('home.html',Title=title, Services_Overview=services_Overview)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/appointment-booking')
def appointmentBooking():
    return render_template('appointment-booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact_send_email', methods=['POST'])
def contact_send_email():
    client_name = request.form.get('client-name')
    client_email = request.form.get('client-email')
    client_phone = request.form.get('client-phone-number')

    project_location = request.form.get('property-location')
    project_Info = request.form.get('project-info-text-area')

    still_imaging_service = request.form.get('still-image-service')
    videography_service = request.form.get('videography-service')
    virtual_tour_service = request.form.get('virtual-tour-service')
    model_service = request.form.get('model-3d-service')
    undecided_service = request.form.get('unsure-service')

    #testing
    tst_msg = Message(f"Client Contact - {client_name}", sender=client_email, recipients=['zion.johnson@high-altitude-media.com'])
    tst_msg.body = f"Name: '{client_name}'\nEmail: {client_email}\nPhone: {client_phone}\nProject_Location: {project_location}\nProject_Info: {project_Info}\nStill_imaging_Service: {still_imaging_service}\nVideography_Service: {videography_service}\nVirtual_Tour_Service: {virtual_tour_service}\n3D_Modeling_Service: {model_service}\nUndecided_Service: {undecided_service}"

    #create a varible for storing email status notification
    status_notification = str()

    try:
        if not mail.is_connected:
            mail.connect()
            print(f'mail server connected: {mail.is_connected}')
            mail.send(tst_msg)
            status_notification = 'Contact Email Successfully sent. We will get back to soon!'
    except Exception as e:
        print("SMTP server connection failed:", str(e))
        status_notification = f'Error Sending Email: {str(e)}'
        return str(e)

    return render_template("home.html", notification=status_notification)

@cross_origin()
@app.route('/deliverables')
def client_deliverables():
    client_property_name = "Example Property Name"
    return render_template('client-deliverables-base.html')

# get 3d model data
@app.route('/construction-services')
def construction_services():
    return render_template('construction-services.html')

@app.route('/aerial-imaging-services')
def aerial_imaging_services():
    return render_template('aerial-imaging-services.html')

@app.route('/data-formats-provided')
def data_formats_provided():
    return render_template('/data-formats-provided.html')

@app.route('/portfolio')
def portfolio():
    return render_template('/portfolio.html')


# Need to create a debug mode for backend testing
# this route takes in a query Paramerter for product ex. /page?product='product ID'
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    session_url = handle_create_checkout_session(request, dev_testing_mode)
    return redirect(session_url, code=303)

# Payment Success Endpoint
@app.route('/payment-success', methods=['GET'])
def payment_success():
    return render_template('/payment_processing/payment_success.html')

# Payment Cancel Endpoint
@app.route('/payment-cancled', methods=['GET'])
def payment_cancled():
    return render_template('/payment_processing/payment_cancel.html')

# Check out page
@app.route('/services-checkout')
def service_checkout():
    return render_template('/payment_processing/checkout.html')


#Run in debug mode while testing
if dev_testing_mode==True:
    app.run(debug=True)

if __name__ == '__main__':
    db.create_all() # Create database tables
    app.run()