class InitialiseDatabase():
    def __init__(self):
        self.SETUP_QUERIES = [
            "CREATE DATABASE IF NOT EXISTS `fr_image_library` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;",
            "USE `fr_image_library`;",
            ]
        
    def return_query(self):
        print("(InitialiseDatabase) QUERY:")
        print(self.QUERY)
        return self.QUERY