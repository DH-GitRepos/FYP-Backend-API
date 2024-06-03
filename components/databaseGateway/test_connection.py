import sys
import os
import json

# from query_executor import QueryExecutor
from IDatabaseGatewayFacade import IDatabaseGatewayFacade

# Get the directory that this script is in
script_dir = os.path.dirname(os.path.realpath(__file__))
# Add the parent directory of the script to the system path
sys.path.append(os.path.abspath(os.path.join(script_dir, '..')))
from log_mgr_class import LogManager

LOG_MGR = LogManager()
DBC = IDatabaseGatewayFacade(LOG_MGR)
# DBC.test_connection()

################################


# print(f"\nRESULT (Status): {result['status']}")
# print(f"RESULT (Message): {result['status_message']}")
# print(f"RESULT (Rows affected): {result['rows']}")
# print(f"RESULT (Rows affected): {result['affected_rows']}")
################################

# result = DBC.insert_image_to_library("test_image", 0)
#result = DBC.insert_tagged_face_to_library_image("test_image", "test_profile_uid")

# for i in range(0, 10):
#     result = DBC.insert_new_profile_to_index(f"profile_uid-{i}")

# result = DBC.insert_new_name_to_mapper("Fred Bloggs", "test_profile_uid_x")

# result = DBC.insert_tmp_profile_to_frdb("TEST-UID", "TEST-SRC")



# for i in range(0, 10):
#     result = DBC.insert_image_to_library(f"image-{i}", 0)
    
#     print(f"\nRESULT (Status): {result['status']}")
#     print(f"RESULT (Message): {result['status_message']}")
#     print(f"RESULT (Rows affected): {result['rows']}")
#     print(f"RESULT (Rows affected): {result['affected_rows']}")
    
# for i in range(0, 10):
#     result = DBC.insert_new_profile_to_index(f"profile_uid-{i}")
    
#     print(f"\nRESULT (Status): {result['status']}")
#     print(f"RESULT (Message): {result['status_message']}")
#     print(f"RESULT (Rows affected): {result['rows']}")
#     print(f"RESULT (Rows affected): {result['affected_rows']}")    
    
# result = DBC.get_all_images_from_library()
# result = DBC.get_all_profile_uids()

# print(f"\nRESULT (Status): {result['status']}")
# print(f"RESULT (Message): {result['status_message']}")
# print(f"RESULT (Rows affected): {result['rows']}")
# print(f"RESULT (Rows affected): {result['affected_rows']}")

#############################

# data = DBC.get_all_profile_uids()

# print(f"\nRESULT (Status): {data}")

# return_data = {"profiles": []}

# for item in data['rows']:
#     new_item = {"uid": item[0]}
#     return_data["profiles"].append(new_item)

# return_json = json.dumps(return_data)
# print(return_json)

#############################

request = DBC.get_profile_by_uid("profile_uid-4")
print(request['num_rows'])
print(request)

#print(f"\nRESULT (Status): {request['status']}")
