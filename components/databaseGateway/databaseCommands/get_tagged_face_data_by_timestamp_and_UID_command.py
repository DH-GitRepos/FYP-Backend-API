class GetTaggedFaceDataByTimestampAndUID():
    def __init__(self, timestamp, uid):
        self.TIMESTAMP = timestamp
        self.UID = uid
        self.QUERY = f"SELECT * FROM `image_library_tagged_faces` WHERE `img_name` = '{self.TIMESTAMP}' AND `profile_uid` = '{self.UID}';"
        
        
    def return_query(self):
        print("(GetTaggedFaceDataByTimestampAndUID) QUERY:")
        print(self.QUERY)
        return self.QUERY