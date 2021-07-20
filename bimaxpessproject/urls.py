"""bimaxpessproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('about', views.about, name="about"),
    path('', views.login, name="login"),
    # path('table', views.table, name="table"),
    # path('claim', views.claim ,name="claim"),
    path('claimpage1',views.claimpage1, name="claimpage1"),
    path('postsignIn',views.postsignIn, name="postsignIn"),
    # path('usercreation',views.usercreation, name="usercreation"),
    path('mainpage',views.mainpage, name="mainpage"),
    path('sendmail',views.sendmail,name="sendmail"),
    path('generateform',views.generateform,name="generateform"),
    path('adduser',views.adduser, name="adduser"),
    path('logout',views.logout, name="logout"),
    path('claims',views.claims, name="claims"),
    path('saveData/', views.saveData , name="saveData"),
    path('listData/<p>', views.listData, name='listData'),
    path('addcompany',views.addcompany,name='addcompany'),
    path('listData/updateFormstatus/<new>', views.updateFormstatus, name="updateFormstatus"),
    path('formData/<text>', views.formData , name='formdata'),
    path('addQuery/<que>', views.addQuery, name='addQuery'),
    path('sendcompany/<p>', views.sendcompany ,name="sendcompany"),
    path('resendemail', views.resendemail ,name="resendemail"),
    

    #<-----Anis_code------>
    path('bunny',views.bunny , name="bunny"),
    path('sent',views.sentmail , name="sentmail"),
    path('trash',views.trashmail , name="trashmail"),
    path('starred',views.starredemail , name="starredmail"),
    path('drafts',views.draftmail , name="draftmail"),
    path('replymail',views.replymail , name="replymail"),
    
    path('savefinal',views.savefinal , name="savefinal"),
    
    
    # <-----Grv---->
    path('hospital', views.hospital, name='hospital'),
    path('plandetails', views.plandetails, name='plandetails'),
    path('hospital/edit', views.hospitalEdit, name='hospitalEdit'),
    path('doctor', views.doctor, name='doctor'),
    path('doctor/edit', views.doctorEdit, name='doctorEdit'),
    path('doctor/add', views.doctorAdd, name='doctorAdd'),
    path('analist', views.analist, name='analist'),
    path('analist/edit', views.analistEdit, name='analistEdit'),
    path('analist/add', views.analistAdd, name='analistAdd'),
    path('rateList', views.rateList, name='rateList'),
    path('rateList/details', views.rateListDetails, name='rateListDetails'),
    path('empanelledCompanies', views.EmpanelledCompanies, name='EmpanelledCompanies'),
    path('empanelledCompanies/add', views.empanelledCompaniesAdd, name='empanelledCompaniesAdd'),
    
    path('caseDetails', views.caseDetails, name='caseDetails'),
    path('newAction', views.newAction, name='newAction'),
    path('loginPage', views.loginPage, name='loginPage'),
    path('companyDetails', views.companyDetails, name='companyDetails'),
    path('getcasedetail', views.getcasedetail, name='getcasedetail'),
    path('savestatus', views.savestatus, name='savestatus'),
    path('updateunprocess', views.updateunprocess, name='updateunprocess'),
    path('saveinsurancedata', views.saveinsurancedata, name='saveinsurancedata'),
    # fro form
    path('sendData', views.sendData, name='sendData'),
    path('sendDataDoctors', views.sendDataDoctors, name='sendDataDoctors'),
    

    
    
    
]
