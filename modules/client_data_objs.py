# dashboard helper objects
class Project:
    def __init__(self,project_id , description, project_date, project_url):
        self.project_id = project_id
        self.description = description
        self.project_date = project_date
        self.project_url = project_url

#Client_Virtual_Tours
class Client_Virtual_Tour_Obj:
    def __init__(self, tour_id, creation_date, tour_desc, tour_imgs):
        self.tour_id = tour_id
        self.creation_date = creation_date
        self.tour_desc = tour_desc
        self.tour_imgs = tour_imgs

#Client Tour Still Images Data Obj
class Client_Proj_Tour_Still_Obj:
    def __init__(self, tour_proj_id, tour_img_id, photo_url):
        self.tour_proj_id = tour_proj_id
        self.tour_img_id = tour_img_id
        self.photo_url = photo_url

#Client Model Asset Obj
class Client_Model_Asset_Obj:
    def __init__(self, model_id: int, model_url: str, model_desc: str):
        self.id = model_id
        self.model_url = model_url
        self. model_desc = model_desc
#Client Ortho Asset Obj
class Client_Ortho_Asset_Obj:
    def __init__(self, ortho_id: int, ortho_url: str, ortho_desc: str):
        self.ortho_id = ortho_id
        self.ortho_url = ortho_url
        self.ortho_desc = ortho_desc

#Client Video Asset Obj
class Client_Video_Asset_Obj:
    def __init__(self, video_id: int, video_url: str, video_desc: str):
        self.video_id = video_id
        self.video_url = video_url
        self.video_desc = video_desc

#Client Still Asset Obj
class Client_Still_Asset_Obj:
    def __init__(self, still_id: int, still_url: str, is_progression: bool, photo_desc: str):
        self.still_id = still_id
        self.still_url = still_url
        self.is_progression = is_progression
        self.photo_desc = photo_desc

# Services Offerings obj
class Client_Choosen_Services_obj:
    def __init__(self, stills_serv: bool, video_serv: bool, model_serv: bool, ortho_serv: bool, tour_serv: bool):
        self.stills_serv = stills_serv
        self.video_serv = video_serv
        self.model_serv = model_serv
        self.ortho_serv = ortho_serv
        self.tour_serv = tour_serv

# Project Progress obj
class Client_Project_Status_obj:
    def __init__(self, airspace_auth: bool, init_site_vist: bool, flight_plan_created: bool, data_collected: bool, data_processed: bool, deliverables_uploaded: bool):
        self.airspace_auth = airspace_auth
        self.init_site_vist = init_site_vist
        self.flight_plan_created = flight_plan_created
        self.data_collected = data_collected
        self.data_processed = data_processed
        self.deliverables_uploaded = deliverables_uploaded

#Project View Data Object
class Project_View:
    def __init__(self,description:str, date:str, project_location: str, virtual_tour_objs: list, project_model_objs: list, project_ortho_objs: list, project_video_objs: list, project_still_objs: list, client_services_obj:Client_Choosen_Services_obj, project_status_obj:Client_Project_Status_obj):
        self.description = description
        self.date = date
        self.project_location = project_location
        self.virtual_tour_objs = virtual_tour_objs
        self.project_model_objs = project_model_objs
        self.project_ortho_objs = project_ortho_objs
        self.project_video_objs = project_video_objs
        self.project_still_objs = project_still_objs
        self.client_services_obj = client_services_obj
        self.project_status_obj = project_status_obj