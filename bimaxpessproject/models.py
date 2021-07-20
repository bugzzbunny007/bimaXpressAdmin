from fireo.models import Model
from fireo.fields import *

class Hospitals(Model):
    name = TextField()
    
class InsuranceCompany_or_TPA(Model):
    image = TextField()

class Cases(Model):
    status = TextField()
    test = TextField()
    hospitals = NestedModel(Hospitals)
    insurance = NestedModel(InsuranceCompany_or_TPA)

class hospital_details(Model):
    name = TextField()
    Date_of_Admission = TextField()
    cases = NestedModel(Cases)

class patient_details(Model):
    Name = TextField()
    Insurance_Company = TextField()
    cases = NestedModel(Cases)