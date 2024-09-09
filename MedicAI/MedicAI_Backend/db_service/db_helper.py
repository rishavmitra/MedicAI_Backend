import gridfs
from db_connections import db
from ..models import user_data_collection,user_table,user_chats,session_ids


def user_data(**kwargs):
    data = user_table.count_documents({"UserID":kwargs["UserId"]})

    if data == 0:
        record = {"UserID":kwargs["UserId"],"SessionId":kwargs["SessionId"]}
        user_table.insert_one(record)

    if "file_object_id" in kwargs:

        record = {"UserID":kwargs["UserId"],"file_object_id":kwargs["file_object_id"],"SessionId":kwargs["SessionId"]}

        res = user_data_collection.insert_one(record)

   
def upload_document(UserId,file,SessionId):
    try:
        data = file.read()
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

def upload_chat(user_id,user_message, system_message, timestamp,session_id):

    user_data(UserId=user_id)
    record = {'UserID':user_id,'UserMessage':user_message,'SystemMessage':system_message,'timestamp':timestamp,'SessionId':session_id}
    user_chats.insert_one(record)

    return {'Response':True,'Message':'Message stored successfully'}

def upload_sessions(session_id,user_id):
    user_data(UserId=user_id)
    record = {'SessionId':session_id,'UserID':user_id}
    session_ids.insert_one(record)

    return {'Response':True,'Message':'Session Stored Succesfully'}