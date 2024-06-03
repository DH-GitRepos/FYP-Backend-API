import os
import shutil


class LibraryManager:
    def __init__(self, logging_manager, database_interface):
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.LIBRARY_INDEX_FOLDER = f"{self.FILE_PATH}\\..\\library\\"
        self.LIBRARY_DETECTION_DATA_FOLDER = f"{self.LIBRARY_INDEX_FOLDER}data\\"
        self.LIBRARY_IMAGES_FOLDER = f"{self.LIBRARY_INDEX_FOLDER}images\\"
        self.UPLOADS_FOLDER = f"{self.FILE_PATH}\\..\\uploads\\"
        self.LIBRARY_INDEX_PATH = f"{self.LIBRARY_INDEX_FOLDER}library_index.json"
        self.LOG_MGR = logging_manager
        self.DBI = database_interface
     
    
    def save_uploaded_file_data(self, data):
        self.LOG_MGR.log(f"LIBRARY_MANAGER(save_uploaded_file_data): Incoming data:\n\tDATA: {data}")
                
        self.DBI.insert_uploaded_image_data(data)
        
        self.LOG_MGR.log(f"\tRETURNING(save_uploaded_file_data) -> TRUE\n")
        return True
    
    
    def insert_tagged_face_to_library_image(self, timestamp, face_id, uid):
        self.LOG_MGR.log(f"LIBRARY_MANAGER(insert_tagged_face_to_library_image): Incoming data:\n\tTIMESTAMP: {timestamp}, FACE ID: {face_id}, UID: {uid}")
        
        self.DBI.insert_tagged_face_to_library_image(timestamp, face_id, uid)
        
        self.LOG_MGR.log(f"\tRETURNING(insert_tagged_face_to_library_image) -> TRUE\n")
        return True
        
        
    def update_image_tagged_value(self, timestamp, tagged_value):
        self.LOG_MGR.log(f"LIBRARY_MANAGER(update_image_tagged_value): Incoming data:\n\tTIMESTAMP: {timestamp}, TAGGED VALUE: {tagged_value}")
        
        self.DBI.update_image_tagged_value(timestamp, tagged_value)
        
        self.LOG_MGR.log(f"\tRETURNING(update_image_tagged_value) -> TRUE\n")
        return True
        

    def move_upload_to_library(self, timestamp):
        self.LOG_MGR.log(f"LIBRARY_MANAGER(move_upload_to_library): Incoming data:\n\tTIMESTAMP: {timestamp}")
        
        img_filename = f"{timestamp}.jpg"
        img_file_src = f"{self.UPLOADS_FOLDER}{img_filename}"
        img_file_target = f"{self.LIBRARY_IMAGES_FOLDER}{img_filename}"
        shutil.move(img_file_src, img_file_target)
        
        new_library_index_object = {
            "img_name": timestamp,
            "tagged": False,        
            "tagged_faces": []
        }    
        
        self.add_to_library_index(False, new_library_index_object)
        
        self.LOG_MGR.log(f"\tRETURNING(move_upload_to_library) -> TRUE\n")
        return True
    
 
    def add_to_library_index(self, tagged, new_img_obj):
        self.LOG_MGR.log(f"LIBRARY_MANAGER(add_to_library_index): Incoming data:\n\tTAGGED VALUE: {tagged}, IMG OBJ: {new_img_obj}")
        
        image_added_to_library_index = False
        
        image_exists_check = self.DBI.get_image_by_timestamp(new_img_obj['img_name'])
        self.LOG_MGR.log(f"\tLIBRARY_MANAGER(add_to_library_index) -> IMG CHECK {image_exists_check}.\n")    
        
        tagged_value = 0
        if tagged:          
            tagged_value = 1
        
        if image_exists_check['num_rows'] == 0:
            self.DBI.insert_image_to_library(new_img_obj['img_name'], tagged_value)
            image_added_to_library_index = True
            self.LOG_MGR.log(f"\tLIBRARY_MANAGER(add_to_library_index) -> Image added to DB library index.\n")
        
        if not image_added_to_library_index:
            self.LOG_MGR.log(f"\tLIBRARY_MANAGER(add_to_library_index) -> Image already exists in DB library index, not added.\n")
        
        self.LOG_MGR.log(f"\tRETURNING(add_to_library_index) -> TRUE\n")
        return True


    def get_all_images(self):
        self.LOG_MGR.log(f"LIBRARY_MANAGER(get_all_images)")   
        
        list_of_images = self.DBI.get_all_images_from_library()
        
        image_list = []
        
        for img in list_of_images['rows']:
            image_list.append(img[0])
                
        self.LOG_MGR.log(f"\tRETURNING(get_all_images) -> IMAGE LIST: {image_list}\n")       
        return image_list


    def get_images_by_uid(self, uid):
        self.LOG_MGR.log(f"LIBRARY_MANAGER(get_images_by_uid)")
        
        list_of_images_data = self.DBI.get_all_tagged_images_from_library_by_uid(uid)
        
        image_list = []
        
        for img in list_of_images_data['rows']:
            image_list.append(img[0])
        
        self.LOG_MGR.log(f"\tRETURNING(get_images_by_uid) -> IMAGE LIST: {image_list}\n")       
        return image_list


    def get_all_tagged_faces_by_image_timestamp(self, image_id):
        self.LOG_MGR.log(f"LIBRARY_MANAGER(get_all_tagged_faces_by_image_timestamp): Incoming data:\n\tIMAGE ID: {image_id}")
        
        tagged_faces_data = self.DBI.get_all_tagged_faces_by_image_timestamp(image_id)
        
        self.LOG_MGR.log(f"\tRETURNING(get_all_tagged_faces_by_image_timestamp) -> TAGGED FACES DATA: {tagged_faces_data}\n")       
        return tagged_faces_data


    def check_tagged_values(self):
        self.LOG_MGR.log(f"\nLIBRARY_MANAGER(check_tagged_values)")
        
        # get list of image ids
        image_list_data = self.DBI.get_all_images_from_library()
        
        if image_list_data['num_rows'] == 0:
            self.LOG_MGR.log(f"\nRETURNING(check_tagged_values) -> False (No rows to process)")
            return False            
        else:
            self.LOG_MGR.log(f"LIBRARY_MANAGER(check_tagged_values): Image list data: {image_list_data['rows']}")
            
            # for each image id
            for img in image_list_data['rows']:
                img_id = img[0]
                self.LOG_MGR.log(f"LIBRARY_MANAGER(check_tagged_values): Current image: {img_id}")

                # check tagged list for profile id
                image_is_tagged_data = self.DBI.get_tagged_image_by_timestamp(img_id)
                
                # if profile id in tagged list
                if image_is_tagged_data['num_rows'] == 0:
                    self.DBI.update_image_tagged_value(img_id, 0)
                else:
                    # set tagged value to true
                    self.DBI.update_image_tagged_value(img_id, 1)
                    
            self.LOG_MGR.log(f"\nRETURNING(check_tagged_values) -> True (Rows processed)")
            return True
