import gridfs
from db_connections import db
from ..models import user_data_collection,user_table


def user_data(**kwargs):
    if "file_object_id" in kwargs:

        data = user_table.find({"UserID":kwargs["UserId"]})

        if data.retrieved == 0:
            record = {"UserID":kwargs["UserId"]}
            user_table.insert_one(record)

        record = {"UserID":kwargs["UserId"],"file_object_id":kwargs["file_object_id"]}

        res = user_data_collection.insert_one(record)

def upload_document(UserId,file):
    try:
        data = file.read()
        fs = gridfs.GridFS(db)

        file_object_id = fs.put(data,filename=file.name)

        user_data(UserId = UserId,file_object_id=file_object_id)

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

