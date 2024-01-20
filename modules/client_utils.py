from modules.client_data_objs import Project, Client_Virtual_Tour_Obj, Client_Proj_Tour_Still_Obj, Client_Model_Asset_Obj, Client_Ortho_Asset_Obj, Client_Video_Asset_Obj, Client_Still_Asset_Obj, Client_Choosen_Services_obj, Client_Project_Status_obj, Project_View
from modules.db_schemas import db, Clients, Projects, Site_admin, Models_3d, Virtual_tour_projects, Virtual_tour_photos, Orthomosaics_2D, Still_photos, Videos


#dash board data obj
class dash_board_data_obj:
    def __init__(self, projects: list[Project] ,username: str, email: str, phone_number: str, company: str):
        self.projects: list[Project] = projects
        self.username: str = username
        self.email: str = email
        self.phone_number: str = phone_number
        self.company: str = company
        

# Client Dashboard
def get_client_dashboard_data(current_user) -> dash_board_data_obj :
    #Create routes and pages to update individual fields
    username = current_user.username
    email = current_user.email
    phone_number = current_user.phone_number
    company = current_user.company

    # load projects
    current_user_projects = Projects.query.filter_by(client_id=current_user.id).all()
    project_count = len(current_user_projects)

    project_index: int = 0

    project_objects: list[Project] = []

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

    dash_board_data = dash_board_data_obj(project_objects, username, email, phone_number, company)
    return dash_board_data


# Client Project View
def get_client_project_data(project_id) -> Project_View:
    #task: validate user access by checking project client id and current logged in user id.
    current_project = Projects.query.filter_by(id=project_id).first()

    #Get Project Data
    description  = str(current_project.project_description)
    date = str(current_project.creation_date)
    project_location = str()
    project_address = str(current_project.project_address)
    project_tax_parcel = str(current_project.project_tax_parcel)

    # Do additional checks for project services and gather data for client assets ids.
    project_services_obj = Client_Choosen_Services_obj(current_project.still_image_service,current_project.videography_service, current_project.model_3d_service, current_project.ortho_service, current_project.virtual_tour_service)
    project_status_obj = Client_Project_Status_obj(current_project.airspace_authorization, current_project.intial_site_visit, current_project.flight_plan_created, current_project.data_collected, current_project.data_processed, current_project.deliverables_uploaded)

    #Get address type and set project location var
    if len(project_address) == 0 and len(project_tax_parcel) == 0:
        project_location = 'None'
    elif len(project_address) == 0 and len(project_tax_parcel) != 0:
        project_location = str(project_tax_parcel)
    elif len(project_address) != 0 and len(project_tax_parcel) == 0:
        project_location = project_address
        print(f'project location: {project_location}')

    

    #Get All Project Assets
    project_models = Models_3d.query.filter_by(project_id=project_id).all()
    project_videos = Videos.query.filter_by(project_id=project_id).all()
    project_stills = Still_photos.query.filter_by(project_id=project_id).all()
    project_orthos = Orthomosaics_2D.query.filter_by(project_id=project_id).all()
    project_tour_projects = Virtual_tour_projects.query.filter_by(project_id=project_id).all()

    #Virtual tour Objects List
    virtual_tour_objs = []
    project_model_objs = []
    project_ortho_objs = []
    project_video_objs = []
    project_still_objs = []

    # get all  tour images  and virtual tour
    # array of objects contains Virtual_Tour_Proj id, tour_img_id, photos_url
    for tour_project in project_tour_projects:
        #get tour project
        tour_projs = Virtual_tour_projects.query.filter_by(project_id=project_id).all()
        tour_objs = [] # holds all the tour objs for given tour
        #print('Tour Project ID : ' + str(tour_project.id) + ' Photos in tour: ' +  str(len(tour_photos)))
        # for tour in tour_projs:
        #     #Create Still Photo OBJ
        #     tour_obj = Client_Proj_Tour_Still_Obj(photo.tour_id, photo.id, photo.photo_url)
        #     tour_objs.append(tour_obj)
        #     #print(f'Photo ID: {photo.id} Photo URL: {photo.photo_url}')

        # Create Tour Project Obj - contains virtual tour info and an array of tour photo objs. Add this to the Client_Proj_View Obj
        tour_proj_obj = Client_Virtual_Tour_Obj(tour_project.id,tour_project.creation_date, tour_project.tour_desc, tour_project.tour_url)
        virtual_tour_objs.append(tour_proj_obj)

    # Get all 3D Model Assets and create OBJs
    for model in project_models:
        #Create Model Obj and append to project models list 
        model_obj = Client_Model_Asset_Obj(model.id, model.model_url, model.model_desc)
        project_model_objs.append(model_obj)

    # Get all Ortho Assets
    for ortho in project_orthos:
        ortho_obj = Client_Ortho_Asset_Obj(ortho.id,ortho.ortho_url,ortho.ortho_desc)
        project_ortho_objs.append(ortho_obj)

    # Get all Video Assets
    for video in project_videos:
        video_obj = Client_Video_Asset_Obj(video.id, video.video_url, video.video_desc)
        project_video_objs.append(video_obj)

    # Get all Still Assets
    for still in project_stills:
        still_obj = Client_Still_Asset_Obj(still.id, still.photo_url, still.is_progression_photo, still.photo_desc)
        project_still_objs.append(still_obj)

    #Create Project data object
    project_view_data = Project_View(description,date, project_location,virtual_tour_objs, project_model_objs,project_ortho_objs,project_video_objs,project_still_objs,project_services_obj, project_status_obj)
    return project_view_data

# Client new project
def create_client_project(json_object: dict, client_id, current_date):
    
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