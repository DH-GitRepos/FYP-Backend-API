class InsertTmpProfileToFRDB():
    def __init__(self, tmp_profile):
        self.TMP_PROFILE = tmp_profile
        self.UID = None
        self.SRC = None
        self.QUERY = None
        
        
    def return_query(self):
        self.UID = self.TMP_PROFILE["uid"]
        self.SRC = self.TMP_PROFILE["src"]
        
        self.QUERY = f"INSERT INTO `profile_tmp_index_frdb` (`profile_tmp_uid`, `profile_tmp_src`) VALUES ('{self.UID}', '{self.SRC}');"
        
        print("(InsertTmpProfileToFRDB) QUERY:")
        print(self.QUERY)
        return self.QUERY