#Admin Client Projects View Data Object
class Client_Project_obj:
    def __init__(self,project_id, date, location, project_url, client_id, client_username):
        self.project_id = project_id
        self.date = date
        self.location = location
        self.project_url = project_url
        self.client_id = client_id
        self.client_username = client_username

#Admin Dashboard Clients obj
class Admin_Client_obj:
    def __init__(self, username, email, user_id):
        self.username = username
        self.email = email
        self.user_id = user_id

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
    def __init__(self, tour_id: int, project_id: int, date: str, tour_desc: str, tour_url: str):
        self.tour_id: int = tour_id
        self.project_id: int = project_id
        self.date: str = date
        self.tour_desc: str = tour_desc
        self.tour_url: str = tour_url

#Admin Tour Image Object - remove later no longer storing individual images
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