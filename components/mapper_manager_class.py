import os


class MapperManager:
    def __init__(self, logging_manager, database_interface):
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.MAPPER_FOLDER = f"{self.FILE_PATH}\\..\\profiles\\mapper\\"
        self.MAPPER_PATH = f"{self.MAPPER_FOLDER}mapper.json"
        self.LOG_MGR = logging_manager
        self.DBI = database_interface
    
    
    def get_mapper_data(self):
        self.LOG_MGR.log(f"MAPPER_MANAGER(get_mapper_data)")
        
        result = self.DBI.get_mapper_data()
        if result['num_rows'] == 0:
            return False
        
        else:
            mapper_data = {
                "identities": []
            }
            
            for row in result['rows']:
                uid = row[0]
                name = row[1]
                mapper_data['identities'].append({"uid": uid, "name": name})
            
            self.LOG_MGR.log(f"\tRETURNING(get_mapper_data) -> MAPPER DATA: {mapper_data}\n")
            return mapper_data
    
    
    def find_name_by_uid(self, uid):
        self.LOG_MGR.log(f"MAPPER_MANAGER(find_name_by_uid): Incoming data:\n\tUID: {uid}")
        
        result = self.DBI.get_mapper_name_by_uid(uid)

        self.LOG_MGR.log(f"\tRETURNING(find_name_by_uid) -> NAME: {result}\n")
        return result    
    
    
    def get_mapper_uid_by_name(self, name):
        self.LOG_MGR.log(f"MAPPER_MANAGER(get_mapper_uid_by_name): Incoming data:\n\tNAME: {name}")
    
        uid_profile_results = self.DBI.get_mapper_uid_by_name(name)
    
        self.LOG_MGR.log(f"\tRETURNING(get_mapper_uid_by_name) -> RESULTS: {uid_profile_results}\n")
        
        return uid_profile_results
        

    def find_uid_by_name(self, name):
        self.LOG_MGR.log(f"MAPPER_MANAGER(find_uid_by_name): Incoming data:\n\tNAME: {name}")
        
        result = self.DBI.get_uid_by_name(name)
        if result['num_rows'] == 0:
            return False
        
        else:
            uid = result['rows'][0][0]
            self.LOG_MGR.log(f"\tRETURNING(find_uid_by_name) -> UID: {uid}\n")
            return uid
