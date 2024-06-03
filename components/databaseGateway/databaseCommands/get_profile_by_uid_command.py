class GetProfileByUID():
    def __init__(self, profile_uid):
        self.UID = profile_uid
        self.QUERY = f"SELECT * FROM `profile_index` WHERE `profile_uid` = '{profile_uid}';"
        
        
    def return_query(self):
        print("(GetProfileByUID) QUERY:")
        print(self.QUERY)
        return self.QUERY