class InsertUploadedImageData():
    def __init__(self, image_data):
        self.DETECTION_DATA = image_data
        self.TIMESTAMP = None
        self.FILENAME = None
        self.FILE_W = None
        self.FILE_H = None
        self.NUM_FACES = None
        self.IMG_FORMAT = None
        self.QUERY = None
        
        
    def return_query(self):
        self.TIMESTAMP = self.DETECTION_DATA['timestamp']
        self.FILENAME = self.DETECTION_DATA['file_name']
        self.FILE_W = self.DETECTION_DATA['file_width']
        self.FILE_H = self.DETECTION_DATA['file_height']
        self.NUM_FACES = self.DETECTION_DATA['num_faces_detected']
        self.IMG_FORMAT = self.DETECTION_DATA['img_format']
        
        self.QUERY = f"INSERT INTO `uploaded_image_data` (`timestamp`, `file_name`, `file_width`, `file_height`, `num_faces_detected`, `img_format`) VALUES ('{self.TIMESTAMP}', '{self.FILENAME}', '{self.FILE_W}', '{self.FILE_H}', '{self.NUM_FACES}', '{self.IMG_FORMAT}');"
        
        print("(InsertUploadedImageData) QUERY:")
        print(self.QUERY)
        return self.QUERY