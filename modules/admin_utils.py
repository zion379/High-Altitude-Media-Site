from modules.db_schemas import db, Clients, Projects, Site_admin, Models_3d, Virtual_tour_projects, Virtual_tour_photos, Orthomosaics_2D, Still_photos, Videos
from modules.admin_data_objs import Client_Project_obj, Admin_Client_obj, Admin_project_services_obj, Admin_3dModel_obj, Admin_virtual_tour_obj, Admin_virtual_tour_img_obj, Admin_ortho_obj, Admin_still_image_obj, Admin_video_obj, Admin_project_view_obj

class Admin_dash_data():
    def __init__ (self, projects_data_obj: list, all_clients_obj: list):
        self.projects_data_obj = projects_data_obj
        self.all_clients_obj = all_clients_obj


def get_admin_dash_projects() -> Admin_dash_data:
    all_client_projects = Projects.query.all()
    total_projects = len(all_client_projects)
    project_index = 0

    projects_data_objects = []

    #Check if any projects exist
    if total_projects != 0 :
        #display all client projects
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

    #Get all clients for Project Creation Data Field
    all_clients = Clients.query.all()
    admin_clients_obj = []

    #Check if there are any clients
    if len(all_clients) != 0:
        for client_record in all_clients:
            #Create client object and append it to array
            client = Admin_Client_obj(client_record.username, client_record.email, client_record.id) # return to this, delete this comment
            admin_clients_obj.append(client)
    
    data = Admin_dash_data(projects_data_objects,admin_clients_obj)

    return data

def get_admin_project_view_data(project_id) -> Admin_project_view_obj:
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
        virtual_tour_obj = Admin_virtual_tour_obj(tour.id, tour.project_id, tour.creation_date, tour.tour_desc, tour.tour_url)
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
    return admin_proj_view_obj

def admin_update_asset_attributes(json_object: dict):
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
        try: # check for tour desc
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

        try: # check for tour url
            if json_object['new_tour_url']:
                # save new tour url to db
                asset_id = json_object['asset_id']
                #query record
                tour_record = Virtual_tour_projects.query.get(asset_id)
                # check if record exist
                if tour_record: #Update url col if record exists
                    tour_record.tour_url = str(json_object['new_tour_url'])
                    #Commit changes to db
                    db.session.commit()
                    print('saved new tour url ' + json_object['new_tour_url'])
        except KeyError:
            print('new_tour_url object key not included')

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

# create new asset
def admin_create_new_asset(json_data: dict):
    asset_project_id = json_data['project_id']
    asset_type = json_data['asset_type']
    asset_url = json_data['asset_url']
    asset_desc = json_data['asset_desc']

    # check what type the new asset is
    if asset_type == 'model':
        #create new model instance
        new_model_asset = Models_3d(project_id=asset_project_id, model_url=asset_url, model_desc=asset_desc)
        #Add Asset Record to db session
        db.session.add(new_model_asset)
        # Commit the sesion to save data
        db.session.commit()
        print('Created new Model Asset')

    elif asset_type == 'tour':
        current_date = datetime.now().date()
        #create new tour instance
        new_tour_asset = Virtual_tour_projects(creation_date=current_date,tour_desc=asset_desc, project_id=asset_project_id)
        #Add Asset Record to db session
        db.session.add(new_tour_asset)
        # Commit session
        db.session.commit()
        print('Created new Model Asset')
    elif asset_type == 'ortho':
        #create new ortho instance
        new_ortho_asset = Orthomosaics_2D(project_id=asset_project_id, ortho_url=asset_url, ortho_desc=asset_desc)
        #Add asset record to db session
        db.session.add(new_ortho_asset)
        #Commit session
        db.session.commit()
        print('Created new Ortho Asset')
    elif asset_type == 'still':
        #create new still instance
        new_still_asset = Still_photos(project_id=asset_project_id, photo_url=asset_url, photo_desc=asset_desc)
        #Add asset record to db session
        db.session.add(new_still_asset)
        #Commit session
        db.session.commit()
        print('Created new Still Image Asset')
    elif asset_type == 'video':
        # create new video instance
        new_video_asset = Videos(project_id=asset_project_id, video_url=asset_url, video_desc=asset_desc)
        #Add asset record to db session
        db.session.add(new_video_asset)
        #Commit session
        db.session.commit()
        print('Created new Video Asset')

def admin_del_project_asset(json_data: dict):
    project_id = json_data['project_id']
    asset_type = json_data['asset_type']
    asset_id = json_data['asset_id']

    if asset_type == 'model':
        # delete model asset
        model_record = Models_3d.query.get(asset_id)

        #check if record exist
        if model_record:
            db.session.delete(model_record)
            db.session.commit()

        print('delete model asset ')
    elif asset_type == 'tour':
        #delete tour asset
        tour_record = Virtual_tour_projects.query.get(asset_id)

        #check if record exist
        if tour_record:
            db.session.delete(tour_record)
            db.session.commit()

        print('delete tour asset ')
    elif asset_type == 'ortho':
        #delete ortho asset
        ortho_record = Orthomosaics_2D.query.get(asset_id)

        #check if record exist
        if ortho_record:
            db.session.delete(ortho_record)
            db.session.commit()

        print('delete ortho asset ' + json_data)
    elif asset_type == 'still':
        #delete still asset
        still_record = Still_photos.query.get(asset_id)

        #check if record exist
        if still_record:
            db.session.delete(still_record)
            db.session.commit()

        print('delete still asset ' + json_data)
    elif asset_type == 'video':
        #delete video asset
        video_record = Videos.query.get(asset_id)

        #check if record exist
        if video_record:
            db.session.delete(video_record)
            db.session.commit()

        print('delete video asset ' + json_data)


def admin_create_new_project(json_data: dict):
    # Get attributes
    client_id = json_data['client_id']
    address_type = json_data['address_type']
    location = json_data['location']
    proj_desc = json_data['proj_desc']
    creation_date = datetime.now().date()

    # create new project instance
    if address_type == 'tax_parcel':
        new_client_project = Projects(client_id=client_id, project_tax_parcel=location, project_description=proj_desc, creation_date=creation_date)
        db.session.add(new_client_project)
        db.session.commit()
    else:
        new_client_project = Projects(client_id=client_id, project_address=location, project_description=proj_desc, creation_date=creation_date)
        db.session.add(new_client_project)
        db.session.commit()

def admin_delete_proj(json_data):
    project_id = json_data['project_id']

    # delete all project assets: project, stills, videos, orthos, models, virtual tours,  tour-360s
    proj_stills = Still_photos.query.filter_by(project_id=project_id).all()

    #Check if stills is null
    if proj_stills:
        for img in proj_stills:
            #delete image record
            db.session.delete(img)

    proj_videos = Videos.query.filter_by(project_id=project_id).all()

    #Check if there are any videos
    if proj_videos:
        for video in proj_videos:
            #delete video record
            db.session.delete(video)

    proj_orthos = Orthomosaics_2D.query.filter_by(project_id=project_id).all()

    if proj_orthos:
        for ortho in proj_orthos:
            # delete ortho record
            db.session.delete(ortho)

    proj_models = Models_3d.query.filter_by(project_id=project_id).all()

    if proj_models:
        for model in proj_models:
            # delete model record
            db.session.delete(model)

    proj_tours = Virtual_tour_projects.query.filter_by(project_id=project_id).all()

    if proj_tours:
        for tour in proj_tours:
            # delete all tour photos
            tour_360_imgs = Virtual_tour_photos.query.filter_by(tour_id=tour.id)

            #check if there are any imgs
            if tour_360_imgs:
                for img_360 in tour_360_imgs:
                    # delete image
                    db.session.delete(img_360)

            # delete tour
            db.session.delete(tour)
            print(tour.tour_desc)

    # Delete Project
    current_proj = Projects.query.filter_by(id=project_id).first()
    db.session.delete(current_proj)
    
    db.session.commit()