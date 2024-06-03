class RemoveTmpProfileByUID():
    def __init__(self, uid):
        self.UID = uid
        self.QUERY = f"DELETE FROM `profile_tmp_index_frdb` WHERE `profile_tmp_uid` = '{self.UID}';"
        
        
    def return_query(self):
        print("(RemoveTmpProfileByUID) QUERY:")
        print(self.QUERY)
        return self.QUERY