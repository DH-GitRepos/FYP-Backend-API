class UpdateImageTaggedValue():
    def __init__(self, timestamp, status):
        self.TIMESTAMP = timestamp
        self.STATUS = status
        self.QUERY = f"UPDATE `image_library_index` SET `tagged` = '{self.STATUS}' WHERE `img_name` = '{self.TIMESTAMP}';"
        
        
    def return_query(self):
        print("(UpdateImageTaggedValue) QUERY:")
        print(self.QUERY)
        return self.QUERY