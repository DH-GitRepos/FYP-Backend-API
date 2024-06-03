class LibraryEndpoint:
    def __init__(self, request, logging_manager, library_manager):
        self.REQ = request
        self.LOG_MGR = logging_manager
        self.LIB_MGR = library_manager


    def library_route(self):
        self.LOG_MGR.set_log_type('library')
        self.LOG_MGR.log("\n*****************************", "off")    
        self.LOG_MGR.log("****** LIBRARY REQUEST *******", "off")    
        self.LOG_MGR.log("*****************************\n", "off")
        self.LOG_MGR.log(f"\nAPI('/library'): Received data\n\t{self.REQ}")
        
        request_type = self.REQ['req_type']
        return_data = {"content": []}
        
        if request_type == 'get_all_images':
            image_list = self.LIB_MGR.get_all_images() 
            
            for img in image_list:
                img_url = f"http://127.0.0.1:5000/image-library/{img}.jpg"
                return_data["content"].append(img_url)   
        
        self.LOG_MGR.log(f"\nAPI('/library'): Returning data\n\t{return_data}")        
        
        self.LOG_MGR.log("\n=============================", "off")    
        self.LOG_MGR.log("---- END LIBRARY REQUEST ----", "off")    
        self.LOG_MGR.log("=============================\n", "off") 

        return return_data