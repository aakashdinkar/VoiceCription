from django.shortcuts import render

from django.http import HttpResponse
import qrcode

from langdetect import detect
import speech_recognition as sr
from googletrans import Translator
from langdetect import DetectorFactory
DetectorFactory.seed = 0

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas   

@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.filter(provider='auth0')[0]
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': user.email,
    }

    return render(request, 'Voice/dashboard.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)


def speech():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    local_lang='hi'
    audio = ""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 3)
        audio = r.listen(source)
    try:
        spoken_txt = r.recognize_google(audio,language='en-US')
        print(spoken_txt)
    except:
        print("Error")
    return spoken_txt


def main(request):
    return render(request, 'Voice/main.html')

def index(request):
    return render(request,'Voice/index.html')

dat = []
for i in range(7):
    dat.append('')

dat[0] = 'Dinkar123'

def Name(request):
    data=speech()
    dat[0] = data
    return render(request,'Voice/index.html',{'data':dat})

def Address(request):
    data=speech()
    dat[1] = data
    return render(request,'Voice/index.html',{'data':dat})

def Age(request):
    data=speech()
    dat[2] = data
    return render(request,'Voice/index.html',{'data':dat})

def Contact(request):
    data=speech()
    dat[3] = data
    return render(request,'Voice/index.html',{'data':dat})

def Symptom(request):
    data=speech()
    dat[4] = data
    return render(request,'Voice/index.html',{'data':dat})


def Daignosis(request):
    data=speech()
    dat[5] = data
    return render(request,'Voice/index.html',{'data':dat})

def Medication(request):
    data=speech()
    dat[6] = data
    return render(request,'Voice/index.html',{'data':dat})

from reportlab.pdfgen import canvas   
import qrcode
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def pdf(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        age = request.POST.get('age')
        contact = request.POST.get('contact')
        symptom = request.POST.get('symptom')
        daignosis = request.POST.get('daignosis')
        medication = request.POST.get('medication')
    p = canvas.Canvas(f'{dat[0]}.pdf') 
    p.setFont("Times-Roman", 24)  
    p.drawString(400,800, "Dr. Octocat")
    p.drawString(400,775, "MBBS")
    # p.drawImage("datafiles/1664c50e43535640ec7cc40d49b0b017.png", 45, 740, width = 100, height = 100)  
    p.drawString(15,730,"_______________________________________________")
    p.setFont("Times-Roman", 18)
    p.drawString(100,700,f"Name                          :{dat[0]}")
    p.drawString(100,680,f"Addres                        :{dat[1]}")
    p.drawString(100,660,f"Age                             :{dat[2]}")
    p.drawString(100,640,f"Contact No.                :{dat[3]}")
    p.drawString(100,620,f"Symptoms                  :{dat[4]}")
    p.drawString(100,600,f"Daignosis                   :{dat[5]}")
    p.drawString(100,580,f"Medication                 :{dat[6]}")
    p.showPage()  
    p.save()
    return render(request, 'Voice/Last.html')

def showqrcode(request):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)
    file = drive.CreateFile({'title':f"{dat[0]}"})
    file.SetContentFile(f'{dat[0]}.pdf')
    file.Upload()
    result = None
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for item in file_list:
        if item['title'] == f'{dat[0]}':
            result = 'https://drive.google.com/file/d/' + item['id'] + '/view?usp=drivesdk'
            break
    qr = qrcode.QRCode()
    qr.add_data(result)
    qr.make()
    img = qr.make_image()
    img.save('qrcode.png')
    return render(request, 'Voice/qr.html')