class GetMapperUIDByName():
    def __init__(self, profile_name):
        self.NAME = profile_name
        self.QUERY = f"SELECT `profile_uid` FROM `profile_mapper` WHERE LOWER(`name`) = LOWER('{profile_name}');"
        
        
    def return_query(self):
        print("(GetMapperUIDByName) QUERY:")
        print(self.QUERY)
        return self.QUERY