from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import qrcode

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


file = drive.CreateFile({'title':"Aakash.txt"})
file.SetContentString("This is my first file")
file.Upload()
result = None
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for item in file_list:
	if item['title'] == 'Aakash.txt':
		result = 'https://drive.google.com/file/d/' + item['id'] + '/view?usp=drivesdk'
		break
qr = qrcode.QRCode()
qr.add_data(result)
qr.make()
img = qr.make_image()
img.save('qrcode.png')