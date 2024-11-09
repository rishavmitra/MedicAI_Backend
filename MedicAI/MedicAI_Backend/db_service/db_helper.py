import gridfs
import io
import fitz
from bson import ObjectId
from db_connections import db
from ..models import user_data_collection,user_table,user_chats,sessions

def user_data(**kwargs):
    data = user_table.count_documents({"UserID":kwargs["UserId"]})
    sess_data = sessions.count_documents({"UserID":kwargs["UserId"],"SessionId":kwargs["SessionId"]})

    if data == 0:
        record = {"UserID":kwargs["UserId"]}
        user_table.insert_one(record)

    if "SessionId" in kwargs and "file_object_id" not in kwargs and sess_data == 0:
        record = {"UserID":kwargs["UserId"],"SessionId":kwargs["SessionId"],'timestamp':kwargs["timestamp"]}
        sessions.insert_one(record)

    if "file_object_id" in kwargs:

        record = {"UserID":kwargs["UserId"],"file_object_id":kwargs["file_object_id"],"SessionId":kwargs["SessionId"]}

        res = user_data_collection.insert_one(record)

   
def upload_document(UserId,file,SessionId,document_obj):
    try:
        text = ''
        data = file.read()

        pdf_stream = io.BytesIO(data)

        # Open the PDF from the stream
        doc = fitz.open(stream=pdf_stream, filetype="pdf")

        # Extract and print text from each page
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text1 = page.get_text("text")  # Extract text in readable format
            text += text1

        # Close the document
        doc.close()

        document_obj.insert_context(text)


        fs = gridfs.GridFS(db)

        file_object_id = fs.put(data,filename=file.name)

        user_data(UserId = UserId,file_object_id=file_object_id,SessionId=SessionId)

        return {'Response': True,'Message':'Upload document successful'}
    except Exception as e:
        print("Error from code: \n"+str(e))
        return {'Response': False,'Message':'Could not upload document'}
    # data = db.fs.files.find_one({"_id":ret})
    # my_id = data["_id"]
    # outputdata= fs.get(ret).read()
    # output = open("xyz1.pdf","wb")
    # output.write(outputdata)
    # output.close()

def upload_chat(user_id,user_message, system_message, timestamp,session_id,SerialNum):

    user_data(UserId=user_id,SessionId=session_id,timestamp=timestamp)
    record = {'UserID':user_id,'UserMessage':user_message,'SystemMessage':system_message,'timestamp':timestamp,'SessionId':session_id,'SerialNum':SerialNum}
    user_chats.insert_one(record)

    return {'Response':True,'Message':'Message stored successfully'}

def upload_sessions(session_id,user_id):
    # user_data(UserId=user_id,SessionId = session_id) # Code not fixed yet

    return {'Response':True,'Message':'Session Stored Succesfully'}

def get_sessions(user_id):
    try:
# Query the session_id collection to find all sessions for the given user
        user_sessions = sessions.find(
            {'UserID': user_id, 'timestamp': {'$exists': True}},
            {'SessionId': 1, 'timestamp': 1, '_id': 0}
        ).sort('timestamp', -1)

        print(user_sessions)
        # Convert cursor to a list for further use
        sessions_list = list(user_sessions)

        # Debugging: Print out the session list
        print(f"Sessions for UserID {user_id}: {sessions_list}")
        
        return sessions_list
    except Exception as e:
        print(f"DB Error: {str(e)}")
        return []

def get_chats(session_id):
    # Fetch chats for the specific session_id
    chats = user_chats.find({"SessionId": session_id})
    return list(chats)




def delete_session(user_id, session_id):
    try:
        # Delete the session document
        session_result = sessions.delete_one({
            'UserID': user_id,
            'SessionId': session_id
        })

        # Delete related chats for the session
        chats_result = user_chats.delete_many({
            'UserID': user_id,
            'SessionId': session_id
        })

        # Delete related metadata (if any)
        metadata_result = user_data_collection.delete_many({
            'UserID': user_id,
            'SessionId': session_id
        })

        # Check if the session was deleted successfully
        if session_result.deleted_count > 0:
            print(f"Session {session_id} deleted successfully for UserID {user_id}.")
            print(f"Deleted {chats_result.deleted_count} chats related to session {session_id}.")
            print(f"Deleted {metadata_result.deleted_count} metadata records related to session {session_id}.")
            return True
        else:
            print(f"No session found with ID {session_id} for UserID {user_id}.")
            return False
    except Exception as e:
        print(f"DB Error: {str(e)}")
        return False


