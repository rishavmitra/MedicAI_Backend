from django.db import models
from db_connections import db

# Create your models here.
user_table = db['User_Table']
user_data_collection = db['User_Metadata']

user_chats = db['User_Chats']