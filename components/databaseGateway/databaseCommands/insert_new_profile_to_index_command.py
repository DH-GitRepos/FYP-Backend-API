class InsertNewProfileToIndex():
    def __init__(self, profile_uid):
        self.UID = profile_uid
        self.QUERY = f"INSERT INTO `profile_index` (`profile_uid`) VALUES ('{self.UID}');"
                
        
    def return_query(self):
        print("(InsertNewProfileToIndex) QUERY:")
        print(self.QUERY)
        return self.QUERY