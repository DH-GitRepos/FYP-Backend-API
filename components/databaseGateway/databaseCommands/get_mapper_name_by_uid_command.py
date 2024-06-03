class GetMapperNameByUID():
    def __init__(self, profile_uid):
        self.UID = profile_uid
        self.QUERY = f"SELECT `name` FROM `profile_mapper` WHERE `profile_uid` = '{profile_uid}';"
        
        
    def return_query(self):
        print("(GetMapperNameByUID) QUERY:")
        print(self.QUERY)
        return self.QUERY