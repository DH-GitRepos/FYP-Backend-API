class GetTmpSrcByUID():
    def __init__(self, uid):
        self.UID = uid
        self.QUERY = f"SELECT `profile_tmp_src` FROM `profile_tmp_index_frdb` WHERE `profile_tmp_uid` = '{self.UID}';"
        
        
    def return_query(self):
        print("(GetTmpSrcByUID) QUERY:")
        print(self.QUERY)
        return self.QUERY