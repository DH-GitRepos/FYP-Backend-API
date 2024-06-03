class GetAllProfileUIDs():
    def __init__(self):
        self.QUERY = f"SELECT * FROM `profile_index`;"
        
        
    def return_query(self):
        print("(GetAllProfileUIDs) QUERY:")
        print(self.QUERY)
        return self.QUERY