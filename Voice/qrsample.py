from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LoadCredentialsFile("client_secret.json")
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

