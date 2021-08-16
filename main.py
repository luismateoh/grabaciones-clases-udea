from bs4 import BeautifulSoup
from selenium import webdriver
import time
import youtube_dl

#Cofigurar los sigueintes parametros:
#-----------------------------------------------
USERNAME = "nombre.apellido"  # Moodle nombre de usuario
PASSWORD = "contraseña"  # Moodle contarseña
MATERIA = 'Arquitectura-de-computadores' #Nombre de la materia
REC_URL = 'https://udearroba.udea.edu.co/internos/mod/recordingszoom/recordingsdrive.php?id=882603' #Enlace donde estan las grabaciones
#-----------------------------------------------

BASE_URL = "https://udearroba.udea.edu.co/internos/my"
LOGIN_URL = "https://udearroba.udea.edu.co/internos/login/index.php"

wd = webdriver.Firefox() #Abrir el navegador

wd.get(LOGIN_URL)
time.sleep(2)
wd.find_element_by_id('').send_keys(USERNAME)
wd.find_element_by_id('').send_keys(PASSWORD)
wd.find_element_by_id('loginbtn').click()
wd.get(REC_URL)
time.sleep(2)
soup = BeautifulSoup(wd.page_source, 'html.parser')
rows = soup.find_all('tr')
rows.pop(0)

for r in rows:
    date_link = r.find("td", attrs={"class": "cell c2"})
    date_link = date_link.getText()
    date_link = date_link.split(' ')
    date_link = date_link[0]
    video_link = r.find("input", attrs={"name": "zoomplayredirect"})
    video_link = video_link["value"]
    outtmpl = MATERIA + date_link + '.mp4'
    ydl_opts = {
        'outtmpl': outtmpl,
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

wd.close()