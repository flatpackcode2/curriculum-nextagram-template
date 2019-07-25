from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Donation(BaseModel):
    donation_value = pw.DecimalField()
    recepient_name=pw.CharField(default='unknown')
    donor=pw.ForeignKeyField(User, backref='donations')