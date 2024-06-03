class GetTmpUIDBySrc():
    def __init__(self, src):
        self.SRC = src
        self.QUERY = f"SELECT * FROM `profile_tmp_index_frdb` WHERE `profile_tmp_src` = '{self.SRC}';"
        
        
    def return_query(self):
        print("(GetTmpUIDBySrc) QUERY:")
        print(self.QUERY)
        return self.QUERY