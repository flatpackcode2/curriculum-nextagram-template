from models.base_model import BaseModel
import peewee as pw
from models.user import User
from config import S3_LOCATION, DEFAULT_IMAGE
from playhouse.hybrid import hybrid_property

class Image(BaseModel):
    filename = pw.CharField(null=True)
    # profile_pic=pw.BooleanField(default=False)
    user = pw.ForeignKeyField(User, backref='images')

    @hybrid_property
    def image_url(self):
        return S3_LOCATION + self.filename