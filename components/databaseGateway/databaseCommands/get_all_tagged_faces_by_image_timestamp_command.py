class GetAllTaggedFacesByImageTimestamp():
    def __init__(self, timestamp):
        self.TIMESTAMP = timestamp
        self.QUERY = f"SELECT `profile_uid` FROM `image_library_tagged_faces` WHERE `img_name` = '{self.TIMESTAMP}';"
        
        
    def return_query(self):
        print("(GetAllTaggedFacesByImageTimestamp) QUERY:")
        print(self.QUERY)
        return self.QUERY