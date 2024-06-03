class GetAllImagesFromLibrary():
    def __init__(self):
        self.QUERY = f"SELECT `img_name` FROM `image_library_index`;"
        
        
    def return_query(self):
        print("(GetAllImagesFromLibrary) QUERY:")
        print(self.QUERY)
        return self.QUERY