from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
import os
import time


class UploadEndpoint:
    def __init__(self, file, UPLOAD_FOLDER, TMP_PROFILE_DATA_PATH, FR_API, log_mgr, data_manager, df_detection_manager, frdb_manager, profile_manager, mapper_manager, library_manager):
        
        self.FILE = file
        self.UPLOAD_FOLDER = UPLOAD_FOLDER
        self.TMP_PROFILE_DATA_PATH = TMP_PROFILE_DATA_PATH
        
        self.FR_API = FR_API
        self.LOG_MGR = log_mgr
        self.DATA_MGR = data_manager
        self.DET_MGR = df_detection_manager
        self.FRDB_MGR = frdb_manager
        self.PROF_MGR = profile_manager
        self.MAP_MGR = mapper_manager
        self.LIB_MGR = library_manager
        

    def allowed_file(self, filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            

    def upload_route(self):
        self.LOG_MGR.set_log_type('upload')
        self.LOG_MGR.log("\n*****************************", "off")    
        self.LOG_MGR.log("****** UPLOAD REQUEST *******", "off")    
        self.LOG_MGR.log("*****************************\n", "off")
        
        response = {} # creatre a response object
        
        ####################################################
        ### RECEIVE, PROCESS AND SAVE THE IMAGE ############
        ###
        
        # If the file is valid, save it to the uploads folder
        if self.FILE and self.allowed_file(self.FILE.filename):
            img_format = self.FILE.filename.split('.')[-1]        
            timestamp = str(int(time.time() * 1000)) 
            filename = secure_filename(self.FILE.filename)
            filename_new = f"{timestamp}.{img_format}"
            filepath = os.path.join(self.FR_API.config['UPLOAD_FOLDER'], filename_new)
            self.FILE.save(filepath)
            self.FILE.close()
            
            # DEAL WITH IMAGE ROTATION ISSUES (Caused by mobile devices!)
            # Open the image using PIL
            with Image.open(filepath) as img:
                # Rotate the image based on its EXIF metadata.
                # - this solves odd orientation issues in the detection process.
                img = ImageOps.exif_transpose(img)            
                # Save the rotated image back to the file.
                img.save(filepath)
                img.close()
                # Get the width and height of the image
                width, height = img.size
                
            ####################################################
            ### DETECT AND SAVE FACES IN IMAGE #################
            ###
            ### Detection data saved to DB (df_detect_faces > detection_data)
            ### Face crops saved to file system (df_detect_faces > file system)
            ###
                    
            # Create a unique ID for the image
            img_id = self.DATA_MGR.create_uuid()
            self.LOG_MGR.log(f"\nAPI('/upload'): New image ID: {img_id}")  
            
            # Detect faces in the image and return the detection data 
            self.LOG_MGR.log("\nAPI('/upload'): Detecting faces in the image...")   
            DETECTION_DATA = self.DET_MGR.df_detect_faces(filepath, img_id, timestamp)
            number_of_faces = len(DETECTION_DATA)
            
            self.LOG_MGR.log(f"\nAPI('/upload'): Detected {number_of_faces} faces in the image.")
        
            ####################################################
            ### SAVE IMAGE DATA TO DB ##########################
            ### 
            ### Save image data to the DB (uploaded_image_data)
            ###
            
            # Store the image data in DB
            self.LOG_MGR.log("\nAPI('/upload'): Storing image data...")
            
            # Create a dictionary to store the image data
            img_data = {
                'timestamp': timestamp,
                'file_name': filename,
                'file_width': width,
                'file_height': height,
                'num_faces_detected': number_of_faces,
                'img_format': img_format
                }
            
            self.LIB_MGR.save_uploaded_file_data(img_data)
            
            ####################################################
            ### PROCESS FACE FILES INTO TMP PROFILES ###########
            ###
            ### Store tmp profiles in DB (profile_tmp_index_frdb)
            ###
            
            # Set up collection for individual face profiles
            current_detected_faces_for_image = []
            
            # DO PER-FACE PROCESSING TASKS:       
            if number_of_faces > 0:
                self.LOG_MGR.log("\nAPI('/upload'): Processing detacted faces...")
                for item in DETECTION_DATA:
                    
                    # set up a referecnce the original image file for each detected face
                    src_file = f"{timestamp}-{item['id']}"
                   
                    # Save the detection data to a pickle file for each detected face
                    self.LOG_MGR.log(f"\nAPI('/upload'): Storing detection data for face {item['id']}...")
                    
                    # create a temporary profile for each detected face and add it to the FRDB
                    # ready for FR tasks.
                    self.LOG_MGR.log(f"\nAPI('/upload'): Creating temp face profile and adding face {item['id']} to the FRDB...")
                    
                    # create a new tmp profile object and store in the DB
                    new_tmp_profile = {"src": src_file, "uid": item['face_uid']}
                    
                    self.FRDB_MGR.insert_tmp_profile_to_frdb(new_tmp_profile)
                    
                    new_item = {
                        "tmp_face_uid": item['face_uid'],
                        "matched_face_uid": None,
                        "match_found": False,
                        "timestamp": timestamp,
                        "timestamp_id": item['id'],
                        "src": src_file,
                        "name": None
                    }                
                    
                    current_detected_faces_for_image.append(new_item)
        
                ####################################################
                ### CHECK FOR EXISTING TAGGED PROFILES #############
                ###
                ### If there are tagged profiles in the profile 
                ### index, can check for matches with tmp profiles.
                ###
                
                # To check for matches, we need to have tagged profiles in the profile index
                can_check_for_matches = False
                
                # Get existing tagged profiles, unless the profile index is empty
                self.LOG_MGR.log("\nAPI('/upload'): Checking for existing tagged face profiles...")
                
                # Get a count of existing tagged profiles                
                existing_profiles = self.PROF_MGR.get_all_profile_uids()
                qty_of_existing_profiles = existing_profiles['num_rows']                
                
                if qty_of_existing_profiles < 1:
                    self.LOG_MGR.log("\nAPI('/upload'): No tagged profiles found.")
                else:
                    self.LOG_MGR.log(f"\nAPI('/upload'): Found {qty_of_existing_profiles} tagged profiles.")
                    can_check_for_matches = True
                
                ####################################################
                ### CHECK TMP PROFILES AGAINST EXISTING PROFILES ###
                ###
                ###                
                
                # Set up a collection to store the matches to be processed
                PROFILE_MATCH_DATA = {
                    "matches_found": False,
                    "matches": []            
                }
                
                matches_found = False
                
                # If the profile index is not empty, check for matches
                # between the new faces and the tagged profiles        
                if can_check_for_matches:
                    self.LOG_MGR.log("\nAPI('/upload'): Checking new faces against existing profile for matches...")
                    
                    PROFILE_MATCH_DATA = self.FRDB_MGR.check_tmp_profiles_for_match(current_detected_faces_for_image)
                    
                    self.LOG_MGR.log(f"\nAPI('/upload'): PROFILE MATCH DATA: \n\t{PROFILE_MATCH_DATA}")             
                    
                    # Made changes to the check_tmp_profiles_for_match function and check_for_profile_match
                    # to use df_detection_manager.compare_landmarks() to check for matches.
                    if PROFILE_MATCH_DATA['matched_profiles']['matches_found'] == True:
                        matches_found = True
                
                # Set up a collection to store the matches to be processed        
                tag_data = []
                
                self.LOG_MGR.log(f"\nAPI('/upload'): PROFILE MATCH DATA:\n\t{PROFILE_MATCH_DATA}")
                
                if matches_found:
                    self.LOG_MGR.log("\nAPI('/upload'): Matches found, processing match data...")
                    
                    # set return data for the user
                    for item in PROFILE_MATCH_DATA['profile_match_list']:
                        return_timestamp = item['timestamp']
                        return_id = item['timestamp_id']
                        return_tagged_status = item['match_found']
                        
                        # data specific to a matched face                    
                        if item['match_found']:
                            return_uid = item['matched_face_uid']
                            
                            return_name_data = self.MAP_MGR.find_name_by_uid(return_uid)
                            return_name = return_name_data['rows'][0][0]                            
                            
                            self.LOG_MGR.log(f"\nAPI('/upload'): FOUND USER({return_id}): {return_name}")
                        
                        # data specific to an unmatched face
                        else:
                            return_uid = item['tmp_face_uid']
                            return_name = ""
                            
                        return_obj = {"timestamp": return_timestamp, "id": return_id, "tagged": return_tagged_status, "name": return_name, "uid": return_uid}
                        tag_data.append(return_obj)
                            
                    # merge profiles
                    for match in PROFILE_MATCH_DATA['profile_match_list']:

                        m_match_found = match['match_found']
                        m_tmp_uuid = match['tmp_face_uid']
                        m_main_uuid = match['matched_face_uid']
                        m_src = match['src']
                        m_face_id = match['timestamp_id']
                        m_timestamp = match['timestamp']
                        
                        if m_match_found:
                            # move the image to the correct profile
                            self.PROF_MGR.move_tmp_to_profile(m_src, m_main_uuid)
                            
                            # add tagged face to the image (image_library_tagged_faces)
                            self.LIB_MGR.insert_tagged_face_to_library_image(m_timestamp, m_face_id, m_main_uuid)
                            
                            # remove the tmp profile from the FRDB table
                            self.FRDB_MGR.remove_temp_profile_by_uid(m_tmp_uuid)
                            
                            # update the image tagged status in the image library
                            self.LIB_MGR.update_image_tagged_value(m_timestamp, 1)
                            
                else:
                    self.LOG_MGR.log("\nAPI('/upload'): No matches found.")     
                    
                    # set return data for the user
                    for item in current_detected_faces_for_image:
                        return_timestamp = item['timestamp']
                        return_id = item['timestamp_id']
                        return_tagged_status = item['match_found']
                        return_uid = item['tmp_face_uid']
                        return_name = ""
                            
                        return_obj = {"timestamp": return_timestamp, "id": return_id, "tagged": return_tagged_status, "name": return_name, "uid": return_uid}
                        tag_data.append(return_obj)
                        

            # MOVE THE IMAGE TO THE LIBRARY
            self.LOG_MGR.log("\nAPI('/upload'): Moving image to the library...")
            self.LIB_MGR.move_upload_to_library(timestamp)

            # PREPARE AND SEND THE CLIENT RESPONSE
            face_list = []

            for item in DETECTION_DATA:
                face_list.append({
                    'id': item['id'],
                    'pos_x': item['bounding_box']['x'],
                    'pos_y': item['bounding_box']['y'],
                    'pos_width': item['bounding_box']['w'],
                    'pos_height': item['bounding_box']['h']
                    })

            response_data = {
                'message': 'File successfully uploaded',
                'timestamp': timestamp, 
                'file_name': filename,
                'file_width': width,
                'file_height': height,
                'num_faces': number_of_faces,
                'faces': face_list,
                'tag_data': tag_data
            }        
            
            self.LOG_MGR.log(f"\nAPI('/upload'): Response data:\n\t{response_data}")
                    
            response = response_data
            
            self.LIB_MGR.check_tagged_values()
            
            self.LOG_MGR.log("\n=============================", "off")    
            self.LOG_MGR.log("---- END UPLOAD REQUEST -----", "off")    
            self.LOG_MGR.log("=============================\n", "off")
            
            self.LOG_MGR.log("\nAPI('/upload'): Returning response to client...")
            # return response
            
        else:
            response = {'error': 'Invalid file type'}
            
        return response
        