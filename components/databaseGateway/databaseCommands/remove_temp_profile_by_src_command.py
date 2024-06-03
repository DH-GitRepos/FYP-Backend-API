class RemoveTmpProfileBySrc():
    def __init__(self, src):
        self.SRC = src
        self.QUERY = f"DELETE FROM `profile_tmp_index_frdb` WHERE `profile_tmp_src` = '{self.SRC}';"
        
        
    def return_query(self):
        print("(RemoveTmpProfileBySrc) QUERY:")
        print(self.QUERY)
        return self.QUERY