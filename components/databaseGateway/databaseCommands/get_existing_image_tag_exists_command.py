class GetExistingImageTagExists():
    def __init__(self, timestamp, face_id, uid):
        self.TIMESTAMP = timestamp
        self.FACE_ID = face_id
        self.UID = uid
        self.QUERY = f"SELECT * FROM `image_library_tagged_faces` WHERE `img_name` = '{self.TIMESTAMP}' AND `face_id` = '{self.FACE_ID}' AND `profile_uid` = '{self.UID}';"
        
       
    def return_query(self):
        print("(GetExistingImageTagExists) QUERY:")
        print(self.QUERY)
        return self.QUERY