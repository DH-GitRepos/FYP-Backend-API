import os
import time
from PIL import Image
from deepface import DeepFace as df


class DFDetectionManager:
    def __init__(self, logging_manager, data_manager, database_interface):
        self.BACKENDS = [        # CNN MODELS FOR DETECTION TASKS
            'opencv',         # [0] faster
            'ssd',            # [1] faster
            'mtcnn',          # [2] slower, but more accurate
            'retinaface',     # [3] slower, but more accurate
            'mediapipe',      # [4]
            'yolov8',         # [5]
            'yunet',          # [6]
            'fastmtcnn',      # [7]
            'dlib'            # [8] 'dlib' is not a CNN model, but a traditional CV model
        ]

        self.MODELS = [          # FR MODELS
            "VGG-Face",       # [0] 4096 data points (default) (Oxford Uni)
            "Facenet",        # [1] 128 data points (Google)
            "Facenet512",     # [2] 521 data points (BEST PERFORMING @ 99.65%)
            "OpenFace",       # [3] 128 data points (Carnegie Mellon Uni)
            "DeepFace",       # [4] 4096 data points (Facebook)
            "DeepID",         # [5] 160 data points
            "ArcFace",        # [6] 512 data points
            "SFace",          # [7] 128 data points
        ]

        self.METRICS = [         # SIMILARITY CALCULATION METRICS FOR FACE RECOGNITION
            "cosine",       # [0] (default)
            "euclidean",    # [1]
            "euclidean_l2"  # [2] Best (most stable) metric, with the Facenet512 model
        ]

        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__)) 
        self.SAVE_PATH = f"{self.FILE_PATH}\\..\\profiles\\tmp\\"
        self.PREDICTOR_PATH = f"{self.FILE_PATH}\\tasks\\shape_predictor_68_face_landmarks.dat"
        
        self.LOG_MGR = logging_manager
        self.DATA_MGR = data_manager
        self.DBI = database_interface


    def df_detect_faces(self, image_file, img_id, timestamp):
        self.LOG_MGR.log(f"DF_DETECTION_MANAGER(df_detect_faces): Incoming data:\n\tIMG FILE: {image_file}, IMG ID: {img_id}, TIMESTAMP: {timestamp}")
        
        img_format = image_file.split('.')[-1]
        
        # set the path to the temporary image folder    
        
        try:    
            face_objs = df.extract_faces(img_path=image_file,
                                        detector_backend=self.BACKENDS[3], # retinaface seems to give the best results
                                        align=True 
                                        )
            
            # face_objs - contains a list of dictioanries, each containing the following keys:
            # 'facial_area', tuple of (x, y, w, h, left_eye, right_eye)
            # 'confidence', float representing the confidence score of the detection
            # 'face', numpy ndarray representing the detected face region. Pixels in BGR order.
            
            faces_list = []
            
            face_id = 1
            # Loop through the detected faces and extract the face data
            for item in face_objs:
                face_data = {
                    'id': face_id,
                    'timestamp': timestamp,
                    'face_uid': self.DATA_MGR.create_uuid(),
                    'img_id': img_id,
                    'bounding_box': item['facial_area'],
                    'face_data': item['face']
                    }
                
                
                faces_list.append(face_data)
                ### ADD THE FACE DATA TO THE DATABASE ###
                self.DBI.insert_detection_data(face_data)
                
                face_id += 1
            
            
            # Loop through the faces and crop the image to extract the face    
            for face in faces_list:            
                # Open the image using PIL.
                image_to_crop = Image.open(image_file)
                
                # Extract the bounding box coordinates.
                x = int(face['bounding_box']['x'])
                y = int(face['bounding_box']['y'])
                w = int(face['bounding_box']['w'])
                h = int(face['bounding_box']['h'])

                # Define the coordinates of the bounding box.
                left = int(x)
                upper = int(y)
                right = int(x+w)
                lower = int(y+h)

                # Define the coordinates of the rectangular section to crop.
                # The coordinates are defined as a tuple of (left, upper, right, lower).
                crop_rectangle = (left, upper, right, lower)
                
                # Crop the image using the crop_rectangle coordinates.
                cropped_img = image_to_crop.crop(crop_rectangle)
                image_to_crop.close()  # Close the main image        
                
                # Save the cropped image to a new file.               
                # tmpImgPath = f"{savePath}tmp_cropped_image.{img_format}"
                tmpImgPath = f"{self.SAVE_PATH}{timestamp}-{face['id']}.{img_format}"
                cropped_img.save(tmpImgPath)
                cropped_img.close()  # Close the cropped image  
                
                # Add a small delay
                time.sleep(0.1)
                
        except ValueError as e:
            self.LOG_MGR.log(f"ERROR: ->\n{e}\n\n")
            faces_list = []
        
        self.LOG_MGR.log(f"\tRETURNING(df_detect_faces) -> FACES LIST: {faces_list}\n")
        return faces_list


    def df_verify_faces(self, face_path_1, face_path_2):
        self.LOG_MGR.log(f"DF_DETECTION_MANAGER(df_verify_faces): Incoming data:\n\tFACE 1: {face_path_1}, FACE 2: {face_path_2}")
        
        # Check if the image file at face_path_1 exists
        if not os.path.isfile(face_path_1):
            self.LOG_MGR.log(f"\tERROR::DF_DETECTION_MANAGER(df_verify_faces):\n\tImage file at {face_path_1} does not exist.")
            return
        else:
            self.LOG_MGR.log(f"\tDF_DETECTION_MANAGER(df_verify_faces):\n\tImage(1) file at {face_path_1} exists.")
        
        # Check if the image file at face_path_2 exists
        if not os.path.isfile(face_path_2):
            self.LOG_MGR.log(f"\tERROR::DF_DETECTION_MANAGER(df_verify_faces):\n\tImage file at {face_path_2} does not exist.")
            return
        else:
            self.LOG_MGR.log(f"\tDF_DETECTION_MANAGER(df_verify_faces):\n\tImage(2) file at {face_path_2} exists.")
        
        # Check if the image file at face_path_1 is a valid image file
        try:
            Image.open(face_path_1)
        except IOError:
            self.LOG_MGR.log(f"\tERROR::DF_DETECTION_MANAGER(df_verify_faces):\n\tImage file at {face_path_1} is not a valid image file.")
            return
        
        # Check if the image file at face_path_2 is a valid image file
        try:
            Image.open(face_path_2)
        except IOError:
            self.LOG_MGR.log(f"\tERROR::DF_DETECTION_MANAGER(df_verify_faces):\n\tImage file at {face_path_2} is not a valid image file.")
            return
        
        # Verify the similarity between the two faces
        try:
            # FACE VERIFICATION
            result = df.verify(img1_path=face_path_1, 
                            img2_path=face_path_2,
                            detector_backend=self.BACKENDS[4], # mediapipe
                            model_name=self.MODELS[2], 
                            distance_metric=self.METRICS[2])
            
            # print(result)
            # print(result["verified"])
            # print(result["distance"])
            
        except Exception as e:
            self.LOG_MGR.log(f"\tERROR::DF_DETECTION_MANAGER(df_verify_faces): Exception occurred while verifying faces:\n\t{e}")
            return
        
        self.LOG_MGR.log(f"\tRETURNING(df_verify_faces) -> RESULT: {result}\n")
        return result["verified"]
