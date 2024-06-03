class GetAllTaggedImagesFromLibraryByUID():
    def __init__(self, uid):
        self.UID = uid
        self.QUERY = f"SELECT `img_name` FROM `image_library_tagged_faces` WHERE `profile_uid` = '{self.UID}';"
        
        
    def return_query(self):
        print("(GetAllTaggedImagesFromLibraryByUID) QUERY:")
        print(self.QUERY)
        return self.QUERY