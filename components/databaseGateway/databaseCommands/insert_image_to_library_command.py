class InsertImageToLibrary():
    def __init__(self, image_name, tagged_bool):
        self.IMG_NAME = image_name
        self.TAGGED = tagged_bool
        self.QUERY = f"INSERT INTO `image_library_index` (`img_name`, `tagged`) VALUES ('{self.IMG_NAME}', '{self.TAGGED}');"
        
        
    def return_query(self):
        print("(InsertImageToLibrary) QUERY:")
        print(self.QUERY)
        return self.QUERY