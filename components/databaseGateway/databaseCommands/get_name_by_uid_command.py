class GetNameByUID():
    def __init__(self, uid):
        self.UID = uid
        self.QUERY = f"SELECT `name` FROM `profile_mapper` WHERE `profile_uid` = '{self.UID}';"
        
        
    def return_query(self):
        print("(GetNameByUID) QUERY:")
        print(self.QUERY)
        return self.QUERY