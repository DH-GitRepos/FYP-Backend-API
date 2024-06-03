import os
from datetime import datetime


class LogManager:
    def __init__(self):
        self.LOGGING_ENABLED = True # DISABE LOGGING WHEN TESTING NON-PACKAGE FILES
        self.OUTPUT_TO_FILE = True
        self.OUTPUT_TO_TERMINAL = True
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.LOG_FILE_FOLDER = f"{self.FILE_PATH}\\..\\logs\\"
        self.LOG_FILES = {
            "api": "api_log.txt",
            "uploads": "uploads_log.txt",
            "tags": "tags_log.txt",
            "find": "find_log.txt",
            "image": "image_log.txt",
            "library": "library_log.txt",
            "db": "db_log.txt"
        }
        self.LOG_FILE_PATHS = {
            "uploads": f"{self.LOG_FILE_FOLDER}{self.LOG_FILES['uploads']}",
            "tags": f"{self.LOG_FILE_FOLDER}{self.LOG_FILES['tags']}",
            "api": f"{self.LOG_FILE_FOLDER}{self.LOG_FILES['api']}",
            "find": f"{self.LOG_FILE_FOLDER}{self.LOG_FILES['find']}",
            "image": f"{self.LOG_FILE_FOLDER}{self.LOG_FILES['image']}",
            "library": f"{self.LOG_FILE_FOLDER}{self.LOG_FILES['library']}",
            "db": f"{self.LOG_FILE_FOLDER}{self.LOG_FILES['db']}"
        }
        self.OUTPUT_FILE = True
        self.OUTPUT_TERMINAL = True
        self.LOG_FILE_PATH = ""


    def set_log_type(self, type):
        if self.LOGGING_ENABLED:
            # Change these to control where the log data is output  
            log_files = {
                "upload": self.LOG_FILE_PATHS['uploads'],
                "tag": self.LOG_FILE_PATHS['tags'],
                "api": self.LOG_FILE_PATHS['api'],
                "find": self.LOG_FILE_PATHS['find'],
                "image": self.LOG_FILE_PATHS['image'],
                "library": self.LOG_FILE_PATHS['library'],
                "db": self.LOG_FILE_PATHS['db']
            }
            
            self.LOG_FILE_PATH = log_files.get(type)

            return True


    def check_log_file_exists(self):
        if self.LOGGING_ENABLED: 
            if os.path.exists(self.LOG_FILE_PATH):
                return True        
            else:
                return False


    def create_log_files(self): 
        print("API(INIT)(create_log_files)::CREATING LOG FILES...\n")
        if self.LOGGING_ENABLED: 
            if not os.path.exists(self.LOG_FILE_FOLDER):
                os.makedirs(self.LOG_FILE_FOLDER)
            
            now = datetime.now()
            dt = now.strftime("%d-%m-%Y@%H:%M:%S")
            
            if not os.path.exists(self.LOG_FILE_PATHS['api']):   
                with open(self.LOG_FILE_PATHS['api'], 'w') as f:
                    f.write(f"API LOG FILE CREATED: {dt}\n")
                print("API(INIT)::LOG FILE CREATED -> (API LOG)\n")
            else:
                print("API(INIT)::LOG FILE EXISTS -> (API LOG)\n")
                        
            if not os.path.exists(self.LOG_FILE_PATHS['uploads']):            
                with open(self.LOG_FILE_PATHS['uploads'], 'w') as f:
                    f.write(f"UPLOADS ENDPOINT LOG FILE CREATED: {dt}\n")
                print("API(INIT)::LOG FILE CREATED -> (UPLOAD ENDPOINT LOG)\n")
            else:
                print("API(INIT)::LOG FILE EXISTS -> (UPLOAD ENDPOINT LOG)\n")
                
            if not os.path.exists(self.LOG_FILE_PATHS['tags']):    
                with open(self.LOG_FILE_PATHS['tags'], 'w') as f:
                    f.write(f"TAG ENDPOINT LOG FILE CREATED: {dt}\n")
                print("API(INIT)::LOG FILE CREATED -> (TAG ENDPOINT LOG)\n")
            else:
                print("API(INIT)::LOG FILE EXISTS -> (TAG ENDPOINT LOG)\n")
            
            if not os.path.exists(self.LOG_FILE_PATHS['find']):    
                with open(self.LOG_FILE_PATHS['find'], 'w') as f:
                    f.write(f"FIND ENDPOINT LOG FILE CREATED: {dt}\n")
                print("API(INIT)::LOG FILE CREATED -> (FIND ENDPOINT LOG)\n")
            else:
                print("API(INIT)::LOG FILE EXISTS -> (FIND ENDPOINT LOG)\n")
                        
            if not os.path.exists(self.LOG_FILE_PATHS['image']):    
                with open(self.LOG_FILE_PATHS['image'], 'w') as f:
                    f.write(f"IMAGE ENDPOINT LOG FILE CREATED: {dt}\n")
                print("API(INIT)::LOG FILE CREATED -> (IMAGE ENDPOINT LOG)\n")
            else:
                print("API(INIT)::LOG FILE EXISTS -> (IMAGE ENDPOINT LOG)\n")
                    
            if not os.path.exists(self.LOG_FILE_PATHS['library']):    
                with open(self.LOG_FILE_PATHS['library'], 'w') as f:
                    f.write(f"LIBRARY ENDPOINT LOG FILE CREATED: {dt}\n")
                    print("API(INIT)::LOG FILE CREATED -> (LIBRARY ENDPOINT LOG)\n")
            else:
                print("API(INIT)::LOG FILE EXISTS -> (LIBRARY ENDPOINT LOG)\n")
                
            if not os.path.exists(self.LOG_FILE_PATHS['db']):    
                with open(self.LOG_FILE_PATHS['db'], 'w') as f:
                    f.write(f"DATABASE LOG FILE CREATED: {dt}\n")
                    print("API(INIT)::LOG FILE CREATED -> (DATABASE LOG)\n")
            else:
                print("API(INIT)::LOG FILE EXISTS -> (DATABASE LOG)\n")
                        
            return True


    def log(self, data, date_time="on"):
        if self.LOGGING_ENABLED:
            
            if date_time == "on":
                now = datetime.now()
                str_time = now.strftime("%d-%m-%Y@%H:%M:%S")
                dt = f"{str_time}:\n{data}"
            else:
                dt = ""
                
            if self.OUTPUT_TO_TERMINAL:
                print(f"{data}")
            
            if self.OUTPUT_TO_FILE:
                with open(self.LOG_FILE_PATH, 'a') as f:
                    f.write(f"{dt}\n{data}\n")
                
            return True
