class GetTaggedImageByTimestamp():
    def __init__(self, timestamp):
        self.TIMESTAMP = timestamp
        self.QUERY = f"SELECT `img_name` FROM `image_library_tagged_faces` WHERE `img_name` = '{self.TIMESTAMP}';"
        
        
    def return_query(self):
        print("(GetTaggedImageByTimestamp) QUERY:")
        print(self.QUERY)
        return self.QUERY