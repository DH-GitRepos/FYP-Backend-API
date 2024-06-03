import os
from deepface import DeepFace as df


class FRDBManager:  
    def __init__(self, logging_manager, data_manager, detection_manager, mapper_manager, database_interface):
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__)) 
        self.PROFILE_FOLDER = f"{self.FILE_PATH}\\..\\profiles\\people\\"
        self.TMP_FOLDER = f"{self.FILE_PATH}\\..\\profiles\\tmp\\"
        self.FRDB_FOLDER = f"{self.FILE_PATH}\\..\\profiles\\data\\fr_db\\"
        self.FRDB_PATH = f"{self.FRDB_FOLDER}fr_db.json"
        
        self.LOG_MGR = logging_manager
        self.DATA_MGR = data_manager
        self.DET_MGR = detection_manager        
        self.MAP_MGR = mapper_manager
        self.PROF_MGR = None
        self.DBI = database_interface
        
    
    # To solve circular initialisation dependency with ProfileManager
    def set_prof_mgr(self, prof_mgr):
        self.PROF_MGR = prof_mgr
        

    def insert_tmp_profile_to_frdb(self, new_tmp_profile):
        self.LOG_MGR.log(f"FRDB_MANAGER(insert_tmp_profile_to_frdb): Incoming data:\n\tNEW TEMP PROFILE: {new_tmp_profile}")
        
        self.DBI.insert_tmp_profile_to_frdb(new_tmp_profile)
        
        self.LOG_MGR.log(f"\tRETURNING(insert_tmp_profile_to_frdb) -> TRUE\n")
        
        return True
    
    
    def remove_temp_profile_by_uid(self, uid):
        self.LOG_MGR.log(f"FRDB_MANAGER(remove_temp_profile_by_uid): Incoming data:\n\tUID: {uid}")
        
        self.DBI.remove_temp_profile_by_uid(uid)
        
        self.LOG_MGR.log(f"\tRETURNING(remove_temp_profile_by_uid) -> TRUE\n")
        
        return True
    
    
    # CHECKS TMP PROFILE IMAGES AGAINST MAIN PROFILE IMAGES FOR MATCHES
    # RETURNS A LIST OF MATCHED PROFILES (tmp_uid > main_uid) WITH MATCH STATUS
    def check_tmp_profiles_for_match(self, tmp_profiles_to_check):
        self.LOG_MGR.log(f"FRBD_MANAGER(check_tmp_profiles_for_match): Incoming data:\n\tPROFILE MATCH LIST: {tmp_profiles_to_check}")

        timestamp = tmp_profiles_to_check[0]['timestamp']
        
        # Collection to contain matched profiles    
        matched_profiles = {
            "matches_found": False,
            "matches":  []
        }
        
        # get all existing profile images
        all_profile_images = self.PROF_MGR.get_all_profile_images()
        qty_profile_images = len(all_profile_images)
        
        # get all temp profile images for the current timestamp
        all_tmp_images = self.PROF_MGR.get_all_tmp_images_by_timestamp(timestamp)
        
        if qty_profile_images > 0:
            self.LOG_MGR.log("\tFRDB_MANAGER(check_tmp_profiles_for_match):\n\tMatching temp profiles to main profiles...")
            
            for tmp_image_path in all_tmp_images:
                
                current_tmp_face_uid = tmp_image_path["uid"]
                current_tmp_face_path = tmp_image_path["img_path"]
                
                for uid_instance in all_profile_images:
                    
                    current_profile_img_uid = uid_instance['uid']
                    current_profile_name_data = self.DBI.get_mapper_name_by_uid(current_profile_img_uid)
                    current_profile_name = current_profile_name_data['rows'][0][0]
                    
                    for profile_img_path in uid_instance['img_paths']:
                    
                        matched = self.DET_MGR.df_verify_faces(current_tmp_face_path, profile_img_path)
                        self.LOG_MGR.log(f"\tVALUE-OF-MATCHED:\n\t{matched}")
                        
                        if matched:
                            self.LOG_MGR.log(f"\tCHECK, MATCH: {current_tmp_face_uid} and {current_profile_img_uid}!")
                            matched_profiles['matches_found'] = True
                            profile_match = {"tmp": current_tmp_face_uid, "main": current_profile_img_uid}
                            matched_profiles['matches'].append(profile_match)
                            
                            # Add profile['uid'] to the profile_match_list where the objects temp_face_uid == tmp_profile
                            for p_item in tmp_profiles_to_check:
                                if p_item['tmp_face_uid'] == current_tmp_face_uid:
                                    p_item['matched_face_uid'] = current_profile_img_uid
                                    p_item['match_found'] = True
                                    p_item['name'] = current_profile_name
                                    break
                            
                        else:
                            self.LOG_MGR.log(f"\tCHECK, NO MATCH!")  
        
        else:
            self.LOG_MGR.log("\tFRDB_MANAGER(check_tmp_profiles_for_match):\n\tNo existing temp profiles to check...")
                        
        self.LOG_MGR.log(f"\tFRDB_MANAGER(check_tmp_profiles_for_match):\n\tMatched Profiles: {matched_profiles}")
        
        return_data = {"matched_profiles": matched_profiles, "profile_match_list": tmp_profiles_to_check}
        
        self.LOG_MGR.log(f"\tRETURNING(check_tmp_profiles_for_match) -> RETURN DATA: {return_data}\n")        
        
        return return_data
