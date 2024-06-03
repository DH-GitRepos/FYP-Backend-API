class InsertTaggedFaceToLibraryImage():
    def __init__(self, timestamp, face_id, uid):
        self.TIMESTAMP = timestamp
        self.FACE_ID = face_id
        self.UID = uid
        self.QUERY = f"INSERT INTO `image_library_tagged_faces` (`img_name`, `face_id`, `profile_uid`) VALUES ('{self.TIMESTAMP}', '{self.FACE_ID}', '{self.UID}');"
                
        
    def return_query(self):
        print("(InsertTaggedFaceToLibraryImage) QUERY:")
        print(self.QUERY)
        return self.QUERY