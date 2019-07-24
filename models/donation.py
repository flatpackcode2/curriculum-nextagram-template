from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Donation(BaseModel):
    donation_value = pw.DecimalField()
    recepient=pw.CharField()
    donor=pw.ForeignKeyField(User, backref='donations')