class FindEndpoint:
    def __init__(self, request, logging_manager, mapper_manager, library_manager):
        self.REQ = request
        self.LOG_MGR = logging_manager
        self.MAP_MGR = mapper_manager
        self.LIB_MGR = library_manager
        

    def find_route(self):
        self.LOG_MGR.set_log_type('find')
        self.LOG_MGR.log("\n*****************************", "off")    
        self.LOG_MGR.log("******** FIND REQUEST ********", "off")    
        self.LOG_MGR.log("*****************************\n", "off")
        self.LOG_MGR.log(f"\nAPI('/find'): Received data\n\t{self.REQ}")
        
        request_type = self.REQ['req_type']
        request_uid = self.REQ['uid']
        
        return_data = {"content": []}
        
        if request_type == 'init':
            mapper = self.MAP_MGR.get_mapper_data()
        
            for profile in mapper['identities']:
                uid = profile['uid']
                name = profile['name']
                return_data["content"].append({"uid": uid, "name": name})
                
        elif request_type == 'req':
            image_list = self.LIB_MGR.get_images_by_uid(request_uid)
            
            for img in image_list:
                img_url = f"http://127.0.0.1:5000/image-library/{img}.jpg"
                return_data["content"].append(img_url) 
        
        self.LOG_MGR.log(f"\nAPI('/find'): Returning data\n\t{return_data}")        
        
        self.LOG_MGR.log("\n=============================", "off")    
        self.LOG_MGR.log("------ END FIND REQUEST -----", "off")    
        self.LOG_MGR.log("=============================\n", "off") 
        
        return return_data
    