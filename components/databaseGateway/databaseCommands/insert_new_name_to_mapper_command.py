class InsertNewNameToMapper():
    def __init__(self, profile_name, profile_uid):
        self.NAME = profile_name
        self.UID = profile_uid
        self.QUERY = f"INSERT INTO `profile_mapper` (`profile_uid`, `name`) VALUES ('{self.UID}', '{self.NAME}');"
        
        
    def return_query(self):
        print("(InsertNewNameToMapper) QUERY:")
        print(self.QUERY)
        return self.QUERY