class InsertDetectionData():
    def __init__(self, detection_data):
        self.DETECTION_DATA = detection_data
        self.FACE_ID = None
        self.TIMESTAMP = None
        self.FACE_UID = None
        self.BB_X = None
        self.BB_Y = None
        self.BB_W = None
        self.BB_H = None
        self.FACE_DATA = None
        self.QUERY = None
        
        
    def return_query(self):
        self.FACE_ID = self.DETECTION_DATA['id']
        self.TIMESTAMP = self.DETECTION_DATA['timestamp']
        self.FACE_UID = self.DETECTION_DATA['face_uid']
        self.BB_X = self.DETECTION_DATA['bounding_box']['x']
        self.BB_Y = self.DETECTION_DATA['bounding_box']['y']
        self.BB_W = self.DETECTION_DATA['bounding_box']['w']
        self.BB_H = self.DETECTION_DATA['bounding_box']['h']
        self.FACE_DATA = self.DETECTION_DATA['face_data']
        
        self.QUERY = f"INSERT INTO `detection_data` (`face_id`, `timestamp`, `face_uid`, `bounding_box_x`, `bounding_box_y`, `bounding_box_w`, `bounding_box_h`, `face_data`) VALUES ('{self.FACE_ID}', '{self.TIMESTAMP}', '{self.FACE_UID}', '{self.BB_X}', '{self.BB_Y}', '{self.BB_W}', '{self.BB_H}', '{self.FACE_DATA}');"
        
        print("(InsertDetectionData) QUERY:")
        print(self.QUERY)
        return self.QUERY