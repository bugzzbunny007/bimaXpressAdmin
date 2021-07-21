from django.shortcuts import render, redirect
from django import http
from django.urls import path
from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponse, request
from django.core.paginator import Paginator
from fireo.queries import filter_query
# from .decoration import adminuser
from django.core.paginator import Paginator
from .models import *
import os
from .settings import BASE_DIR, EMAIL_BACKEND,EMAIL_PORT, EMAIL_USE_SSL
import fireo
# anish Emailer
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid
import smtplib
from django.contrib.auth.forms import UserCreationForm
from django.core.mail.message import MIMEMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import get_connection

import urllib
import imaplib
import email
import json
# from .sendemail_form import EmailForm
from django.core.mail import send_mail, send_mass_mail, EmailMessage
import re
import datetime
import os
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
# from background_task import background
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from email.mime.message import MIMEMessage
from textwrap import dedent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
import time
from html import escape, unescape
import requests
# database stuff
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(
    os.path.join(BASE_DIR, "serviceAccountKey.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()
databunny = {}
firebaseConfig = {
    "apiKey": "AIzaSyDlZMu8lypZDEhRpMVKlD3JcTuvItFaG2A",
    "authDomain": "bimaxpress-cashless.firebaseapp.com",
    "projectId": "bimaxpress-cashless",
    "storageBucket": "bimaxpress-cashless.appspot.com",
    "messagingSenderId": "577257002368",
    "databaseURL": "https://accounts.google.com/o/oauth2/auth",
    "appId": "1:577257002368:web:489252768c47b398465d65",
    "measurementId": "G-Y8B68GW5YX"
}
mth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()

def postsignIn(request):
    context = {}
    cases_data = []
    counter = 0
    list_status = ['draft',  'Unprocessed', 'query', 'Approved', 'Reject',
                   'Enhance', 'Discharge Approved', 'Settled']
    values = {
        "draft": 0,
        "Unprocessed": 0,
        "query": 0,
        "Approved": 0,
        "Reject": 0,
        "Enhance": 0,
        "Discharge_Approved": 0,
        "Settled": 0
    }
    
    if request.method == "POST":
        email = request.POST.get('email')
        pasw = request.POST.get('pass')
        try:
            user = authe.sign_in_with_email_and_password(email, pasw)
            request.session['email'] = user['email']

        except:
            message = "Invalid Credentials!!Please ChecK your Data"
            return render(request, "login.html", {"message": message})

        docs = db.collection(u'backend_users').where(
            u'email', u'==', user['email']).stream()
        for doc in docs:
            Role = doc.to_dict()
            request.session['role'] = Role['Role']

        if Role['Role'] != 'admin':
            request.session['hospital_email'] = Role['hospital']
            data = Hospitals.collection.fetch()
            for obj in data:
                print("Hospital Name : ", obj.name)
                if(obj.id == request.session['hospital_email']):
                    val = Cases.collection.parent(obj.key).fetch()

                    for i in val:
                        counter = counter+1
                        if(i.status == "done"):
                            print("--------")
                            print("case Number", i.id)
                            print("Status:", i.status)
                            
                            if(i.formstatus == "draft"):
                                values['draft'] += 1
                                
                            if(i.formstatus == "Unprocessed"):
                                values['Unprocessed'] += 1
                                
                            if(i.formstatus == "query"):
                                values['query'] += 1
                                
                            if(i.formstatus == "Approved"):
                                values['Approved'] += 1

                            if(i.formstatus == "Reject"):
                                values['Reject'] += 1
                                
                            if(i.formstatus == "Discharge"):
                                values['Discharge'] += 1
                                
                            if(i.formstatus == "Discharge Approved"):
                                values['Discharge_Approved'] += 1
    
                            if(i.formstatus == "Settled"):
                                values['Settled'] += 1

                            print("formStatus", i.formstatus)
                            print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                            val2 = hospital_details.collection.parent(
                                i.key).fetch()
                            for j in val2:
                                print("Hospital Name : ", j.name)
                                print("Date of Admision:", j.Date_of_Admission)
                                admissiondate = str(j.Date_of_Admission)
                                if(len(admissiondate) > 12):
                                    admissiondate = admissiondate[:-8]
                                    print(admissiondate)

                            val3 = patient_details.collection.parent(
                                i.key).fetch()
                            for m in val3:
                                print("Patient Name : ", m.Name)
                                print("Insurance Company", m.Insurance_Company)
                                if(m.Name) != None:
                                    cases_data.append(
                                        {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name, "company": m.Insurance_Company, "Date": admissiondate})
                else:
                    continue

            print(values)
            request.session['backendcase'] = "case"+str(counter+1)
            context["backcase"] = "case"+str(counter+1)
            context["cases_data"] = cases_data
            context['list_status'] = list_status
            context['values'] = values
            context['hospital_email'] = request.session['hospital_email']
            context['role'] = request.session.get('role')
            context['insurance_company'] = request.session['insurance_company']

            return render(request, "index.html", context)

        else:
            request.session['hospital_email'] = user['email']
            print("this is session",request.session['hospital_email'])
            return redirect("hospital")

def mainpage(request):
    print("got it")
    context = {}
    counter=0
    cases_data = []
    list_status = ['draft',  'Unprocessed', 'query', 'Approved', 'Reject',
                   'Enhance', 'Discharge Approved', 'Settled']
    
    values = {
        "draft": 0,
        "Unprocessed": 0,
        "query": 0,
        "Approved": 0,
        "Reject": 0,
        "Enhance": 0,
        "Discharge_Approved": 0,
        "Settled": 0
    }
    
    print("this is role ", request.session['role'])
    print("hospooiiiiiiiiiiiii",request.session['hospital_email'])
    if request.session['role']  != 'admin':
        data = Hospitals.collection.fetch()
        for obj in data:
            print("OBj Data runnigng")
            print("Hospital Name : ", obj.id)
            if(obj.id == request.session['hospital_email']):
                val = Cases.collection.parent(obj.key).fetch()
                for i in val:
                    counter = counter+1
                    if(i.status == "done"):
                        print("--------")
                        print("case Number", i.id)
                        print("Status:", i.status)

                            
                        if(i.formstatus == "draft"):
                            values['draft'] += 1
                                
                        if(i.formstatus == "Unprocessed"):
                            values['Unprocessed'] += 1
                                
                        if(i.formstatus == "query"):
                               
                            values['query'] += 1
                                
                        if(i.formstatus == "Approved"):
                            values['Approved'] += 1
                                
                        if(i.formstatus == "Reject"):
                            values['Reject'] += 1
                                
                        if(i.formstatus == "Enhance"):
                            values['Enhance'] += 1
                                
                        if(i.formstatus == "Discharge Approved"):
                            values['Discharge_Approved'] += 1
                                
                        if(i.formstatus == "Settled"):
                            values['Settled'] += 1

                        print("formStatus", i.formstatus)
                        print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                        val2 = hospital_details.collection.parent(
                                i.key).fetch()
                        for j in val2:
                                print("Hospital Name : ", j.name)
                                print("Date of Admision:", j.Date_of_Admission)
                                admissiondate = str(j.Date_of_Admission)
                                if(len(admissiondate) > 12):
                                    admissiondate = admissiondate[:-8]
                                    print(admissiondate)

                        val3 = patient_details.collection.parent(
                                i.key).fetch()
                        for m in val3:
                                print("Patient Name : ", m.Name)
                                print("Insurance Company", m.Insurance_Company)
                                if(m.Name) != None:
                                    cases_data.append(
                                        {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name, "company": m.Insurance_Company, "Date": admissiondate})
            else:
                continue

            print(values)

            context["backcase"] = "case"+str(counter+1)
            context["cases_data"] = cases_data
            context['list_status'] = list_status
            context['values'] = values
            context['hospital_email'] = request.session['hospital_email']
            context['role'] = request.session.get('role')
            context['insurance_company'] = request.session['insurance_company']
            return render(request, "index.html", context)
        else:
            print("this is session",request.session['hospital_email'])
            return redirect("hospital")
    else:
        print("this is session",request.session['hospital_email'])
        data = Hospitals.collection.fetch()
        for obj in data:
            print("OBj Data runnigng")
            print("Hospital Name : ", obj.id)
            if(obj.id == request.session['hospital_email']):
                val = Cases.collection.parent(obj.key).fetch()
                for i in val:
                    counter = counter+1
                    if(i.status == "done"):
                        print("--------")
                        print("case Number", i.id)
                        print("Status:", i.status)

                            
                        if(i.formstatus == "draft"):
                            values['draft'] += 1
                                
                        if(i.formstatus == "Unprocessed"):
                            values['Unprocessed'] += 1
                                
                        if(i.formstatus == "query"):
                               
                            values['query'] += 1
                                
                        if(i.formstatus == "Approved"):
                            values['Approved'] += 1
                                
                        if(i.formstatus == "Reject"):
                            values['Reject'] += 1
                                
                        if(i.formstatus == "Enhance"):
                            values['Enhance'] += 1
                                
                        if(i.formstatus == "Discharge Approved"):
                            values['Discharge_Approved'] += 1
                                
                        if(i.formstatus == "Settled"):
                            values['Settled'] += 1

                        print("formStatus", i.formstatus)
                        print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                        val2 = hospital_details.collection.parent(
                                i.key).fetch()
                        for j in val2:
                                print("Hospital Name : ", j.name)
                                print("Date of Admision:", j.Date_of_Admission)
                                admissiondate = str(j.Date_of_Admission)
                                if(len(admissiondate) > 12):
                                    admissiondate = admissiondate[:-8]
                                    print(admissiondate)

                        val3 = patient_details.collection.parent(
                                i.key).fetch()
                        for m in val3:
                                print("Patient Name : ", m.Name)
                                print("Insurance Company", m.Insurance_Company)
                                if(m.Name) != None:
                                    cases_data.append(
                                        {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name, "company": m.Insurance_Company, "Date": admissiondate})
            else:
                continue

            print(values)

            context["backcase"] = "case"+str(counter+1)
            context["cases_data"] = cases_data
            context['list_status'] = list_status
            context['values'] = values
            context['hospital_email'] = request.session['hospital_email']
            context['role'] = request.session.get('role')
            context['insurance_company'] = request.session['insurance_company']
            return render(request, "index.html", context)
        
        


def hospital(request):
    context = {}
    doc_ref = db.collection(u'hospitals').document(request.session['hospital_email'])
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        
        context["hospitals"] = doc.to_dict()
    else:
        print(u'No such document!')
    
    return render(request, 'hospital.html', context)


def hospitalEdit(request):
    context = {}
    doc_ref = db.collection(u'hospitals').document(request.session['hospital_email'])
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        print(type(doc.to_dict()))
        context["hospitals"] = doc.to_dict()
    else:
        print(u'No such document!')

    if request.method == "POST":
        data = request.POST.dict()
        print(data)
        db.collection(u'hospitals').document(
            request.session['email']).update(data)

    return render(request, 'hospitalEdit.html', context)

def plandetails(request):
    context = {}
    doc_ref = db.collection(u'hospitals').document("noureen@gmail.com")
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        print("got document",doc.to_dict())
        context["hospitals"] = doc.to_dict()
    else:
        print(u'No such document!')

    return render(request, 'plandetails.html', context)

def sendData(request):
    context ={}
    if request.method == "POST":
        data = request.POST.dict()
        mystr = str(data['mybtn'])
        context['perticulerAnalyst'] = mystr.split(",")
        print(context)
    return render(request , 'analistEdit.html',context)


def analist(request):
    context= {}
    mylist = []
    docs = db.collection(u'backend_users').where(u'hospital', u'==', request.session['hospital_email']).stream()

    for doc in docs:
        mylist.append(doc.to_dict())
        context ['claimAnalyst'] = mylist
        
    print("list of analyst",mylist)
    
    return render(request, 'analist.html', context)

def analistAdd(request):
    if request.method == "POST":
        data = request.POST.dict()
        data['hospital'] = request.session['email']
        data.pop('csrfmiddlewaretoken')
        print(type(data))
        session = request.session['email']
        print(session)
        db.collection(u'backend_users').document(data['email']).set({
            "email":data['email'],
            "employeeId":data['employeeId'],
            "hospital":request.session['email'],
            "name":data['name'],
            "phone":data['phone'],
            "Role":"claim_analyst"
        })
    return render(request, 'analistAdd.html')

def analistEdit(request):
    if request.method == "POST":
        data = request.POST.dict()
        print(data)
        data.pop('csrfmiddlewaretoken')
        print(request.session['email'])
        db.collection(u'backend_users').document(data['email']).update(data)
    return render(request, 'analistEdit.html')

def doctor(request):
    context= {}
    mylist = []
    docs = db.collection(u'backend_users').where(u'hospitals', "array_contains", request.session['hospital_email']).stream()
    for doc in docs:
        mylist.append(doc.to_dict())
        context ['doctor'] = mylist
    print(context)
    return render(request, 'doctor.html',context)

def sendDataDoctors(request):
    context= {}
    if request.method == "POST":
        data = request.POST.dict()
        print("last ", data)
        mystr = str(data['mybtn'])
        context['perticulerdoctor'] = mystr.split(",")
    return render(request , "doctorEdit.html",context)

def doctorEdit(request):
    if request.method == "POST":
        data = request.POST.dict()
        print(data)
        data.pop('csrfmiddlewaretoken')
        db.collection(u'backend_users').document(data['email']).update(data)

    return render(request, 'doctorEdit.html')

def doctorAdd(request):
    if request.method == "POST":
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        print("Last",data)
        doc_ref = db.collection(u'backend_users').document(data['email'])
        doc = doc_ref.get()
        if doc.exists:
            db.collection(u'backend_users').document(data['email']).update({"hospitals": firestore.ArrayUnion([request.session['email']])})
        else:
            db.collection(u'backend_users').document(data['email']).set({
                "doctorRegistrationNo":data['doctorRegistrationNo'],
                "email":data['email'],
                "name":data['name'],
                "phone":data['phone'],
                "qualification":data['qualification'],
                "speciality":data['speciality'],
                "Role":"doctor",
            })
            db.collection(u'backend_users').document(data['email']).update({"hospitals": firestore.ArrayUnion([request.session['email']])})
        
    return render(request, 'doctorAdd.html')



def EmpanelledCompanies(request):
    context={}
    temp = {}
    empanneled =[]
    res=[]
    print(request.session['hospital_email'])
    doc_ref = db.collection(u'hospitals').document(request.session['hospital_email'])
    doc = doc_ref.get()
    if doc.exists:
        temp = doc.to_dict()
        companies = temp['Empanelled_companies']
        empanneled = list(companies.keys())
        for i in empanneled:
            res.append(i.strip())
        print(res)
        
        images={}
        
        for i in res:
            print("val of i",i)
            doc_ref = db.collection(u'InsuranceCompany_or_TPA').document(f"{i}")
            doc = doc_ref.get()
            if doc.exists:
                img_value = doc.to_dict()
                print(img_value)
                images[doc.id]=(img_value['image'])
        context['images'] = images
    else:
        print(u'No such document!')
        
    print(images)
        
    return render(request, 'empanelledCompanies.html',context)

def sendcompany(request , p):
    context={}
    print("value of P",p)
    # doc_ref = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
    #     u'cases').document(f'{casenumber}').collection("patient_details").document("patient_details")

    doc_ref = db.collection(u'hospitals').document(request.session['hospital_email'])
    doc = doc_ref.get()
    if doc.exists:
        temp = doc.to_dict()
        temp1 = temp['Empanelled_companies']
        gotvalue = {x.replace(' ', ''): v for x, v in temp1.items()}
        print("gotvalue ki value",gotvalue)
        companydata = gotvalue[p]
    print(companydata)
    context['companydata'] = companydata
    context['companyname'] = p
    return render(request, "companyDetails.html" ,context)

def saveinsurancedata(request):
    if request.method == "POST":
        data = request.POST.dict()

    db.collection(u'hospitals').document("bansal@gmail.com").update({
            "Empanelled_companies":{
                data['companyname']:{
                    "Discount":data.get("Discount",""),
                    "Exclusion":data.get("Exclusion",""),
                    "Expiry":data.get("Expiry","")
                }
            }
})
    
    return redirect("EmpanelledCompanies")

def listData(request, p):
    context = {}
    counter=0
    if request.session.get('role') != None:
        list_status = ['draft',  'Unprocessed', 'query', 'Approved', 'Reject',
                       'Enhance', 'Discharge Approved', 'Settled']
        values = {
            "draft": 0,
            "Unprocessed": 0,
            "query": 0,
            "Approved": 0,
            "Reject": 0,
            "Enhance": 0,
            "Discharge_Approved": 0,
            "Settled": 0
        }

        user_data = []
        print("this is value of p", p)
        data = Hospitals.collection.fetch()

        for obj in data:
            counter = counter+1

            if(obj.id == request.session['hospital_email']):
                print("Hospital Name : ", obj.name)
                print("Hospital ID : ", obj.id)
                print("--------------")
                val = Cases.collection.parent(obj.key).fetch()
                for i in val:
                    if(i.status == "done"):
                        print("--------")
                        print("case Number", i.id)
                        print("Status:", i.status)
                        if(i.formstatus == "draft"):
                            values['draft'] += 1
                                
                        if(i.formstatus == "Unprocessed"):
                            values['Unprocessed'] += 1
                                
                        if(i.formstatus == "query"):
                               
                            values['query'] += 1
                                
                        if(i.formstatus == "Approved"):
                            values['Approved'] += 1
                                
                        if(i.formstatus == "Reject"):
                            values['Reject'] += 1
                                
                        if(i.formstatus == "Enhance"):
                            values['Enhance'] += 1
                                
                        if(i.formstatus == "Discharge Approved"):
                            values['Discharge_Approved'] += 1
                                
                        if(i.formstatus == "Settled"):
                            values['Settled'] += 1

                        print("formStatus", i.formstatus)
                        print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                        val2 = hospital_details.collection.parent(
                            i.key).fetch()
                        for j in val2:
                            print("Hospital Name : ", j.name)
                            print("Date of Admision:", j.Date_of_Admission)
                            admissiondate = str(j.Date_of_Admission)
                            if(len(admissiondate) > 12):
                                admissiondate = admissiondate[:-8]
                                print(admissiondate)

                        val3 = patient_details.collection.parent(
                            i.key).fetch()
                        for m in val3:
                            print("Patient Name : ", m.Name)
                            print("Insurance Company", m.Insurance_Company)
                            if(m.Name) != None:
                                user_data.append(
                                    {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name, "company": m.Insurance_Company, "Date": admissiondate})
                else:
                    continue

        print(user_data)
        print(p)
        context["backcase"] = "case"+str(counter+1)
        context['content_data'] = user_data
        context['list_status'] = list_status
        context['values'] = values
        context['hospital_email'] = request.session['hospital_email']
        context['p'] = p

        print(p.upper())
        if p.upper() == "DRAFT":
            context['isdraft'] = True
        else:
            context['isdraft'] = False
            
        if p.upper() == "UNPROCESSED":
             context['isunprocessed'] = True
        else:
            context['isunprocessed'] = False
            

        if p.upper() == "ISSUBMITTED_QUERY":
            context['issubmitted_query'] = True
        else:
            context['issubmitted_query'] = False

        if p.upper() == "QUERY":
            context['isquery'] = True
        else:
            context['isquery'] = False

        if p.upper() == "APPROVED":
            context['isapproved'] = True
        else:
            print("runnnniiiiiiiiiing")
            context['isapproved'] = False

        if p.upper() == "REJECT":
            context['isreject'] = True
        else:
            context['isreject'] = False

        if p.upper() == "ENHANCE":
            context['isenhance'] = True
        else:
            context['isenhance'] = False

        if p.upper() == "DISCHARGE APPROVE":
            context['isdischargeapprove'] = True
        else:
            context['isdischargeapprove'] = False

        if p.upper() == "SETTLED":
            context['issettled'] = True
        else:
            context['issettled'] = False

        return render(request, 'renderCards.html', context)
    else:
        return redirect('login')


def updateunprocess(request):
    context = {}
    casenumber = request.GET.get('data', None)
    flag = 0
    email = ""
    case = ""
    for char in casenumber:
        if char == " ":
            flag = 1
        if flag == 0 and char != ' ':
            email = email+char
        if flag == 1 and char != ' ':
            case = case+char
    try:
        db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(case).update({
            'formstatus': "Unprocessed",
        })
    except:
        db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(case).add({
            'formstatus': "Unprocessed",
        })

    return redirect("mainpage")


def getcasedetail(request):
    context = {}
    
    casenumber = request.GET.get('data')
    print("hosital email",request.session['hospital_email'])
    print(casenumber)
    doc_ref = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
        u'cases').document(f'{casenumber}').collection("patient_details").document("patient_details")
    doc = doc_ref.get()

    if doc.exists:
        a = doc.to_dict()
        print(a)
        context['insurance_company'] = a['Insurance_Company']
        context['patient_name'] = a['Name']
        context['caseid'] = casenumber                      
        context['contact_Number'] = a['Number'] 
        context['doctor_natureOfLiness'] = a['Nature_Of_Illness']
    else:
        print("no data found")

    doc_ref_new = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
        u'cases').document(f'{casenumber}').collection("hospital_details").document("hospital_details")
    doc_new = doc_ref_new.get()

    if doc_new.exists:
        b = doc_new.to_dict()
        print(b)
        # context['admissiondate'] = b['Date_of_Admission']
        # context['treating_doctor'] = b['Treating_Doctor']

    else:
        print("no data found")

    status = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
        u'cases').document(f'{casenumber}')

    formstatus = status.get()
    if formstatus.exists:
        b = formstatus.to_dict()
        print(b)
        context['formstatus'] = b['formstatus']

    else:
        print("no data found o")
    audit = []

    audit_trail = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
        u'cases').document(f'{casenumber}')
    audit_value = audit_trail.get()

    if audit_value.exists:
        b = audit_value.to_dict()
        print(b)
        if len(b) > 3:
            values = b['audit_trail']
            for i in values:    
                x = i.split("+")
                audit.append(x)
            print(audit)
            context['audit'] = audit
            context['hospital_email'] = request.session['hospital_email']
            context['casenumber'] = casenumber
        else:
            print("no data found")
            context['hospital_email'] = request.session['hospital_email']
            context['casenumber'] = casenumber
    else:
        context['hospital_email'] = request.session['hospital_email']
        context['casenumber'] = casenumber


    return render(request, 'caseDetails.html', context)


def updateFormstatus(request, new):
    new_status = ''
    email = ''
    old_status = ''
    case = ''
    flag = 1
    print("update form status", new)
    for char in new:
        if char == '+':
            flag = 0
        if flag == 1:
            new_status = new_status+char
        if char == '*':
            flag = 2
        if char == '&':
            flag = 3
        if flag == 0 and char != '+':
            email = email+char
        if flag == 2 and char != '*':
            old_status = old_status+char
        if flag == 3 and char != '&':
            case = case+char
            
    return HttpResponse("success")


def claimpage1(request):
    if request.session.get('role') != None:
        context = {}
        system = request.GET.get('system', None)
        flag = 0
        email = ''
        case = ''
        for char in system:
            if char == "+":
                flag = 1
            if flag == 0 and char != '+':
                email = email+char
            if flag == 1 and char != '+':
                case = case+char
        print(email)
        print(case)
        bunny = []
        docus = db.collection(u'hospitals').document(email).collection(
            u'cases').where(u'status', u'==', 'done').get()

        for i in docus:
            collections = db.collection('hospitals').document(
                email).collection(u'cases').document(case).collections()
            for collection in collections:
                for doc in collection.stream():
                    databunny[doc.id] = doc.to_dict()
                    bunny.append(doc.to_dict())

        print(databunny)
        context['akey'] = case
        context['email'] = email
        context['bunny'] = bunny
        context['data'] = databunny
        context['system'] = system
        context['role'] = request.session['role']
        context['insurance_company'] = request.session['insurance_company']

        print("cool dude", system)
        
        doc = db.collection('hospitals').document(email).collection('cases').document(case).collection('patient_details').stream()	
        for docs in doc:	
            data = docs.to_dict()	
            print(data)	
            def checkKey(dict, key):	
                if key in dict:	
                    return True	
                else:	
                    return False	
            if checkKey(data, "UrlotherDocuments"):	
                context['UrlotherDocuments'] = data['UrlotherDocuments']	
            else:	
                 context['UrlotherDocuments'] = "https://thumbs.dreamstime.com/z/no-image-available-icon-photo-camera-flat-vector-illustration-132483296.jpg"	
            if checkKey(data, "UrluploadConsultation"):	
                context['UrluploadConsultation'] = data['UrluploadConsultation']	
            else:	
                context['UrluploadConsultation'] = "https://thumbs.dreamstime.com/z/no-image-available-icon-photo-camera-flat-vector-illustration-132483296.jpg"	
            if checkKey(data, "UrluploadPatients"):	
                context['UrluploadPatients'] = data['UrluploadPatients']	
            else:	
                context['UrluploadPatients'] = "https://thumbs.dreamstime.com/z/no-image-available-icon-photo-camera-flat-vector-illustration-132483296.jpg"	
            if checkKey(data, "UrluploadSigned"):	
                context['UrluploadSigned'] = data['UrluploadSigned']	
            else:	
                context['UrluploadSigned'] = "https://thumbs.dreamstime.com/z/no-image-available-icon-photo-camera-flat-vector-illustration-132483296.jpg"
        
        return render(request, 'pageAccordian.html', context)
    else:
        return redirect('login')


def claims(request):
    context = {}
    cases_data = []
    list_status = ['draft',  'Unprocessed', 'query', 'Approved', 'Reject',
                   'Enhance', 'Discharge Approved', 'Settled']
    values = {
        "draft": 0,
        "Unprocessed": 0,
        "query": 0,
        "Approved": 0,
        "Reject": 0,
        "Enhance": 0,
        "Discharge_Approved": 0,
        "Settled": 0
    }
    print(request.session['hospital_email'])
    print(request.session['email'])
    if request.method == "POST":
        email = request.POST.get('email')
        pasw = request.POST.get('pass')
        try:
            user = authe.sign_in_with_email_and_password(email, pasw)
            request.session['email'] = user['email']

        except:
            message = "Invalid Credentials!!Please ChecK your Data"
            return render(request, "login.html", {"message": message})

        docs = db.collection(u'backend_users').where(
            u'Email', u'==', user['email']).stream()
        for doc in docs:
            Role = doc.to_dict()
            request.session['role'] = Role['Role']

        if Role['Role'] != 'admin':
            request.session['hospital_email'] = Role['hospital']
            data = Hospitals.collection.fetch()
            for obj in data:
                print("Hospital Name : ", obj.name)
                if(obj.id == request.session['hospital_email']):
                    val = Cases.collection.parent(obj.key).fetch()

                    for i in val:
                        counter = counter+1
                        if(i.status == "done"):
                            print("--------")
                            print("case Number", i.id)
                            print("Status:", i.status)

                            
                            if(i.formstatus == "draft"):
                                values['draft'] += 1
                                
                            if(i.formstatus == "Unprocessed"):
                                values['Unprocessed'] += 1
                                
                            if(i.formstatus == "query"):
                               
                                values['query'] += 1
                                
                            if(i.formstatus == "Approved"):
                                values['Approved'] += 1
                                
                            if(i.formstatus == "Reject"):
                                values['Reject'] += 1
                                
                            if(i.formstatus == "Enhance"):
                                values['Enhance'] += 1
                                
                            if(i.formstatus == "Discharge Approved"):
                                values['Discharge_Approved'] += 1
                                
                            if(i.formstatus == "Settled"):
                                values['Settled'] += 1

                            print("formStatus", i.formstatus)
                            print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                            val2 = hospital_details.collection.parent(
                                i.key).fetch()
                            for j in val2:
                                print("Hospital Name : ", j.name)
                                print("Date of Admision:", j.Date_of_Admission)
                                admissiondate = str(j.Date_of_Admission)
                                if(len(admissiondate) > 12):
                                    admissiondate = admissiondate[:-8]
                                    print(admissiondate)

                            val3 = patient_details.collection.parent(
                                i.key).fetch()
                            for m in val3:
                                print("Patient Name : ", m.Name)
                                print("Insurance Company", m.Insurance_Company)
                                if(m.Name) != None:
                                    cases_data.append(
                                        {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name, "company": m.Insurance_Company, "Date": admissiondate})
                else:
                    continue

        else:
            request.session['hospital_email'] = user['email']
            print("this is session",request.session['hospital_email'])
            return redirect("hospital")

    print(cases_data)
    context["cases_data"] = cases_data
    return render(request, "cases.html", context)


def logout(request):
    request.session.flush()
    return redirect('login')


def adduser(request):
    context = {}
    context['role'] = request.session.get('role')
    return render(request, 'addaccount.html', context)


def index(request):

    return render(request, 'index.html')


def about(request):
    return HttpResponse("About page bolte")

def addcompany(request):
    if request.method == "POST":
        data = request.POST.dict()
    print(data['imgval'])
    
    return render(request, 'randomCompany.html')

def savefinal(request):
    if request.method == "POST":
        data = request.POST.dict()
    print(data)
    return render(request, 'empanelledCompaniesAdd.html')

def empanelledCompaniesAdd(request):
    
    return render(request, 'empanelledCompaniesAdd.html')

def login(request):
    context = {}
    insurance_company = {}
    message = "Provide Email password to singnIn"
    docs = db.collection(u'InsuranceCompany_or_TPA').stream()
    for doc in docs:
        insurance_company[f'{doc.id}'] = f'{doc.to_dict()}'
    request.session['insurance_company'] = insurance_company
    print(insurance_company)
    context['message'] = message
    context['insurance_company'] = request.session['insurance_company']

    return render(request, 'login.html', context)

def sendmail(request):
    emailId = request.session['hospital_email']
    if request.method == 'POST':
        
        sub = request.POST.get('emailSubject')
        body = request.POST.get('emailBody')

        print(sub)
        print(body)

        list = request.POST.get('sendbtn')
        Bcc =""
        Cc=""
        data = list.split('+')
        companyName = data[0]
        
        case = data[2]
        
        db.collection(u'hospitals').document(data[1]).collection('cases').document(case).update({
            "formstatus":"Unprocessed",
        })
    
        print(companyName)
        print(case)
        companyName = companyName.replace(" ","_")
        companyDetails = db.collection(u'InsuranceCompany_or_TPA').document(companyName).get().to_dict()
        to = companyDetails['email']

        datadir = 'c:/'
        directory = case
        path = os.path.join(datadir,directory)
        os.mkdir(path)
        storage = firebase.storage()

        #consultation forms
        # emailId = 'lbs@gmail.com'
        # case = 'case2'
        patient_details = db.collection(u'hospitals').document(emailId).collection(u'cases').document(case).collection(u'patient_details').document(u'patient_details').get()
        consultArray = patient_details.to_dict()

        x=0
        for urls in consultArray['Consultation_Paper']:
            r =requests.get(urls, allow_redirects=True)
            k = str(x+1)
            x = x+1
            open(path +'/consultation'+k+'.jpg', 'wb').write(r.content)

        # emailId = 'anish@bimaxpress.com'
        # to='anishshende001@gmail.com'

        #aadhar card
        AadharCardFrontUrl = consultArray['Aadhar_Card_Front']
        r =requests.get(AadharCardFrontUrl, allow_redirects=True)
        open(path +'/AadharCardFront.jpg', 'wb').write(r.content)

        AadharCardBackUrl = consultArray['Aadhar_Card_Back']
        r =requests.get(AadharCardBackUrl, allow_redirects=True)
        open(path +'/AadharCardBack.jpg', 'wb').write(r.content)

        #health card 
        healthCardUrl = consultArray['Health_card']
        r =requests.get(healthCardUrl, allow_redirects=True)
        open(path +'/healthCard.jpg', 'wb').write(r.content)

        filesDown = os.listdir(path+'/')
        files = []
        for f in filesDown:
            filePath = path+'/'+f
            files.append(filePath)

        print(files)

        sendemail(emailId,to,sub,body,Bcc,Cc,files)

        return redirect('mainpage')

    

def resendemail(request):
    if request.method == "POST":
        data = request.POST.dict()
    if data['email'] != "":
        authe.send_password_reset_email(data['email'])
    else:
        return redirect("login")
    
    return redirect("login")
   


def get_name(email):
    try:
        name = ''
        for char in email:
            if char == '@':
                return name
            name = name+char
    except:
        return None


def savestatus(request):
    if request.method == "POST":
        data = request.POST.dict()

    print(data)
    city_ref = db.collection(u'hospitals').document(
        request.session['hospital_email']).collection(u'cases').document(data['save'])
    
    print('********************')

    statusVal = data['status'].upper()
    print(statusVal)
    statusArray = city_ref.get().to_dict()['statusimage']['Settled']

    datadir = 'C://'
    directory = data['save']
    # print(directory)
    path = os.path.join(datadir,directory)
    os.mkdir(path)

    for f in statusArray:
        r =requests.get(f, allow_redirects=True)
        k = str(x+1)
        x = x+1
        open(path +'/'+statusVal+k+'.jpg', 'wb').write(r.content)

    filesDown = os.listdir(path+'/')
    files = []
    for f in filesDown:
        filePath = path+'/'+f
        files.append(filePath)

    print('********************')

    try:
        city_ref.update({"audit_trail": firestore.ArrayUnion([data.get(
            'status', "None")+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+data['email_title']])})

        db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(data['save']).update({
            'formstatus': data['status'],
            'settledate': data.get('valuedate', "None"),
            'settleamount': data.get('valueamount', "None"),
            'status': "done"
        })
    except:
        db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(data['save']).set({
            'formstatus': data['status'],
            'settledate': data.get('valuedate', "None"),
            'settleamount': data.get('valueamount', "None"),
            'status': "done"
        })

    fromEmail = request.session['hospital_email']
    
    # sendemail(fromEmail, toEmail, sub, msg, bcc, cc, files)
        
    return redirect("mainpage")

def generateform(request):
    context = {}
    form = ""
    form_data = ""
    flag=0
    email=""
    case=""
    bunny=[]
    if request.method == "POST":
        data = request.POST.dict()
        system = request.POST.get('finalvalue', None)
        print(system)
        for char in system:
            if char == "+":
                flag = 1
            if flag == 0 and char != '+':
                email = email+char
            if flag == 1 and char != '+':
                case = case+char
        print("case value",case)
        print("email value",email)
        
        # They should be populate
        # [{'cost_Of_Implant': '', 'Per_Day_Room_Rent': '123', 'OtherHospitalIfAny': '', 'All_Including_Package': '22', 'ICU_Charges': '22', 'total': '22', 'OT_Charges': '2222', 'Cost_Of_Investigation': '21', 'ProfessionalFeesSurgeon': ''}, {'ExpectedDateOfDelivery': 'dhcbdcb', 'DateofInjury': 'dcbdch', 'Room_Type': 'Delux', 'Days_In_ICU': '32', 'Treating_Doctor': 'Naman Singh Doctor', 'Date_of_Admission': '23/21/2121'}, {'Nature_Of_Illness': 'bahabahba', 'isThisAEmergencyPlannedHospitalization': '', 'Past_History_Of_Present_Ailments': 'bhbhbfhb', 'AsthmaOrCOPDOrBronchitisMonth': '11', 'familyPhysician': '', 'CancerYear': '11', 'If_Other_Treatment_Provide_Details': '12334443', 'RelatedAlimentsYear': '11', 'doctor_releventClinicFindings': 'bhabahbah', 'MandatoryPastHistoryMonth': '11', 'Reported_To_Police': '', 'Date_Of_First_Consultation': '', 'AlcoholOrDrugAbuseYear': '11', 'AsthmaOrCOPDOrBronchitisYear': '11', 'AlcoholOrDrugAbuseMonth': '11', 'RelatedAlimentsMonth': '11', 'HypertensionMonth': '11', 'CancerMonth': '11', 'HeartDiseaseMonth': '11', 'Date_Of_Injury': 'dcbdch', 'patient_details_HealthInsurance': '', 'Injury_Disease_Caused_Due_To_Substance_Abuse_Alcohol_Consumption_': '', 'In_Case_Of_Accident': '', 'Duration_Of_Present_Ailments': 'abahbahb', 'HypertensionYear': '11', 'ICD_Code': 'dchbdcbd', 'HyperlipidemiasYear': '11', 'HeartDiseaseYear': '11', 'doctor_proposedLineOfTreatment': '', 'How_Did_Injury_Occur': 'djcbdcd', 'HyperlipidemiasMonth': '11', 'OtherAliments': '11', 'OsteoarthritisYear': '11', 'doctor_testAlcohol': '', 'MandatoryPastHistoryYear': '11', 'Provision_Diagnosis': 'dhcbdcbdhcb', 'OsteoarthritisMonth': '11'}, {'Number': '9425026255', 'AgeMonth': '22', 'Doctor_ContactNumber': 'baabaabb', 'Attending_Relative_Number': '1122334455', 'Policy_Id': '3233', 'Nature_Of_Illness': 'bahabahba', 'DOB': '22/08/2019', 'EmployeeId': '243', 'Address': 'kyon batau', 'InsuredIdCardNumber': '1234', 'Gender': 'male', 'AgeYear': '', 'Insurance_Company': 'Aditya_Birla_Health_Insurance', 'Occupation': '2444', 'Name': 'Naman Yadav'}]
        
        
        doc_ref = db.collection(u'hospitals').document(email)

        doc = doc_ref.get()
        if doc.exists:
            hospitaldata = doc.to_dict()
        else:
            print(u'No such document!')
        
        collections = db.collection('hospitals').document(
                email).collection(u'cases').document(case).collections()
        for collection in collections:
            for doc in collection.stream():
                databunny[doc.id] = doc.to_dict()
                bunny.append(doc.to_dict())
                
        try:
            if(databunny["patient_details"]["Insurance_Company"]) == "Aditya_Birla_Health_Insurance":
                context['hospitaldata'] = hospitaldata
                context['data'] = databunny
                return render(request, "hdfc.html", context)
            else:
                context['hospitaldata'] = hospitaldata
                context['data'] = databunny
                return render(request, "star.html", context)
        except:
            print("Exception")
            

def saveData(request):
    context = {}
    form = ""
    form_data = ""
    if request.method == "POST":
        data = request.POST.dict()
        system = request.POST.get('save', None)
        form = request.POST.get('last', None)
        if(form != None):
            form_data = form[-4:]
        
       

        print("system = ", system)
        flag = 0
        email = ''
        case = ''
        print(" System value when in last"+f"{system}")
        print(system)

        if system == None:
            
            context['data'] = data
            print(data["insurance_company"])
            if data["insurance_company"] == "HDFC ERGO General Insurance":
                print("None called")
                return render(request, "hdfc.html", context)
            else:
                return render(request, "hdfc.html", context)

        if system == "":
            
            context['data'] = data
            print(data["insurance_company"])
            if data["insurance_company"] == "HDFC ERGO General Insurance":
                print("None called")
                return render(request, "hdfc.html", context)
            else:
                return render(request, "hdfc.html", context)

        if system == " ":
            sys = request.POST.get('save', None)
            print("value of system",sys)
            context['data'] = data
            print(data["insurance_company"])
            if data["insurance_company"] == "HDFC ERGO General Insurance":
                print("None called")
                return render(request, "hdfc.html", context)
            else:
                return render(request, "hdfc.html", context)

        if system != None:
            print("running inside")
            for char in system:
                if char == "+":
                    flag = 1
                if flag == 0 and char != '+':
                    email = email+char
                if flag == 1 and char != '+':
                    case = case+char
            print("email = ", email)
            print("case = ", case)
            context["data"] = data
            # return render(request,"test.html",context)
            
            try:
                patient_details = {
                    "Insurance_Company": data.get("insurance_company", ""),
                    "Name": data["patient_details_name"],
                    "Gender": data["patient_details_gender"],
                    "AgeYear": data["patient_details_ageYear"],
                    "AgeMonth": data["patient_details_ageMonth"],
                    "DOB": data["patient_details_date"],
                    "Number": data["patient_details_contact_number"],
                    "Attending_Relative_Number": data["patient_details_numberOfAttendingRelative"],
                    "InsuredIdCardNumber": data["patient_details_insuredMemberIdCardNo"],
                    "Policy_Id": data["patient_details_policyNumberorCorporateName"],
                    "EmployeeId": data["patient_details_EmployeeId"],
                    "Address": data["patient_details_currentAddress"],
                    "Occupation": data["patient_details_occupation"],
                    "Nature_Of_Illness": data["doctor_natureOfLiness"],
                    "Doctor_ContactNumber": data["doctor_contactNumber"],
                }
                
                addition_details = {
                    "Nature_Of_Illness": data["doctor_natureOfLiness"],
                    "Duration_Of_Present_Ailments": data["doctor_durationOfPresentAliment"],
                    "Date_Of_First_Consultation": data["doctor_dateOfFirstConsultation"],
                    "Past_History_Of_Present_Ailments": data["doctor_PastHistoryOfPresentAlignment"],
                    "Provision_Diagnosis": data["doctor_provisionalDiagnosis"],
                    "ICD_Code": data["doctor_icdCode"],
                    "If_Other_Treatment_Provide_Details": data["doctor_ifOtherTratmentProvideDetails"],
                    "How_Did_Injury_Occur": data["doctor_howDidInjuryOccure"],
                    "Date_Of_Injury":data.get("doctor_dateOfInjury",""),
                    "doctor_releventClinicFindings":data.get("doctor_releventClinicFindings",""),
                    "MandatoryPastHistoryMonth": data["admission_mandatoryPastHistoryMonth"],
                    "MandatoryPastHistoryYear": data["admission_mandatoryPastHistoryYear"],
                    "HeartDiseaseMonth": data["admission_heartDiseaseMonth"],
                    "HeartDiseaseYear": data["admission_heartDiseaseYear"],
                    "HypertensionMonth": data["admission_hypertensionMonth"],
                    "HypertensionYear": data["admission_hypertensionYear"],
                    "HyperlipidemiasMonth": data["admission_HyperlipidemiasMonth"],
                    "HyperlipidemiasYear": data["admission_HyperlipidemiasYear"],
                    "OsteoarthritisMonth": data["admission_osteoarthritisMonth"],
                    "OsteoarthritisYear": data["admission_osteoarthritisYear"],
                    "AsthmaOrCOPDOrBronchitisMonth": data["admission_asthmaOrCOPDOrBronchitisMonth"],
                    "AsthmaOrCOPDOrBronchitisYear": data["admission_asthmaOrCOPDOrBronchitisYear"],
                    "CancerMonth": data["admission_cancerMonth"],
                    "CancerYear": data["admission_cancerYear"],
                    "AlcoholOrDrugAbuseMonth": data["admission_alcoholOrDrugAbuseMonth"],
                    "AlcoholOrDrugAbuseYear": data["admission_alcoholOrDrugAbuseYear"],
                    "RelatedAlimentsMonth": data["admission_anyHIVOrSTDOrRelatedAlimentsMonth"],
                    "RelatedAlimentsYear": data["admission_anyHIVOrSTDOrRelatedAlimentsYear"],
                    "OtherAliments": data["admission_anyOtherAliments"],
                    "Reported_To_Police": data.get("doctor_reportedToPolice", ""),
                    "patient_details_HealthInsurance": data.get("patient_details_HealthInsurance", ""),
                    "familyPhysician": data.get("patient_details_familyPhysician", ""),
                    "doctor_proposedLineOfTreatment_Medical_Managment": data.get("doctor_proposedLineOfTreatment_Medical_Managment", ""),
                    "doctor_proposedLineOfTreatment_Surgical_Managment": data.get("doctor_proposedLineOfTreatment_Surgical_Managment", ""),
                    "doctor_proposedLineOfTreatment_Intensive_Care": data.get("doctor_proposedLineOfTreatment_Intensive_Care", ""),
                    "doctor_proposedLineOfTreatment_Investigation": data.get("doctor_proposedLineOfTreatment_Investigation", ""),
                    "doctor_proposedLineOfTreatment_Allopathic_Treatment": data.get("doctor_proposedLineOfTreatment_Allopathic_Treatment", ""),
                    "In_Case_Of_Accident": data.get("doctor_inCaseOfAccident", ""),
                    "Injury_Disease_Caused_Due_To_Substance_Abuse_Alcohol_Consumption_": data.get("doctor_injuryorDiseaseCausedDueToSubstance", ""),
                    "doctor_testAlcohol": data.get("doctor_testAlcohol", ""),
                    "isThisAEmergencyPlannedHospitalization": data.get("admission_isThisAEmergencyPlannedHospitalization", ""),
                    "HealthInsuranceYesCompanyName": data.get("HealthInsuranceYesCompanyName", ""),
                    "Give_Company_details": data.get("Give_details", ""),
                    "PhysicianYesPhysicianName": data.get("PhysicianYesPhysicianName", ""),
                    "PhysicianYesPhysicianContactNum": data.get("PhysicianYesPhysicianContactNum", ""),
                    "doctor_firNo": data.get("doctor_firNo", ""),
                    "G": data.get("doctor_inCaseMaternityG", ""),
                    "P": data.get("doctor_inCaseMaternityP", ""),
                    "L": data.get("doctor_inCaseMaternityL", ""),
                    "A": data.get("doctor_inCaseMaternityA", ""),     
                                       
                }


                hospital_details = {
                    "Date_of_Admission": data["admission_date"],
                    "ExpectedDateOfDelivery": data["doctor_expectedDateOfDelivery"],
                    "Days_In_ICU": data["admission_daysInICU"],
                    "Room_Type": data["admission_roomType"],
                    "DateofInjury": data["doctor_dateOfInjury"],
                    "Treating_Doctor": data["Treating_Doctor"],
                    "Days_In_Hospital":data["admission_expectedNoOfDays"],
                }

                hospital_charges = {
                    "Per_Day_Room_Rent": data["admission_perDayRoomRent"],
                    "Cost_Of_Investigation": data["admission_expectedCostForInvestigation"],
                    "ICU_Charges": data["admission_icuCharge"],
                    "OT_Charges": data["admission_otCharge"],
                    "ProfessionalFeesSurgeon": data["admission_professionalFeesSurgeon"],
                    "cost_Of_Implant": data["admission_madicineConsumablesCostOfImplats"],
                    "OtherHospitalIfAny": data["admission_otherHospitalIfAny"],
                    "All_Including_Package": data["admission_allIncludePackageCharge"],
                    "total": data["admission_sumTotalExpected"],
                }
                try:
                    print("final submission Taking Place")
                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'patient_details').document(u'patient_details').update(patient_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'patient_details').document(u'addition_details').update(addition_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'hospital_details').document(u'hospital_details').update(hospital_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'hospital_details').document(u'hospital_charges').update(hospital_charges)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).update({"audit_trail": firestore.ArrayUnion([data.get('status', "None")+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+data.get('email_title', "None")])})

                except:
                #     return HttpResponse("Exception")
                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'patient_details').document(u'patient_details').set(patient_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'patient_details').document(u'addition_details').set(addition_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'hospital_details').document(u'hospital_details').set(hospital_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'hospital_details').document(u'hospital_charges').set(hospital_charges)

                
                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(case).set({
                        'formstatus': u'draft',
                        'status': "done",
                        'Type': data.get("admission_isThisAEmergencyPlannedHospitalization", ""),
                    })
            except IndexError as e:
                print(e)
                return redirect(f"/claimpage1?system={email}%2B{case}")

            db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(case).update({
                'formstatus': u'draft',
            })

            # storage= firebase.storage()
            # datadir = '/home/anishshende/bmxp'

            # aadharFiles = storage.child(request.session['hospital_email']).child(u'cases').child(u'case{i}').child(u'uploadAdhar').list_files()
            # consultationFiles = storage.child(request.session['hospital_email']).child(u'cases').child(u'case{i}').child(u'uploadConsultation').list_files()
            # healthFiles = storage.child(request.session['hospital_email']).child(u'cases').child(u'case{i}').child(u'uploadHealth').list_files()

            # for file in aadharFiles:
            #     try:
            #         file.download_to_filename(datadir + file.name)
            #     except:
            #         print('Download Failed')

            # for file in consultationFiles:
            #     try:
            #         file.download_to_filename(datadir + file.name)
            #     except:
            #         print('Download Failed')

            # for file in healthFiles:
            #     try:
            #         file.download_to_filename(datadir + file.name)
            #     except:
            #         print('Download Failed')

            return redirect(f"/claimpage1?system={email}%2B{case}")

    return redirect(f"/claimpage1?system={email}%2B{case}")


def formData(request, text):
    flag = 0
    email = ''
    case = ''

    print("thiissssssssssssssssssss")

    for char in text:
        if char == "+":
            flag = 1
        if flag == 0 and char != '+':
            email = email + char
        if flag == 1 and char != '+':
            case = case+char

    context = {}
    doc_ref = db.collection(u'users').document(f'{email}').collection(
        u'case').document(f'{case}').collection(u'forms').document(u'form_data')
    doc = doc_ref.get()
    if doc.exists:
        a = doc.to_dict()
    else:
        print("no data found")
    print(a)
    context['formContents'] = a

    return render(request, 'formData.html', context)


def addQuery(request, que):
    email = ""
    case = ''
    query = ''
    flag = 0
    for char in que:
        if char == '+':
            flag = 1
        if char == '&':
            flag = 2
        if flag == 0:
            query = query+char
        if flag == 1 and char != '+':
            email = email+char
        if flag == 2 and char != '&':
            case = case+char

    print("email = ", email)
    print("case = ", case)
    print("query = ", query)

    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
        case).update({
            'formstatus': 'query',
            'Query': query,
            "status": "filled"
        })

    return HttpResponse("success")



def rateList(request):
    return render(request, 'rateList.html')


def rateListDetails(request):
    return render(request, 'ratelistDetails.html')

def caseDetails(request):
    context = {}
    casenumber = request.GET.get('data')
    doc_ref = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
        u'cases').document(f'{casenumber}').collection("patient_details").document("patient_details")
    doc = doc_ref.get()

    if doc.exists:
        a = doc.to_dict()
        context['insurance_company'] = a['Insurance_Company']
        context['patient_name'] = a['Name']
        context['caseid'] = casenumber
        # context['city'] = a['City']
        context['contact_Number'] = a['Number']
        context['doctor_natureOfLiness'] = a['Nature_Of_Illness']
    else:
        print("no data found")

    doc_ref_new = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
        u'cases').document(f'{casenumber}').collection("hospital_details").document("hospital_details")
    doc_new = doc_ref_new.get()

    if doc_new.exists:
        b = doc_new.to_dict()
        print(b)
        context['admissiondate'] = b['Date_of_Admission']
        context['treating_doctor'] = b['Treating_Doctor']

    else:
        print("no data found")

    status = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
        u'cases').document(f'{casenumber}')

    formstatus = status.get()
    if formstatus.exists:
        b = formstatus.to_dict()
        print(b)
        context['formstatus'] = b['formstatus']

    else:
        print("no data found o")
    audit = []

    audit_trail = db.collection(u'hospitals').document(request.session['hospital_email']).collection(
        u'cases').document(f'{casenumber}')
    audit_value = audit_trail.get()

    if audit_value.exists:
        b = audit_value.to_dict()
        print(b)
        if len(b) > 3:
            values = b['audit_trail']
            for i in values:
                x = i.split("+")
                audit.append(x)
            print(audit)
            context['audit'] = audit
        else:
            print("no data found")
    else:
        print("no data found of ")

        # this is hospital email also accessible in caseDetails page
        
        context['hospital_email'] = request.session['hospital_email']

    return render(request, 'caseDetails.html')


def newAction(request):
    return render(request, 'newAction.html')


def loginPage(request):

    return render(request, 'loginPage.html')


def companyDetails(request):
    return render(request, 'companyDetails.html')
























# Emailer Anish
def optimiser(s):
    if(s[0] == '"' and s[len(s)-1] == '"'):
        return s[1:-1]
    else:
        return s


def helper(s):
    s = str(s)
    if(s[0] == '0'):
        return s[1:]
    else:
        return s


def spliteremail(s):
    if(s == None):
        return "", ""
    idx = s.find('<')
    if(idx == -1):
        return s, s
    lgth = len(s)
    # print(s)
    x_name = s[:idx-1]
    if s[:-1].isalpha():
        y_email = s[idx+1:]

    else:
        y_email = s[idx+1:-1]
    # print (y_email)
    # print("-"*50)
    return x_name, y_email


def func(s):
    if(s[:2].isdigit()):
        x = s[:2]
        y = s[2:]
    else:
        x = s[:1]
        y = s[1:]

    # print(x)
    # print(y)
    return x, y


def spliterdate(s):
    if s == None:
        return "0"
    day = s[5:11]
    final = day
    monthdate = day.replace(" ", "")
    curr = datetime.today()

    date, day = func(monthdate)

    date = helper(date)
    day = mth.index(day) + 1
    tdate = helper(curr.day)
    tmonth = helper(curr.month)

    if(date == tdate and day == tmonth):
        return "today"
    else:
        s = date + " " + mth[day-1]
        return s


def bunny(request):
    context = {}
    sender = "anish@bimaxpress.com"

    # sender = request.session['hospital_email']
        # sender = 'newuser@gmail.com'

    data = db.collection(u'hospitals').document(sender).get()
        
    user = data.to_dict()['Emailer']

    domain = user['domain']

    emailID = user['email']

    password = user['password']

    # domain = 'mail.bimaxpress.com'
    # emailID = 'anish@bimaxpress.com'
    # password = 'abcd1234'
    

    if request.method == "POST":
        
        file = request.FILES.getlist("filenameupload")
        # fs = FileSystemStorage()
        # print(file)
        # for f in file:
        #     # filename = fs.save('/home/anishshende/bmxp/' + file.name, file)
        #     print(f)
        
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        
        print('_'*50)
        print(os.environ)
        print('_'*50)
        # print(len(file))

        sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,file,domain,password)

    # print(data)

    imap_server = imaplib.IMAP4_SSL(host=domain)
    imap_server.login(emailID, password)
    imap_server.select()  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])
        # print("========email start===========")
        # print(x)
        # print("========email end===========")
        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]
            print("part print")
            # print(part)
            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        # newtext.replace('"',"\'" )
        # newtext.replace("'","\'")
        # newtext = escape(newtext)
        # print(newtext)
        msg_json = {
            # "from" : x['from'],
            "from": escape(emailid),
            "name": escape(optimiser(nameid)),
            "to": escape(x['to']),
            "subject": escape(x['subject']),
            # "name": x['name'],
            # "name": spliter1(x['from']),
            # "emailaddr": spliter2(x['from']),
            "message": escape(newtext),
            "date": escape(time),
            "id": count,
        }
        # print(newtext)
        count += 1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a = eval(email_message)
    # print(a)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    time_list = []

    for i in reversed(range(len(a))):

        print("+++++++++++")
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l

    return render(request, "baseemail.html", context)


def replymail(request):
    context = {}
    # print(request.method)
    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")
        sender = request.session['hospital_email']
        data = db.collection(u'hospitals').document(sender).get()
        user = data.to_dict()['Emailer']
        domain = user['domain']
        emailID = user['email']
        password = user['password']

        # file = request.FILES['filenameupload']

        sender_msg = request.POST.get('rep_smsg')
        reciever = request.POST.get('rep_recv')

        Bcc = request.POST.get('rep_recvBcc')
        Cc = request.POST.get('rep_recvCc')
        sub = request.POST.get('rep_ssub')
        m_id = request.POST.get('rep_id')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"

        imap_server = imaplib.IMAP4_SSL(host=domain)
        imap_server.login(emailID, password)
        imap_server.select()

        _, msg = imap_server.fetch(m_id, '(RFC822)')
        email_msg = email.message_from_bytes(msg[0][1])

        newtext = ""

        new = EmailMultiAlternatives("Re: "+email_msg["Subject"],
                                     sender_msg,
                                     sender,  # from
                                     [email_msg["Reply-To"]
                                         or email_msg["From"]],  # to
                                     headers={'Reply-To': sender,
                                              "In-Reply-To": email_msg["Message-ID"],
                                              "References": email_msg["Message-ID"]})
        # new.attach_alternative(sender_msg, "text/plain")
        new.attach(MIMEMessage(email_msg))
        # print(new.body) # attach original message
        for f in file:
            new.attach(f.name, f.read(),f.content_type)

        new.send()
        next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
    # return render(request,"baseemail.html",context)


def create(request):
    if request.method == 'POST':
        to = request.POST['to']
        subject = request.POST['subject']
        message = request.POST['message']
        new_email = Email(to=to, subject=subject, message=message)
        new_email.save()
        # print(new_email)
        success = 'Mail sent' + to + 'successfully'
        return HttpResponse(success)

    # print("EMAIL SENT")


def sentmail(request):
    context = {}
    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")

        sender = request.session['hospital_email']
        data = db.collection(u'hospitals').document(sender).get()
        user = data.to_dict()['Emailer']
        domain = user['domain']
        emailID = user['email']
        password = user['password']
        # file = request.FILES['filenameupload']
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,domain,password)
    # print(data)

    imap_server = imaplib.IMAP4_SSL(host=domain)
    imap_server.login(emailID, password)
    imap_server.select('INBOX.Sent')  # sent folder selected
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        # print(x['from'])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])
        to = ""
        ssub = ""
        mssg = ""
        if(x['to'] != None):
            to = x['to']

        if(x['subject'] != None):
            ssub = x['subject']

        if(x['message'] != None):
            mssg = x['message']

        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": to,
            "subject": ssub,
            "date": time,
            "id": count,
            "message": newtext,
        }

        if(emailid):
            count += 1
            message.append(msg_json)

    imap_server.close()
    imap_server.logout()

    email_message = json.dumps(message)
    print(email_message)

    a = eval(email_message)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    time_list = []

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        # print(a[i]['message'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l

    return render(request, "sentemail.html", context)

# TRASH Folder


def trashmail(request):
    context = {}
    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")
        sender = request.session['hospital_email']
        data = db.collection(u'hospitals').document(sender).get()
        user = data.to_dict()['Emailer']
        domain = user['domain']
        emailID = user['email']
        password = user['password']
        # file = request.FILES['filenameupload']
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,file,domain,password)
    # print(data)

    imap_server = imaplib.IMAP4_SSL(host=domain)
    imap_server.login(emailID, password)
    imap_server.select('INBOX.Trash')  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])

        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": x['to'],
            "subject": x['subject'],
            "date": time,
            "id": count,
            "message": newtext,
        }
        count += 1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a = eval(email_message)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    time_list = []

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l

    return render(request, "trash.html", context)

# DRAFTS Folder


def draftmail(request):
    context = {}
    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")
        sender = request.session['hospital_email']
        data = db.collection(u'hospitals').document(sender).get()
        user = data.to_dict()['Emailer']
        domain = user['domain']
        emailID = user['email']
        password = user['password']

        # file = request.FILES['filenameupload']
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,file,domain,password)
    # print(data)

    imap_server = imaplib.IMAP4_SSL(host=domain)
    imap_server.login(emailID, password)
    imap_server.select('INBOX.Sent')  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])

        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": x['to'],
            "subject": x['subject'],
            "date": time,
            "id": count,
            "message": newtext,
        }
        count += 1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a = eval(email_message)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    time_list = []

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l

    return render(request, "drafts.html", context)

# Starred Folder


def starredemail(request):
    context = {}
    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")
        sender = request.session['hospital_email']
        data = db.collection(u'hospitals').document(sender).get()
        user = data.to_dict()['Emailer']
        domain = user['domain']
        emailID = user['email']
        password = user['password']
        # file = request.FILES['filenameupload']
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,file,domain,password)
    # print(data)

    imap_server = imaplib.IMAP4_SSL(host=domain)
    imap_server.login(emailID, password)
    imap_server.select('INBOX')  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])

        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": x['to'],
            "subject": x['subject'],
            "date": time,
            "id": count,
            "message": newtext,
        }
        count += 1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a = eval(email_message)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    time_list = []

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l

    return render(request, "starred.html", context)



def sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,files,domain,password):

    connection = get_connection(
        host = domain,
        port = EMAIL_PORT,
        username = sender,
        password = password ,
        use_ssl = EMAIL_USE_SSL,
        backend=EMAIL_BACKEND
    )

    email = EmailMultiAlternatives(sub, sender_msg, sender, [reciever, ], bcc=[
                                   Bcc, ], cc=[Cc, ],connection=connection)
    # print(email.message())
    text = str(email.message())
    imap_server = imaplib.IMAP4_SSL(host=domain, port=993)

    
    imap_server.login(sender, password)
    imap_server.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(
        time.time()), text.encode('utf8'))

    for f in files:
        email.attach(f.name, f.read(), f.content_type)

    email.send()
    connection.close()