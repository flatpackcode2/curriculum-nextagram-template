from models.base_model import BaseModel
from flask import flash
import peewee as pw
from models.user import User


class Image(BaseModel):
    filename = pw.CharField(unique=True)
    # profile_pic=pw.BooleanField(default=False)
    user = pw.ForeignKeyField(User, backref='images', null=False)