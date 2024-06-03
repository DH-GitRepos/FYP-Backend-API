from flask import jsonify 

class ImageEndpoint:
    def __init__(self, request, logging_manager, mapper_manager, library_manager):
        self.REQ = request
        self.LOG_MGR = logging_manager
        self.MAP_MGR = mapper_manager
        self.LIB_MGR = library_manager


    def image_route(self):
        self.LOG_MGR.set_log_type('image')
        self.LOG_MGR.log("\n*****************************", "off")    
        self.LOG_MGR.log("******* IMAGE REQUEST ********", "off")    
        self.LOG_MGR.log("*****************************\n", "off")
        self.LOG_MGR.log(f"\nAPI('/image'): Received data\n\t{self.REQ}")
        
        request_type = self.REQ['req_type']
        return_data = {
                        "content": {
                            "status": None, 
                            "message": None,
                            "imgID": None, 
                            "img_url": None, 
                            "tagged_faces": None
                        }
                      }
        
        if request_type == 'get_image':        
            
            image_id = self.REQ['imgID']
            img_url = f"http://127.0.0.1:5000/image-library/{image_id}.jpg"
            
            library_index_data = self.LIB_MGR.get_all_tagged_faces_by_image_timestamp(image_id)
                          
            self.LOG_MGR.log(f"\nAPI('/image'): Tagged faces request response: \n\t{library_index_data}")
             
            uid_list = []
            library_uid_index = library_index_data['rows']
            
            self.LOG_MGR.log(f"\nAPI('/image'): Library UID index: \n\t{library_uid_index}")
            
            for uid in library_uid_index:
                uid_list.append(uid[0])
                
            self.LOG_MGR.log(f"\nAPI('/image'): UID list to process: \n\t{uid_list}")
             
            names = []

            for person_uid in uid_list:
                name_data = self.MAP_MGR.find_name_by_uid(person_uid)
                
                self.LOG_MGR.log(f"\nAPI('/image'): Mapper name request response: \n\t{name_data}")
                name = name_data['rows'][0][0]
                
                self.LOG_MGR.log(f"\nAPI('/image'): Mapper name found: \n\t{name}")
                
                names.append(name)

            return_data["content"]["status"] = 200
            return_data["content"]["message"] = "OK"            
            return_data["content"]["imgID"] = image_id
            return_data["content"]["img_url"] = img_url
            return_data["content"]["tagged_faces"] = names
            
            
            # .append({"status": 200, "imgID": image_id, "img_url": img_url, "tagged_faces": names})
        else:
            return_data["content"]["status"] = 400
            return_data["content"]["message"] = "ERROR: Invalid request type"
            return_data["content"]["imgID"] = image_id
            return_data["content"]["img_url"] = img_url
            return_data["content"]["tagged_faces"] = names
            
            # return_data["content"].append({"status": 400, "error": "Invalid request type"})

        self.LOG_MGR.log(f"\nAPI('/image'): Endpoint returning status: {return_data['content']['status']}, {return_data['content']['message']}")
        
        self.LOG_MGR.log("\n=============================", "off")    
        self.LOG_MGR.log("----- END IMAGE REQUEST -----", "off")    
        self.LOG_MGR.log("=============================\n", "off") 
        
        return return_data