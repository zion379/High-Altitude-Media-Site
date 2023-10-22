from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mail import Mail, Message
import requests
from flask_cors import CORS, cross_origin
import stripe
import boto3
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
from datetime import datetime

app = Flask(__name__)

#site dev testing Mode varible for testing
dev_testing_mode = True

#Load Enviorment Variables for testing
if dev_testing_mode==True:
	load_dotenv()

#user login
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # change this and add it to an enviorment variable
digital_ocean_db_URI = os.getenv('DATABASE_URI')
local_dev_db= os.getenv('DEV_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = digital_ocean_db_URI # Create Database and change name if needed
db = SQLAlchemy(app)
login_manager = LoginManager(app)

#Data Base Schemas
class Clients(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    company = db.Column(db.Text,nullable=True)
    
    #Create one-to-many relationship to Projects
    projects = relationship('Projects', back_populates='client')

class Projects(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    project_description = db.Column(db.Text, nullable=True)
    project_address = db.Column(db.Text, nullable=True)
    project_tax_parcel = db.Column(db.Text, nullable=True)
    still_image_service = db.Column(db.Text, default=False)
    videography_service = db.Column(db.Boolean, default=False)
    model_3d_service = db.Column(db.Boolean, default=False)
    ortho_service = db.Column(db.Boolean, default=False)
    virtual_tour_service = db.Column(db.Boolean, default=False)
    airspace_authorization = db.Column(db.Boolean, default=False)
    intial_site_visit = db.Column(db.Boolean, default=False)
    flight_plan_created = db.Column(db.Boolean, default=False)
    data_collected = db.Column(db.Boolean, default=False)
    deliverables_uploaded = db.Column(db.Boolean, default=False)

    # Create a many-to-one relation ship to clients
    client = relationship('Clients', back_populates='projects')


class Site_admin(UserMixin, db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password  = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)

    def id(self):
        return f'admin_{get_actual_id()}' # modify user id to distinguish between user and admin

    def get_actual_id(self):
        return admin_id

class Models_3d(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, ForeignKey('projects.id'), nullable=False)
    model_url = db.Column(db.Text, nullable=False)
    model_desc = db.Column(db.Text, nullable=True)

    #Create one-to-one relationship to Projects
    projects = relationship('Projects', backref='models_3d', uselist=False, lazy='joined')

class Virtual_tour_projects(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.Date, nullable=False)
    tour_desc = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, ForeignKey('projects.id'), nullable=False)

    #Create one-to-one relationship to Projects
    projects = relationship('Projects', backref='virtual_tour_projects', uselist=False, lazy="joined")

class Virtual_tour_photos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, ForeignKey('virtual_tour_projects.id'), nullable=False)
    photo_url = db.Column(db.Text, nullable=False)

    #Create one-to-one relationship to Projects
    tour_projects = relationship('Virtual_tour_projects', backref='virtual_tour_photos', uselist=False, lazy="joined")


class Orthomosaics_2D(UserMixin, db.Model):
    __tablename__ =  'orthomosaics_2d'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, ForeignKey('projects.id'), nullable=False)
    ortho_url = db.Column(db.Text, nullable=False)
    ortho_desc = db.Column(db.Text, nullable=True)

    #Create one-to-one relationship to Projects
    projects = relationship('Projects', backref='orthomosaics_2d', uselist=False, lazy="joined")

class Still_photos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, ForeignKey('projects.id'), nullable=False)
    photo_url = db.Column(db.Text, nullable=False)
    is_progression_photo = db.Column(db.Boolean, default=False)
    photo_desc = db.Column(db.Text, nullable=True)

    #Create one-to-one relationship to Projects
    projects = relationship('Projects', backref='still_photos', uselist=False, lazy="joined")

class Videos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, ForeignKey('projects.id'), nullable=False)
    video_url = db.Column(db.Text, nullable=False)
    video_desc = db.Column(db.Text, nullable=True)

    #Create one-to-one relationship to Projects
    projects = relationship('Projects', backref='videos', uselist=False, lazy="joined")

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
        if user and user.password == password:
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
            # Create a new user
            new_user = Clients(username=username, email=email, password=password)
            #Add the new user to the session
            db.session.add(new_user)
            # Commit the session to save the data
            db.session.commit()
            # show message
            status_notification = 'successfully created account!'

            #log in user
            user = Clients.query.filter_by(username=username).first() 
            login_user(user)

            # redirect to dashboard
            return redirect('/dashboard')
        else:
            print(f'Username and or email already exist {username}, {email}')
            status_notification=f'Username and or email already exist {username}, {email}'

    return render_template('/user_templates/signup.html', notification=status_notification)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# dashboard helper objects
class Project:
    def __init__(self,project_id , description, project_date, project_url):
        self.project_id = project_id
        self.description = description
        self.project_date = project_date
        self.project_url = project_url

@app.route('/dashboard')
@login_required
def dashboard():
    # load projects
    current_user_projects = Projects.query.filter_by(client_id=current_user.id).all()
    project_count = len(current_user_projects)

    project_index = 0

    project_objects = []

    #Check if there are any projects for client
    if project_count != 0:
        for project in current_user_projects:
            if project_index >= (project_count):
                project_index = 0
            
            # get Project Attributes
            project_id = str(current_user_projects[project_index].id)
            description = str(current_user_projects[project_index].project_description)
            date = str(current_user_projects[project_index].creation_date)
            project_url = f'/project-view/{project_id}'
            
            #create data object and add it to project_objects list
            project_obj = Project(project_id,description,date, project_url)
            project_objects.append(project_obj)
            project_index += 1

    return render_template('/user_templates/dashboard.html', username=current_user.username,project_objects=project_objects )

#Project View Data Object
class Project_View:
    def __init__(self,description, date, project_location, model3d_url):
        self.description = description
        self.date = date
        self.project_location = project_location
        self.model3d_url = model3d_url

@app.route('/project-view/<int:project_id>', methods=['GET'])
@login_required
def project_view(project_id):

    #task: validate user access by checking project client id and current logged in user id.

    current_project = Projects.query.filter_by(id=project_id).first()

    #Get Project Data
    description  = str(current_project.project_description)
    date = str(current_project.creation_date)
    project_location = str()
    project_address = str(current_project.project_address)
    project_tax_parcel = str(current_project.project_tax_parcel)

    # Do additional checks for project services and gather data for client assets ids.

    #Get address type and set project location var
    if len(project_address) == 0 and len(project_tax_parcel) == 0:
        project_location = 'None'
    elif len(project_address) == 0 and len(project_tax_parcel) != 0:
        project_location = str(project_tax_parcel)
    elif len(project_address) != 0 and len(project_tax_parcel) == 0:
        project_location = project_address
        print(f'project location: {project_location}')

    #Get 3D Model File URL
    #model3d_url = 'https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com/example-property/small_format_property.glb'
    # Testing 3D Model Viewer with loading a different model
    model3d_url = 'https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com/example-property/skull.glb'


    #Create data object
    project_view_data = Project_View(description,date, project_location, model3d_url)

    return render_template('/user_templates/project_view.html', username=current_user.username, project_view_data=project_view_data)


@app.route('/profile-settings', methods=['GET','PUT'])
@login_required
def profile_settings():
    #Create routes and pages to update individual fields
    username = current_user.username
    email = current_user.email
    phone_number = current_user.phone_number
    company = current_user.company
   
    return render_template('/user_templates/profile_settings.html', username=username, email=email, phone_number=phone_number, company=company)

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

        project_description = json_object["additional_details"]

        location_type = json_object['location_type']

        project_address = str
        project_tax_parcel = str

        if location_type == "street_address":
            project_address = json_object['location_val']
            project_tax_parcel = ''
        else:
            project_address = ''
            project_tax_parcel = json_object['location_val']

        still_image_service = json_object['still_images']
        videography_service = json_object['videography']
        model_3d_service = json_object['model_3d']
        ortho_service = json_object['ortho']
        virtual_tour_service = json_object['virtual_tour']

        # save data to database
        #create new project object
        new_project = Projects(client_id=client_id, creation_date=current_date, project_description=project_description, project_address=project_address, project_tax_parcel=project_tax_parcel, still_image_service=still_image_service, videography_service=videography_service, model_3d_service=model_3d_service, ortho_service=ortho_service,virtual_tour_service=virtual_tour_service)

        db.session.add(new_project)

        db.session.commit()

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
        if admin and admin.password == password:
            #login
            login_user(admin)

            #redirect to admin dashboard
            return redirect('/admin-dashboard')

    return render_template('/admin_templates/admin_login.html')

@app.route('/logout-admin')
@login_required
def admin_logout():
    logout_user()
    return redirect('/admin-login')

#Admin Client Projects View Data Object
class Client_Project_obj:
    def __init__(self,project_id, date, location, project_url, client_id, client_username):
        self.project_id = project_id
        self.date = date
        self.location = location
        self.project_url = project_url
        self.client_id = client_id
        self.client_username = client_username

@app.route('/admin-dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    all_client_projects = Projects.query.all()
    total_projects = len(all_client_projects)
    project_index = 0

    projects_data_objects = []

    #Check if any projects exist
    if total_projects != 0 :
        for client_project in all_client_projects:
            project_id = all_client_projects[project_index].id
            creation_date = all_client_projects[project_index].creation_date
            location = str

            if all_client_projects[project_index].project_address != None:
                location = all_client_projects[project_index].project_address
            else:
                location = all_client_projects[project_index].project_tax_parcel

            client_id = all_client_projects[project_index].client_id
            #get client username
            client_username = Clients.query.filter_by(id=client_id).first().username

            # Create URL to admin project page view

            #create data object
            project_data = Client_Project_obj(project_id, creation_date, location, f'/admin-project-view/{project_id}', client_id, client_username)
            
            projects_data_objects.append(project_data)

            project_index += 1

    return render_template('admin_templates/admin_dashboard.html', username=current_user.username, projects=projects_data_objects)

# Admin Project View Objects

#Admin services obj
class Admin_project_services_obj:
    def __init__(self, model_service: bool, tour_service: bool, ortho_service: bool, stills_service: bool, video_service: bool):
        self.model_service: bool = model_service
        self.tour_service: bool = tour_service
        self.ortho_service: bool = ortho_service
        self.stills_service: bool = stills_service
        self.video_service: bool = video_service

#Admin 3D Models Object
class Admin_3dModel_obj:
    def __init__(self, model_id: int, project_id: int, model_url: str, model_desc: str):
        self.model_id: int = model_id
        self.project_id: int = project_id
        self.model_url: str = model_url
        self.model_desc: str = model_desc

#Admin Tour Object
class Admin_virtual_tour_obj:
    def __init__(self, tour_id: int, project_id: int, date: str, tour_desc: str):
        self.tour_id: int = tour_id
        self.project_id: int = project_id
        self.date: str = date
        self.tour_desc: str = tour_desc

#Admin Tour Image Object
class Admin_virtual_tour_img_obj:
    def __init__(self, img_id: int, tour_id: int, photo_url: str):
        self.img_id: int = img_id
        self.tour_id: int = tour_id
        self.photo_url: str = photo_url

#Admin Ortho Object
class Admin_ortho_obj:
    def __init__(self, ortho_id: int, project_id: int, ortho_url: str, ortho_desc:str):
        self.ortho_id: int = ortho_id
        self.project_id: int = project_id
        self.ortho_url: str = ortho_url
        self.ortho_desc: str = ortho_desc

#Admin Still Image Object
class Admin_still_image_obj:
    def __init__(self, still_id: int, project_id: int, photo_url: str, is_progression_photo: bool, photo_desc: str):
        self.still_id: int = still_id
        self.project_id: int = project_id
        self.photo_url: str = photo_url
        self.is_progression_photo: bool = is_progression_photo
        self.photo_desc: str = photo_desc

#Admin Videos Object
class Admin_video_obj:
    def __init__(self, video_id: int, project_id: int, video_url: str, video_desc: str):
        self.video_id: int = video_id
        self.project_id: int = project_id
        self.video_url: str = video_url
        self.video_desc: str = video_desc

#Admin Project View Object
class Admin_project_view_obj:
    def __init__(self, client_id: int, client_username: str, date: str, project_desc: str, project_location, services_obj: Admin_project_services_obj, models_3d_obj: list[Admin_3dModel_obj], tours_obj: list[Admin_virtual_tour_obj], orthos_obj: list[Admin_ortho_obj], stills_obj: list[Admin_still_image_obj], videos_obj: list[Admin_video_obj]):
        self.client_id: int = client_id
        self.client_username: str = client_username
        self.date: str = date
        self.project_desc: str = project_desc
        self.project_location = project_location
        self.services_obj: Admin_project_services_obj = services_obj
        self.models_3d_obj: list[Admin_3dModel_obj] = models_3d_obj
        self.tours_obj: list[Admin_virtual_tour_obj] = tours_obj
        self.orthos_obj: list[Admin_ortho_obj] = orthos_obj
        self.stills_obj: list[Admin_still_image_obj] = stills_obj
        self.videos_obj: list[Admin_video_obj] = videos_obj

@app.route('/admin-project-view/<int:project_id>', methods=['GET'])
@login_required
def admin_project_view(project_id):
    # Create Asset Object Models
    # Retreive project videos
    videos_list: Admin_video_obj = [] # Videos Object List
    all_project_videos = Videos.query.filter_by(project_id=project_id).all() 
    

    for video in all_project_videos:
        video_obj = Admin_video_obj(video.id, video.project_id, video.video_url, video.video_desc )
        videos_list.append(video_obj)

    #Retreive project photos
    photos_list: Admin_still_image_obj = [] # photos Object List
    all_project_photos = Still_photos.query.filter_by(project_id=project_id).all()

    for photo in all_project_photos:
        photo_obj = Admin_still_image_obj(photo.id, photo.project_id, photo.photo_url, photo.is_progression_photo, photo.photo_desc)
        photos_list.append(photo_obj)

    #Retreive project orthos
    orthos_list: Admin_ortho_obj = [] # orthos Object List
    all_project_orthos = Orthomosaics_2D.query.filter_by(project_id=project_id).all()

    for ortho in all_project_orthos:
        ortho_obj = Admin_ortho_obj(ortho.id, ortho.project_id, ortho.ortho_url, ortho.ortho_desc)
        orthos_list.append(ortho_obj)

    #Retreive Project Virtual Tour
    virtual_tours_list: Admin_virtual_tour_obj = [] # virtual Tours list
    all_project_tours = Virtual_tour_projects.query.filter_by(project_id=project_id).all()

    for tour in all_project_tours:
        virtual_tour_obj = Admin_virtual_tour_obj(tour.id, tour.project_id, tour.creation_date, tour.tour_desc)
        virtual_tours_list.append(virtual_tour_obj)

    #Retreive Virtual Tour Images
    virtual_tour_imgs_list: Admin_virtual_tour_img_obj = [] # virtual_tour_imgs list
    
    for tour in virtual_tours_list:
        all_project_tour_imgs = Virtual_tour_photos.query.filter_by(tour_id=tour.tour_id)
        for image in all_project_tour_imgs:
            virtual_tour_img_obj = Admin_virtual_tour_img_obj(image.id, image.tour_id, image.photo_url)
            virtual_tour_imgs_list.append(virtual_tour_img_obj)

    #Retreive Project 3D Models
    model_3d_objs_list: Admin_3dModel_obj = []
    all_project_models = Models_3d.query.filter_by(project_id=project_id).all()

    for model in all_project_models:
        model_obj = Admin_3dModel_obj(model.id, model.project_id, model.model_url, model.model_desc)
        model_3d_objs_list.append(model_obj)
    
    # Create Services Object Models
    current_project = Projects.query.filter_by(id=project_id).first()
    services_obj = Admin_project_services_obj(current_project.model_3d_service, current_project.virtual_tour_service, current_project.ortho_service, current_project.still_image_service, current_project.videography_service)

    # Create Admin_project_view_obj
    client_username = Clients.query.filter_by(id=current_project.client_id).first().username
    location = str

    if current_project.project_address != None:
        location = current_project.project_address
    else:
        location = current_project.project_tax_parcel

    admin_proj_view_obj = Admin_project_view_obj(current_project.client_id, client_username, current_project.creation_date, current_project.project_description, location, services_obj, model_3d_objs_list, all_project_tours, orthos_list, all_project_photos, all_project_videos)
        

    return render_template('admin_templates/admin_project_view.html', admin_proj_view_obj=admin_proj_view_obj)

@app.route('/update-asset-attributes', methods=['POST'])
def update_asset_attributes():
    json_data = request.json
    json_object = json.loads(json_data)
    print(json_object) # testing

    #check the type of asset to handle data
    if json_object['type_asset'] == 'model':
        try:
            if json_object['new_model_url']:
                #save new value to db
                #get asset id
                asset_id = json_object['asset_id']
                # Query the database to retrieve the record
                model_record = Models_3d.query.get(asset_id)
                # Check if record exists
                if model_record:
                    # Update url col if record exists
                    model_record.model_url = str(json_object['new_model_url'])

                    # Commit the changes to the database
                    db.session.commit()

                    print('saved url modificaion to model record.')
                else:
                    # Handle the case where the record does not exist
                    print('model record not found')
        except KeyError:
            print('new_model_url object key not included')

        try:
            if json_object['new_model_desc']:
                # get asset id
                asset_id = json_object['asset_id']
                # Query record
                model_record = Models_3d.query.get(asset_id)
                #check if record exists
                if model_record:
                    #Update desc col if record exists
                    model_record.model_desc = str(json_object['new_model_desc'])

                    #Commit the changes to the database
                    db.session.commit()
                print('new desc: ' + json_object['new_model_desc'])

        except KeyError:
            print('new_model_desc object key not included')

    #check for asset of type tour
    if json_object['type_asset'] == 'tour':
        try:
            if json_object['new_tour_desc']:
                # save new tour desc to db.
                asset_id = json_object['asset_id']
                # Query record
                tour_record = Virtual_tour_projects.query.get(asset_id)
                # check if record exist
                if tour_record:
                    #Update desc col if record exists
                    tour_record.tour_desc = str(json_object['new_tour_desc'])
                    #Commit changes to db
                    db.session.commit()
                    print('saved new tour desc ' + json_object['new_tour_desc'])
        except KeyError:
            print('new_tour_desc object key not included')

    # check for asset type of type ortho
    if json_object['type_asset'] == 'ortho':
        try:
            if json_object['new_ortho_url']:
                # save new ortho url to db
                asset_id = json_object['asset_id']
                # Query record
                ortho_record = Orthomosaics_2D.query.get(asset_id)
                #check if record exist
                if ortho_record:
                    #Update url col 
                    ortho_record.ortho_url = str(json_object['new_ortho_url'])
                    #Commit Changes to db
                    db.session.commit()
                    print('saved new ortho url ' + json_object['new_ortho_url'])
        except KeyError:
            print('new_ortho_url object key not included')
        
        try:
            if json_object['new_ortho_desc']:
                # save new ortho desc to db
                asset_id = json_object['asset_id']
                # Query record
                ortho_record = Orthomosaics_2D.query.get(asset_id)
                # check if record exist
                if ortho_record:
                    # Update desc col
                    ortho_record.ortho_desc = str(json_object['new_ortho_desc'])
                    #Commit Changes to db
                    db.session.commit()
        except KeyError:
            print('new_ortho_desc object key not included')

    # check for asset type of type still
    if json_object['type_asset'] == 'still':
        try:
            if json_object['new_still_url']:
                # save new still url to db
                asset_id = json_object['asset_id']
                # Query record
                still_record = Still_photos.query.get(asset_id)
                # check if record exist
                if still_record:
                    # Update url col
                    still_record.photo_url = str(json_object['new_still_url'])
                    # Commit Changes to db
                    db.session.commit()
        except KeyError:
            print('new_still_url object key not included')

        try:
            if json_object['new_still_desc']:
                # save new still desc to db
                asset_id = json_object['asset_id']
                # Query record
                still_record = Still_photos.query.get(asset_id)
                # check if record exist
                if still_record:
                    # Update desc col
                    still_record.photo_desc = str(json_object['new_still_desc'])
                    # Commit Changes to db
                    db.session.commit()
        except KeyError:
            print('new_still_desc object key not included')
    
    # check for asset type of video
    if json_object['type_asset'] == 'video':
        try:
            if json_object['new_video_url']:
                # save new video url to db
                asset_id = json_object['asset_id']
                # Query record
                video_record = Videos.query.get(asset_id)
                # check if record exist
                if video_record:
                    # Update url col
                    video_record.video_url = str(json_object['new_video_url'])
                    # Commit Changes to db
                    db.session.commit()
        except KeyError:
            print('new_video_url object key not included')
        try:
            if json_object['new_video_desc']:
                # save new video desc to db
                asset_id = json_object['asset_id']
                # Query record
                video_record = Videos.query.get(asset_id)
                # check if record exist
                if video_record:
                    # Update desc col
                    video_record.video_desc = str(json_object['new_video_desc'])
                    # Commit Changes to db
                    db.session.commit()
        except KeyError:
            print('new_video_desc object key not included')
            
    return jsonify(message="Saved Model Record to DB") # update this to a dynamic message

#SQL Database Setup

digital_ocean_cors_config = {
    "origins": ["https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com"]
}


cors= CORS(app, resources={r"/deliverables": {"origins": "https://high-altitude-media-assets.nyc3.cdn.digitaloceanspaces.com"}})

#Mail Setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER_NAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

#stripe setup
stripe.api_key = os.getenv('STRIPE_API_KEY') # Secret key create enviorment variable

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

@app.route('/get_model_data', methods=['GET'])
def get_data():
    return 'Hello'

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

# Payment Processor
'''
#Testing Stripe API
@app.route('/payment', methods=['GET'])
def Payment():
    #Get customers and print them out.
    customers = stripe.Customer.list()
    #emails = [Customer['email'] for customer in customers]
    #emails = stripe.Customer.data
    
    return jsonify(customers['data'][0]['email']), 200
'''

# Need to create a debug mode for backend testing
# this route takes in a query Paramerter for product ex. /page?product='product ID'
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
	# make condition if there is not a product ID
	productID = request.args.get('product')
	paymentMode = request.args.get('mode') # mode can only be subcription

	domain = 'www.high-altitude-media.com'

	if dev_testing_mode == True:
		domain = 'http://10.0.0.218:5000'

	url_success = domain + '/payment-success'
	url_cancel = domain + '/payment-cancled'


	print(paymentMode)
	try:
		session = stripe.checkout.Session.create(
			line_items=[
				{
				# provide Price ID (ex. pr_1234) of the product i want to sell
				"price": productID,
				"quantity": 1,
				},
			],
			mode= f'{paymentMode}',
			success_url= url_success,
			cancel_url= url_cancel,
			automatic_tax={'enabled': False},
		)

	except Exception as e:
		return str(e)
		
	return redirect(session.url, code=303)

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

# comment this line out before pushing code to server.
#app.run(debug=True)

#Run in debug mode while testing
if dev_testing_mode==True:
    app.run(debug=True)

if __name__ == '__main__':
    db.create_all() # Create database tables
    app.run()