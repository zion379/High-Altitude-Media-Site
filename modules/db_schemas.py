from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import relationship

db = SQLAlchemy()

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
    data_processed = db.Column(db.Boolean, default=False)
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
    tour_desc = db.Column(db.Text, nullable=True)
    tour_url = db.Column(db.Text, nullable=True)

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
