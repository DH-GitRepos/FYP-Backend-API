import os
import shutil


class CleanupManager:
    def __init__(self, database_interface):
        self.DBI = database_interface
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.PROFILE_PATH = f"{self.FILE_PATH}\\..\\profiles\\"
        self.PROFILE_FRDB_INDEX_PATH = f"{self.PROFILE_PATH}data\\"
        self.PROFILE_FRDB_DATA_PATH = f"{self.PROFILE_FRDB_INDEX_PATH}fr_db\\"
        self.PROFILE_PEOPLE_PATH = f"{self.PROFILE_PATH}people\\"
        self.PROFILE_TMP_PATH = f"{self.PROFILE_PATH}tmp\\"
        self.LIBRARY_PATH = f"{self.FILE_PATH}\\..\\library\\"
        self.LIBRARY_IMG_PATH = f"{self.FILE_PATH}\\..\\library\\images\\"
        self.UPLOADS_PATH = f"{self.FILE_PATH}\\..\\uploads\\"
        self.LOG_PATH = f"{self.FILE_PATH}\\..\\logs\\"

    def clean_up_database(self):
        # Clean the database
        self.DBI.clean_database()

    def clean_up_files(self):
        static_file_removal_list = []
        recursive_removal_list = []
        
        # collect log files
        for file in os.listdir(self.LOG_PATH):
            if file.endswith('.txt'):
                static_file_removal_list.append(f"{self.LOG_PATH}{file}")
                
        # collect uploaded files
        for file in os.listdir(self.UPLOADS_PATH):
            if file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.jpeg') or file.endswith('.JPEG') or file.endswith('.png') or file.endswith('.PNG'):
                static_file_removal_list.append(f"{self.UPLOADS_PATH}{file}")
        
        # collect profiles -> tmp files
        for file in os.listdir(self.PROFILE_TMP_PATH):
            if file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.jpeg') or file.endswith('.JPEG') or file.endswith('.png') or file.endswith('.PNG'):
                static_file_removal_list.append(f"{self.PROFILE_TMP_PATH}{file}")
        
        # collect profiles -> people dirs (recursive)
        for file in os.listdir(self.PROFILE_PEOPLE_PATH):
            if os.path.isdir(f"{self.PROFILE_PEOPLE_PATH}{file}"):
                recursive_removal_list.append(f"{self.PROFILE_PEOPLE_PATH}{file}")
        
        # collect library -> image files
        for file in os.listdir(self.LIBRARY_IMG_PATH):
            if file.endswith('.pkl') or file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.jpeg') or file.endswith('.JPEG') or file.endswith('.png') or file.endswith('.PNG'):
                static_file_removal_list.append(f"{self.LIBRARY_IMG_PATH}{file}")
        
        # delete static files
        for file in static_file_removal_list:
            if os.path.exists(file):
                os.remove(file)
        
        # recursively delete folders
        for dir in recursive_removal_list:
            if os.path.exists(dir):
                shutil.rmtree(dir)  
                
                              
