import sys
import os

# # Get the directory that this script is in
script_dir = os.path.dirname(os.path.realpath(__file__))
# # Add the parent directory of the script to the system path
sys.path.append(os.path.abspath(script_dir))


from query_executor import QueryExecutor

# # Get the directory that this script is in
# script_dir = os.path.dirname(os.path.realpath(__file__))
# # Add the parent directory of the script to the system path
# sys.path.append(os.path.abspath(os.path.join(script_dir, './databaseCommands/')))

from databaseCommands import (InsertImageToLibrary,
                              InsertTaggedFaceToLibraryImage,
                              InsertNewProfileToIndex,
                              InsertNewNameToMapper,
                              InsertTmpProfileToFRDB,
                              InsertDetectionData,
                              InsertUploadedImageData,
                              GetAllImagesFromLibrary,
                              GetImageByTimestamp,
                              GetAllProfileUIDs,
                              GetProfileByUID,
                              GetTmpUIDBySrc,
                              GetTmpSrcByUID,
                              GetMapperNameByUID,
                              GetMapperUIDByName,
                              GetExistingImageTagExists,
                              GetAllTaggedImagesFromLibraryByUID,
                              GetAllTaggedFacesByImageTimestamp,
                              GetTaggedFaceDataByTimestampAndUID,
                              GetTaggedImageByTimestamp,
                              GetMapperData,
                              UpdateImageTaggedValue,
                              RemoveTmpProfileByUID,
                              RemoveTmpProfileBySrc,
                              RemoveProfileFromImage
                              )

class IDatabaseGatewayFacade:
    def __init__(self, logging_manager):
        self.LOG_MGR = logging_manager
        self.Q_EXEC = QueryExecutor(self.LOG_MGR)
   
    def initialise(self):
        pass    
    
    def test_connection(self):
        self.LOG_MGR.set_log_type("db")
        if self.Q_EXEC.test_connection():
            print("Connection successful")
        else:
            print("Connection failed")  
            
            
    def process_query(self, command_object):
        # pass the command objects query property to the query executor
        query = command_object.return_query()
        # execute the query
        result = self.Q_EXEC.execute_query(query)
        return result
    
    
    def clean_database(self):
        result = self.Q_EXEC.clean_database()
        return result
    
    
    ## CRUD OPERATIONS ##
    
    # Create functions
    
    def insert_image_to_library(self, image_name, tagged_bool):
        # instantiate command object for this command (create command objects)
        command_object = InsertImageToLibrary(image_name, tagged_bool)
        # process the query and return the result
        return self.process_query(command_object)

    
    def insert_tagged_face_to_library_image(self, timestamp, face_id, profile_uid):
        command_object = InsertTaggedFaceToLibraryImage(timestamp, face_id, profile_uid)
        return self.process_query(command_object)

    
    def insert_new_profile_to_index(self, profile_uid):
        command_object = InsertNewProfileToIndex(profile_uid)
        return self.process_query(command_object)
    
    
    def insert_new_name_to_mapper(self, name, profile_uid):
        command_object = InsertNewNameToMapper(name, profile_uid)
        return self.process_query(command_object)
    
    
    def insert_tmp_profile_to_frdb(self, tmp_profile):
        command_object = InsertTmpProfileToFRDB(tmp_profile)
        return self.process_query(command_object)
    
    
    def insert_detection_data(self, detection_data):
        command_object = InsertDetectionData(detection_data)
        return self.process_query(command_object)
    
    
    def insert_uploaded_image_data(self, uploaded_image_data):
        command_object = InsertUploadedImageData(uploaded_image_data)
        return self.process_query(command_object)
    
    
    # Read functions
    
    def get_all_images_from_library(self):
        command_object = GetAllImagesFromLibrary()
        return self.process_query(command_object)
    
    
    def get_image_by_timestamp(self, timestamp):
        command_object = GetImageByTimestamp(timestamp)
        return self.process_query(command_object) 
    
    
    def get_all_tagged_images_from_library_by_uid(self, uid):
        command_object = GetAllTaggedImagesFromLibraryByUID(uid)
        return self.process_query(command_object)
    
    
    def get_tagged_image_by_timestamp(self, timestamp):
        command_object = GetTaggedImageByTimestamp(timestamp)
        return self.process_query(command_object)       


    def get_existing_image_tag_exists(self, timestamp, face_id, uid):
        command_object = GetExistingImageTagExists(timestamp, face_id, uid)
        return self.process_query(command_object)


    def get_all_tagged_faces_by_image_timestamp(self, timestamp):
        command_object = GetAllTaggedFacesByImageTimestamp(timestamp)
        return self.process_query(command_object)
    
    
    def get_tagged_face_data_by_timestamp_and_UID(self, timestamp, uid):
        command_object = GetTaggedFaceDataByTimestampAndUID(timestamp, uid)
        return self.process_query(command_object)


    def get_all_profile_uids(self):
        command_object = GetAllProfileUIDs()
        return self.process_query(command_object)
    
    
    def get_profile_by_uid(self, profile_uid):
        command_object = GetProfileByUID(profile_uid)
        return self.process_query(command_object)
    
    
    def get_mapper_data(self):
        command_object = GetMapperData()
        return self.process_query(command_object)
    
    
    def get_mapper_name_by_uid(self, profile_uid):
        command_object = GetMapperNameByUID(profile_uid)
        return self.process_query(command_object)
    
    
    def get_mapper_uid_by_name(self, profile_name):
        command_object = GetMapperUIDByName(profile_name)
        return self.process_query(command_object)
    
    
    def get_tmp_uid_by_src(self, src):
        command_object = GetTmpUIDBySrc(src)
        return self.process_query(command_object)
    
    def get_tmp_src_by_uid(self, uid):
        command_object = GetTmpSrcByUID(uid)
        return self.process_query(command_object)

    # Update functions

    def update_image_tagged_value(self, timestamp, status):
        command_object = UpdateImageTaggedValue(timestamp, status)
        return self.process_query(command_object)


    # Delete functions

    def remove_temp_profile_by_uid(self, uid):
        command_object = RemoveTmpProfileByUID(uid)
        return self.process_query(command_object)
    
    
    def remove_temp_profile_by_src(self, src):
        command_object = RemoveTmpProfileBySrc(src)
        return self.process_query(command_object)
    
    
    def remove_profile_from_image(self, timestamp, face_id, uid):
        command_object = RemoveProfileFromImage(timestamp, face_id, uid)
        return self.process_query(command_object)
