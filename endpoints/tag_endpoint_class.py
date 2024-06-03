class TagEndpoint:
    def __init__(self, request, log_mgr, profile_manager, mapper_manager, library_manager):
        self.REQ = request
        self.LOG_MGR = log_mgr
        self.PROF_MGR = profile_manager
        self.MAP_MGR = mapper_manager
        self.LIB_MGR = library_manager


    def tag_route(self):
        self.LOG_MGR.set_log_type('tag')
        self.LOG_MGR.log("\n*****************************", "off")    
        self.LOG_MGR.log("******** TAG REQUEST ********", "off")    
        self.LOG_MGR.log("*****************************\n", "off")

        incoming_timestamp = self.REQ['tsp']
        incoming_face_tags = self.REQ['faces']
        
        self.LOG_MGR.log(f"\nAPI('/tag'): Received data\n\t{self.REQ}")
        
        for tag in incoming_face_tags:
            id = tag['id']
            name = tag['name']
            checkbox = tag['checkbox'] 
            tagged = tag['tagged'] 
            uid = tag['uid']
                    
            self.LOG_MGR.log(f"\nAPI('/tag'): Face ID: {id}, Name: {name}, Checkbox: {checkbox}")
            
            # If the checkbox is checked (on), tag the face
            if checkbox == "on":
                
                if tagged == "true": # has been pre-tagged
                    
                    tag_corrected = self.PROF_MGR.check_incoming_tags_match_pre_tags(self.REQ)
                    self.LOG_MGR.log(f"\nAPI('/tag'): TAG-CORRECTED: {tag_corrected}")
                    
                elif tagged == "false": # has not been pre-tagged
                    
                    # CHECK FOR EXISTING PROFILE
                    uid_profile_exists = None                    
                    uid_profile_results = self.MAP_MGR.get_mapper_uid_by_name(name)
                    
                    self.LOG_MGR.log(f"\nAPI('/tag'): UID RESULTS:\n\t{uid_profile_results}\n")
                    
                    if uid_profile_results['num_rows'] == 0:
                        uid_profile_exists = False
                    else:
                        uid_profile_exists = uid_profile_results['rows'][0]['uid']
                
                    self.LOG_MGR.log(f"\nAPI('/tag'): PROFILE EXISTS DATA: {uid_profile_exists}")
                
                    if not uid_profile_exists:
                        self.LOG_MGR.log(f"\nAPI('/tag'): New profile for {name}, creating...")
                        self.PROF_MGR.create_new_profile_from_temp_data(incoming_timestamp, id, name)
                        
                    else:
                        self.LOG_MGR.log(f"\nAPI('/tag'): Profile exists for {name}, updating...")
                        self.PROF_MGR.update_profile_with_temp_data(incoming_timestamp, id, name, uid_profile_exists)
         
        self.LIB_MGR.check_tagged_values()
                    
        self.LOG_MGR.log("\n=============================", "off")    
        self.LOG_MGR.log("------ END TAG REQUEST ------", "off")    
        self.LOG_MGR.log("=============================\n", "off") 
           
        response = {"message": "Faces tagged"}
            
        return response
