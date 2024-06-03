import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import queue
import threading
import uuid
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS # pip install -U flask-cors

# IMPORT COMPONENT CLASSES
from components.log_mgr_class import LogManager
from components.cleanup_manager_class import CleanupManager
from components.data_manager_class import DataManager
from components.library_manager_class import LibraryManager
from components.mapper_manager_class import MapperManager
from components.df_detection_manager_class import DFDetectionManager
from components.frdb_manager_class import FRDBManager
from components.profile_manager_class import ProfileManager
from components.databaseGateway.IDatabaseGatewayFacade import IDatabaseGatewayFacade

# IMPORT ENDPOINT CLASSES
from endpoints.upload_endpoint_class import UploadEndpoint
from endpoints.tag_endpoint_class import TagEndpoint
from endpoints.library_endpoint_class import LibraryEndpoint
from endpoints.image_endpoint_class import ImageEndpoint
from endpoints.find_endpoint_class import FindEndpoint

# ENABLING THIS WILL WIPE ALL NON-STATIC FILES ON RESTART
# - All uploaded files, profiles, database table content will be deleted
# - creating a clean slate
CLEANUP_ON_START = False

# INITIALISE CLASSES
LOG_MGR = LogManager()
DBI = IDatabaseGatewayFacade(LOG_MGR)
CLN_MGR = CleanupManager(DBI)
DATA_MGR = DataManager(LOG_MGR)
LIB_MGR = LibraryManager(LOG_MGR, DBI)
MAP_MRG = MapperManager(LOG_MGR, DBI)
DET_MGR = DFDetectionManager(LOG_MGR, DATA_MGR, DBI)
PROF_MGR = ProfileManager(LOG_MGR, MAP_MRG, LIB_MGR, DATA_MGR, DBI)
FRDB_MGR = FRDBManager(LOG_MGR, DATA_MGR, DET_MGR, MAP_MRG, DBI)
# Update circular dependency properties
PROF_MGR.set_frdb_mgr(FRDB_MGR)
FRDB_MGR.set_prof_mgr(PROF_MGR)

if CLEANUP_ON_START:
    CLN_MGR.clean_up_files()
    CLN_MGR.clean_up_database()

# SET UP LOGGING ##############################################################

LOG_MGR.set_log_type('api') # set the log type to 'api' before checking if the log file exists
LOG_MGR.create_log_files()

# INITIALISE THE API ##########################################################

LOG_MGR.log("\n=============================", "off")    
LOG_MGR.log("----- INITIALISING API ------", "off")    
LOG_MGR.log("=============================\n", "off")

# Ensure there's a folder to save uploaded images
FILE_PATH = os.path.dirname(os.path.abspath(__file__)) 
TMP_PROFILE_DATA_PATH = f"{FILE_PATH}\\profiles\\tmp\\"
IMAGE_LIBRARY_PATH = f"{FILE_PATH}\\library\\images\\"

# set up the uploads folder   
UPLOAD_FOLDER = f"{FILE_PATH}/uploads/"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# INITIALISE DATABASE... TO DO

# SET UP THE API ##############################################################

FR_API = Flask(__name__)
CORS(FR_API)  # Enable CORS for all routes
FR_API.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a queue to hold API requests
TASK_QUEUE = queue.Queue()
# Create a dictionary to store the results of tasks
TASK_RESULTS = {}

# Worker function to process tasks in the queue
def worker():
    while True:
        task_id, task = TASK_QUEUE.get()
        if task is None: # Stop the worker when it receives a None task
            break
        func, args, kwargs = task
        result = func(*args, **kwargs)
        TASK_QUEUE.task_done()
        # Store the result of the task
        TASK_RESULTS[task_id] = result

# Start the worker thread
worker_thread = threading.Thread(target=worker)
worker_thread.start()
    
LOG_MGR.log("\n=============================", "off")    
LOG_MGR.log("------ API INISIALISED ------", "off")    
LOG_MGR.log("=============================\n", "off")

# DEFINE ENDPOINTS ############################################################
# DEFINE: "root" route ########################################################

@FR_API.route('/')
def root():
    return "Welcome to the Face Recognition API by Darren Halpin (20122838)."

# DEFINE: "upload" route ######################################################    

@FR_API.route('/upload', methods=['POST'])
def upload_route():
    # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        else:
            # Get the file from the POST request
            file = request.files['file'] if 'file' in request.files else None  # Get the file here, in the request context
            
            # If the user does not select a file, the browser submits an empty part without a filename
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400 
        
            else:                
                upload_ep = UploadEndpoint(file, UPLOAD_FOLDER, TMP_PROFILE_DATA_PATH, FR_API, LOG_MGR, DATA_MGR, DET_MGR, FRDB_MGR, PROF_MGR, MAP_MRG, LIB_MGR)
                # Generate a unique task id
                task_id = str(uuid.uuid4())
                # Add the task to the queue
                TASK_QUEUE.put((task_id, (upload_ep.upload_route, (), {})))
                # Wait for the task to complete
                TASK_QUEUE.join()    
                # Get the result of the task
                result = TASK_RESULTS.pop(task_id, None)
                return jsonify(result), 200
        
        
# DEFINE: "tag" route #########################################################

@FR_API.route('/tag', methods=['POST'])
def tag_route():
    data = request.get_json()  # Get the data here, in the request context
    tag_ep = TagEndpoint(data, LOG_MGR, PROF_MGR, MAP_MRG, LIB_MGR)
    task_id = str(uuid.uuid4())
    TASK_QUEUE.put((task_id, (tag_ep.tag_route, (), {})))
    TASK_QUEUE.join()
    result = TASK_RESULTS.pop(task_id, None)
    return jsonify(result), 200


# DEFINE: "library" route #####################################################

@FR_API.route('/library', methods=['POST'])
def library_route():
    data = request.get_json()  # Get the data here, in the request context
    library_ep = LibraryEndpoint(data, LOG_MGR, LIB_MGR)
    task_id = str(uuid.uuid4())
    TASK_QUEUE.put((task_id, (library_ep.library_route, (), {})))
    TASK_QUEUE.join()
    result = TASK_RESULTS.pop(task_id, None)
    return jsonify(result), 200
  
  
# DEFINE: "image" route #######################################################

@FR_API.route('/image', methods=['POST'])
def image_route():
    data = request.get_json()  # Get the data here, in the request context
    image_ep = ImageEndpoint(data, LOG_MGR, MAP_MRG, LIB_MGR)
    task_id = str(uuid.uuid4())
    TASK_QUEUE.put((task_id, (image_ep.image_route, (), {})))
    TASK_QUEUE.join()
    result = TASK_RESULTS.pop(task_id, None)
    
    LOG_MGR.log(f"\nAPI('/image'): API returning status: {result['content']['status']}, {result['content']['message']}")
    
    if result["content"]["status"] == 400:
        return jsonify(result), 400
    else:   
        return jsonify(result), 200
        

# DEFINE: "find" route ########################################################

@FR_API.route('/find', methods=['POST'])
def find_route():
    data = request.get_json()  # Get the data here, in the request context
    find_ep = FindEndpoint(data, LOG_MGR, MAP_MRG, LIB_MGR)
    task_id = str(uuid.uuid4())
    TASK_QUEUE.put((task_id, (find_ep.find_route, (), {})))
    TASK_QUEUE.join()
    result = TASK_RESULTS.pop(task_id, None)
    
    return jsonify(result), 200


# DEFINE: "image-library" route ########################################################

@FR_API.route('/image-library/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(IMAGE_LIBRARY_PATH, filename)


# DEFINE: "shutdown" route ########################################################

@FR_API.route('/shutdown', methods=['GET'])
def shutdown():
    print("Shutting down gracefully...")
    TASK_QUEUE.put((None, None))  # Add a None task to the queue to stop the worker
    
    # shutdown_func = request.environ.get('werkzeug.server.shutdown')
    # if shutdown_func is None:
    #     raise RuntimeError('Not running with the Werkzeug Server')
    # shutdown_func()
    
    # def stop_server():
    #     time.sleep(3)
    #     os.kill(os.getpid(), signal.SIGINT)

    # threading.Thread(target=stop_server).start()
    
    # return 'Server shutting down...'
    return "Queue killed..."

# DEFINE: match route #########################################################

if __name__ == '__main__':
    FR_API.run(debug=True)
