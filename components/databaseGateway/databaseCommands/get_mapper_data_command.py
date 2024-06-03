class GetMapperData():
    def __init__(self):
        self.QUERY = f"SELECT `profile_uid`, `name` FROM `profile_mapper`;"
        
        
    def return_query(self):
        print("(GetMapperData) QUERY:")
        print(self.QUERY)
        return self.QUERY