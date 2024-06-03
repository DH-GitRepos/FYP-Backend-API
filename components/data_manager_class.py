import numpy as np
import uuid
import time
import base64
import os


class DataManager:
    def __init__(self, logging_manager):
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.LOG_MGR = logging_manager

        
    def create_uuid(self):
        self.LOG_MGR.log(f"DATA_MANAGER(create_uuid)")
        
        new_uuid = str(uuid.uuid4()) # Generate a random UUID
        
        self.LOG_MGR.log(f"\tRETURNING(create_uuid) -> NEW UUID: {new_uuid}\n")
        return new_uuid


    def create_id(self):
        self.LOG_MGR.log(f"DATA_MANAGER(create_id)")
        
        # Create a random Universally Unique Identifier (UUID)
        part_1 = str(uuid.uuid4()) 
        # Milliseconds since the Unix epoch
        part_2 = int(time.time() * 1000)  
        
        # Concatenate the two parts
        joined_str = part_1 + str(part_2) 
        # Convert the string to bytes (required for base64 encoding)
        byte_str = joined_str.encode('utf-8') 
        # Encode the bytes to base64
        id_str = str(base64.b64encode(byte_str)) 
        
        self.LOG_MGR.log(f"\tRETURNING(create_id) -> ID STRING: {id_str}\n")
        return id_str
