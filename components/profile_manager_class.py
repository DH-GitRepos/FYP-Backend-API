# profile_manager_class.py -- version 3.0

import os
import uuid
import pickle
import shutil
import json
# from databaseGateway.IDatabaseGatewayFacade import IDatabaseGatewayFacade


class ProfileManager:
    def __init__(self, logging_manager, mapper_manager, library_manager, data_manager, database_interface):
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.TMP_DATA_PATH = f"{self.FILE_PATH}\\..\\profiles\\tmp\\"
        self.PROFILE_INDEX_FOLDER = f"{self.FILE_PATH}\\..\\profiles\\people\\"
        self.PROFILE_INDEX_PATH = f"{self.PROFILE_INDEX_FOLDER}profile_index.json"
        
        self.LOG_MGR = logging_manager
        self.MAP_MGR = mapper_manager        
        self.LIB_MGR = library_manager
        self.DATA_MGR = data_manager
        self.FRDB_MGR = None
        self.DBI = database_interface


    # To solve circular initialisation dependency with FRDBManager    
    def set_frdb_mgr(self, frdb_mgr):
        self.FRDB_MGR = frdb_mgr
       
       
    def get_all_profile_uids(self):
        self.LOG_MGR.log(f"PROFILE_MANAGER(get_all_profile_uids)")
        
        profile_index_result = self.DBI.get_all_profile_uids()
        
        self.LOG_MGR.log(f"\tRETURNING(get_all_profile_uids) -> PROFILE INDEX: {profile_index_result}\n")
        return profile_index_result
               

    def move_tagged_face_to_tmp(self, src, profile_uid):
        move_file_from_path = f"{self.PROFILE_INDEX_FOLDER}{profile_uid}\\img\\{src}.jpg"
        move_file_to_path = f"{self.TMP_DATA_PATH}{src}.jpg"
        shutil.move(move_file_from_path, move_file_to_path)        
        return True
    
    
    def move_tmp_to_profile(self, src, profile_uid):
        if not os.path.exists(f"{self.PROFILE_INDEX_FOLDER}{profile_uid}"):
            self.create_user_profile_store_location(profile_uid)
        
        move_file_from_path = f"{self.TMP_DATA_PATH}{src}.jpg"
        move_file_to_path = f"{self.PROFILE_INDEX_FOLDER}{profile_uid}\\img\\{src}.jpg"
        shutil.move(move_file_from_path, move_file_to_path)        
        return True
    

    def get_master_profile_data_by_uid(self, uid):
        self.LOG_MGR.log(f"PROFILE_MANAGER(get_master_profile_data_by_uid): Incoming data:\n\tUID: {uid}")
        
        face_profiles_path = f"{self.PROFILE_INDEX_FOLDER}{uid}\\profile\\{uid}.pkl"
        profile_data = self.DATA_MGR.get_dataFile(face_profiles_path)
        
        self.LOG_MGR.log(f"\tRETURNING(get_master_profile_data_by_uid) -> PROFILE DATA: {profile_data}\n")
        return profile_data


    def update_master_profile_data_by_uid(self, uid, data):
        self.LOG_MGR.log(f"PROFILE_MANAGER(update_master_profile_data_by_uid): Updating master profile data for {uid}...")
        
        face_profiles_path = f"{self.PROFILE_INDEX_FOLDER}{uid}\\profile\\{uid}.pkl"
        
        master_profile = self.DATA_MGR.get_dataFile(face_profiles_path)
        master_profile['face_data'] = data
        
        save_face_profiles_path = f"{self.PROFILE_INDEX_FOLDER}{uid}\\profile\\{uid}"
        
        self.DATA_MGR.store_profileData(save_face_profiles_path, master_profile)    
        
        self.LOG_MGR.log(f"\tRETURNING(update_master_profile_data_by_uid) -> TRUE\n")
        return True


    def create_new_profile_from_temp_data(self, timestamp, face_id, name):
        self.LOG_MGR.log(f"PROFILE_MANAGER(createNewProfileFromTempData): Creating new profile for {name} with face ID: {face_id}")
        
        # - get the uid by src from the db (tmp_profile table)
        full_filename = f"{timestamp}-{face_id}"
        temp_profile = self.DBI.get_tmp_uid_by_src(full_filename)
        
        self.LOG_MGR.log(f"PROFILE_MANAGER(createNewProfileFromTempData): QUERY RETURNED: {temp_profile}")
        
        tmp_profile_uid = None
        
        if temp_profile['num_rows'] > 0:
            temp_profile_data = temp_profile['rows'][0]
            temp_profile_uid = temp_profile_data[1]
        else:
            temp_profile_uid = self.DATA_MGR.create_uuid()
        
        # - create store location for the new profile with uid
        self.create_user_profile_store_location(temp_profile_uid)
        
        # - move the temp files to the new profile location
        tmp_img_filename = f"{full_filename}.jpg"
        self.relocate_temp_files(tmp_img_filename, temp_profile_uid)
                
        # - create a new DB entry for the new profile
        self.DBI.insert_new_profile_to_index(temp_profile_uid)
        
        # - add mapper data for the new profile
        self.DBI.insert_new_name_to_mapper(name, temp_profile_uid)
        
        # - remove the tmp profile entry from the db
        self.DBI.remove_temp_profile_by_uid(temp_profile_uid)
        
        # - add tagged face entry agaist the image
        self.DBI.insert_tagged_face_to_library_image(timestamp, face_id, temp_profile_uid)       
        
        # - update the main image library 'tagged' value to '1'
        self.DBI.update_image_tagged_value(timestamp, 1)
            
        self.LOG_MGR.log(f"\tRETURNING(createNewProfileFromTempData) -> TRUE\n")
        return temp_profile_uid


    def update_profile_with_temp_data(self, timestamp, face_id, name, existing_uuid):
        self.LOG_MGR.log(f"PROFILE_MANAGER(updateProfileWithTempData): Merging new data with profile ID: {existing_uuid} ({name})")

        # - Move the tmp image to the existing profile folder
        full_filename = f"{timestamp}-{face_id}"
        tmp_img_filename = f"{full_filename}.jpg"
        # tmpImg_path = f"{self.FILE_PATH}\\..\\profiles\\tmp\\"
        self.relocate_temp_files(tmp_img_filename, existing_uuid)
        
        # - add tagged face entry agaist the image
        self.DBI.insert_tagged_face_to_library_image(timestamp, face_id, existing_uuid) 
        
        # - update the main image library 'tagged' value to '1'
        self.DBI.update_image_tagged_value(full_filename, 1)
        
        # - remove the tmp profile entry from the db
        self.DBI.remove_temp_profile_by_src(full_filename)
             
        self.LOG_MGR.log(f"\tRETURNING(updateProfileWithTempData) -> TRUE\n")
        return True


    def create_user_profile_store_location(self, userID):
        self.LOG_MGR.log(f"PROFILE_MANAGER(createUserProfileStoreLocation): Incoming data:\n\tUSER ID: {userID}")
        
        face_profile_path = f"{self.PROFILE_INDEX_FOLDER}{userID}\\"
        if not os.path.exists(face_profile_path):
            os.makedirs(face_profile_path)

        face_profile_img_path = f"{self.PROFILE_INDEX_FOLDER}{userID}\\img\\"
        if not os.path.exists(face_profile_img_path):
            os.makedirs(face_profile_img_path)
            
        self.LOG_MGR.log(f"\tRETURNING(createUserProfileStoreLocation) -> FACE PROFILE PATH: {face_profile_path}\n")    
        return face_profile_path


    def get_existing_user_profile_store_location(self, userID):
        self.LOG_MGR.log(f"PROFILE_MANAGER(getExistingUserProfileStoreLocation): Incoming data:\n\tUSER ID: {userID}")
        
        face_profile_path = f"{self.FILE_PATH}\\..\\profiles\\people\\{userID}\\"
        
        self.LOG_MGR.log(f"\tRETURNING(getExistingUserProfileStoreLocation) -> FACE PROFILE PATH: {face_profile_path}\n")
        return face_profile_path
        

    def store_profile_data(self, face_profiles_path, face_profile):
        self.LOG_MGR.log(f"PROFILE_MANAGER(storeProfileData): Incoming data:\n\tFACE PROFILE PATH: {face_profiles_path}\n\tFACE PROFILE: {face_profile}")
        profile_path = f"{face_profiles_path}\\profile\\"
        
        # Store the profile data
        with open(f"{profile_path}{face_profile['face_id']}.pkl", 'wb') as f:
            f.write(pickle.dumps(face_profile))
        
        self.LOG_MGR.log(f"\tRETURNING(storeProfileData) -> TRUE\n")    
        return True


    def relocate_temp_files(self, tmp_img_filename, target_uid):
        self.LOG_MGR.log(f"PROFILE_MANAGER(relocateTempFiles): Incoming data:\n\tIMG FILENAME: {tmp_img_filename}\n\tUSER ID: {target_uid}")
        
        self.LOG_MGR.log(f"\tPROFILE_MANAGER(relocateTempFiles): tmp img filename: {tmp_img_filename}")
        imgTmp_path_src = f"{self.TMP_DATA_PATH}{tmp_img_filename}"    
        
        imgTmp_path_target = f"{self.PROFILE_INDEX_FOLDER}{target_uid}\\img\\{tmp_img_filename}"
        
        if os.path.exists(imgTmp_path_src):    
            # Move the temp image file to the user profile folder
            shutil.move(imgTmp_path_src, imgTmp_path_target)
        else:
            self.LOG_MGR.log(f"\tPROFILE_MANAGER(relocateTempFiles): Image file ({imgTmp_path_src}) not found, skipping... ")
        
        self.LOG_MGR.log(f"\tRETURNING(relocateTempFiles) -> TRUE\n")
        return True


    def get_all_images_for_profile(self, uid):
        self.LOG_MGR.log(f"PROFILE_MANAGER(get_all_images_for_profile): Incoming data: {uid}")

        profile_img_path = f"{self.PROFILE_INDEX_FOLDER}{uid}\\img\\"
        image_files = [f for f in os.listdir(profile_img_path) if f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.jpeg') or f.endswith('.JPEG') or f.endswith('.png') or f.endswith('.PNG')]
        
        self.LOG_MGR.log(f"\tRETURNING(get_all_images_for_profile) -> FACE DATA: {image_files}\n")
        return image_files


    def get_all_profile_images(self):
        self.LOG_MGR.log(f"PROFILE_MANAGER(get_all_profile_images)")
        
        profile_index_result = self.DBI.get_all_profile_uids()
        profile_index = profile_index_result['rows']
        
        self.LOG_MGR.log(f"PROFILE_MANAGER(get_all_profile_images): PROFILE INDEX: {profile_index}")
        
        image_dict = []
        
        for item in profile_index:
            uid_obj = { 
                    "uid" : item[1],
                    "img_paths": self.get_all_images_for_profile(item[1]),
                    }
            image_dict.append(uid_obj)
            
        # update images to full paths
        for item in image_dict:
            
            current_uid = item['uid']
            
            old_paths = item['img_paths']
            new_paths = []
            
            for path in old_paths:
                new_path = f"{self.PROFILE_INDEX_FOLDER}{current_uid}\\img\\{path}"
                new_paths.append(new_path)
            
            item['img_paths'] = new_paths

        self.LOG_MGR.log(f"\tRETURNING(get_all_profile_images) -> PROFILE IMAGE PATHS: {image_dict}\n")
        return image_dict


    def get_all_tmp_images_by_timestamp(self, timestamp):
        self.LOG_MGR.log(f"PROFILE_MANAGER(get_all_tmp_images_by_timestamp): Incoming data: {timestamp}")
        
        image_dict = []
        
        image_files = [f for f in os.listdir(self.TMP_DATA_PATH) if f.startswith(timestamp) and (f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.jpeg') or f.endswith('.JPEG') or f.endswith('.png') or f.endswith('.PNG'))]
        
        # update images to full paths
        for i in range(len(image_files)):
            
            tmp_img_obj = {
                "uid": None,
                "img_path": None,
                "img_src": None
            }        
            
            # set the image path in the tmp_img_obj
            path = f"{self.TMP_DATA_PATH}{image_files[i]}"    
            tmp_img_obj["img_path"] = path 
            
            # set the image src in the tmp_img_obj
            src_ext = image_files[i]
            src_no_ext, _ = os.path.splitext(src_ext)
            tmp_img_obj["img_src"] = src_no_ext
            
            # set the image uid in the tmp_img_obj
            uid = None
            
            result = self.DBI.get_tmp_uid_by_src(src_no_ext)
            uid = result['rows'][0][1]
            
            tmp_img_obj["uid"] = uid
            
            # add the tmp_img_obj to the image_dict
            image_dict.append(tmp_img_obj)
        
        self.LOG_MGR.log(f"\tRETURNING(get_all_tmp_images_by_timestamp) -> TMP IMAGE PATHS: {image_dict}\n")
        return image_dict   


    def check_incoming_tags_match_pre_tags(self, upload_data):
        self.LOG_MGR.log(f"PROFILE_MANAGER(check_incoming_tags_match_pre_tags): Incoming data {upload_data}...")
        
        profile_restored_staus = False
            
        incoming_timestamp = upload_data['tsp']
        incoming_face_tags = upload_data['faces']
    
        for tag in incoming_face_tags:
            id = tag['id']
            name = tag['name']
            uid = tag['uid']                
            profile_id = f"{incoming_timestamp}-{id}"
            checkbox = tag['checkbox']
        
            if checkbox == "on":
                self.LOG_MGR.log(f"\tPROFILE_MANAGER(check_incoming_tags_match_pre_tags):\n\tChecking face id {profile_id}...")
                
                found_name = self.find_person_by_profile_id(profile_id)
                
                self.LOG_MGR.log(f"\tPROFILE_MANAGER(check_incoming_tags_match_pre_tags):\n\tFOUND-NAME for '{profile_id}': {found_name}")
                
                if found_name['found']:
                    if not found_name['name'] == name:
                        self.LOG_MGR.log(f"\tPROFILE_MANAGER(check_incoming_tags_match_pre_tags):\n\tNAME MISMATCH:\n\tPre-tagged as {found_name['name']} but incoming as '{name}'...")
                        
                        # Get existing tag data
                        existing_tag_data = self.DBI.get_tagged_face_data_by_timestamp_and_UID(incoming_timestamp, uid)
                        existing_face_id = existing_tag_data['rows'][0][2]
                                                                    
                        # Correct the tagging actions
                        self.restore_incorrectly_tagged_image(profile_id, found_name['uid'], found_name['file_path'], name)
                        new_uid = self.create_new_profile_from_temp_data(incoming_timestamp, id, name)
                        uid_to_add_list = []
                        uid_to_add_list.append(new_uid)
                        
                        # Remove incorrect tag data from image
                        self.DBI.remove_profile_from_image(incoming_timestamp, existing_face_id, uid)
                        
                        profile_restored_staus = True
                    else:
                        self.LOG_MGR.log(f"\tPROFILE_MANAGER(check_incoming_tags_match_pre_tags):\n\tNAME MATCH:\n\tPre-tagged as {found_name['name']} and incoming as '{name}'...")
                        profile_restored_staus = False
                        
        self.LOG_MGR.log(f"\tRETURNING(check_incoming_tags_match_pre_tags) -> PROFILE RESTORED: {profile_restored_staus}\n")            
        return profile_restored_staus

        
    def find_person_by_profile_id(self, profile_id):
        self.LOG_MGR.log(f"PROFILE_MANAGER(find_person_by_profile_id): Incoming data: Profile ID: {profile_id}...")
        filename = f"{profile_id}.jpg"
        
        # get list of existing profiles
        profile_index_data = self.DBI.get_all_profile_uids()
        profile_index = profile_index_data['rows']
        
        image_dict = []
        
        for item in profile_index:
            uid_obj = { 
                    "uid" : item[1],
                    "images": self.get_all_images_for_profile(item[1]),
                    }
            self.LOG_MGR.log(f"\nPROFILE_MANAGER(find_person_by_profile_id): PROFILE-IMAGES:\n\t{uid_obj}\n")    
            image_dict.append(uid_obj)
        
        name = None
        return_data = {"found": False, "name": None, "uid": None, "file_path": None}
        
        for item in image_dict:
            if filename in item['images']:
                
                name_data = self.DBI.get_mapper_name_by_uid(item['uid'])
                name = name_data['rows'][0][0]
                
                self.LOG_MGR.log(f"\nPROFILE_MANAGER(find_person_by_profile_id):\n\tIMG-FOUND in '{name}'\n")
                return_data = {"found": True, "name": name, "uid": item['uid'], "file_path": f"{self.PROFILE_INDEX_FOLDER}{item['uid']}\\img\\"}
        
        self.LOG_MGR.log(f"\tRETURNING(find_person_by_profile_id) -> RETURN DATA: {return_data}\n")            
        return return_data


    def restore_incorrectly_tagged_image(self, profile_id, from_uid, file_path, name):
        self.LOG_MGR.log(f"PROFILE_MANAGER(restore_incorrectly_tagged_image): Incoming data:\n\tProfile ID: {profile_id}, From UID: {from_uid}, File Path: {file_path}, Name: {name}")
        image_path = f"{file_path}{profile_id}.jpg"
    
        restored_image_path = f"{self.TMP_DATA_PATH}{profile_id}.jpg"
        
        self.LOG_MGR.log(f"\nMOVING-IMG-FILE:\n\tFrom: {image_path}\n\tTo: {restored_image_path}\n")
        shutil.move(image_path, restored_image_path)
    