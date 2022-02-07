import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.parse
from email.utils import formataddr
from dotenv import load_dotenv
import requests
import json
import uuid
load_dotenv()

def mint_nft(address, email):
    url = "https://api.nftport.xyz"
    api_key = os.environ['NFTPORT_KEY']

    headers = {"Authorization": api_key}
    json = {
        "chain": "polygon",
        "name": email,
        "description": "3Safe has verified your ownership of this email address",
        "file_url": "https://lib.umso.co/lib_FxAiMkwJQBKyYSwk/k8lwoxlskzitdnrp.png",
        "mint_to_address": address
    }
    resp = requests.post(url + '/v0/mints/easy/urls', headers=headers, json=json)
    print(resp.text)


def generate_code(email):
    with open("codes.json", "r") as json_data:
        data = json.load(json_data)
        code = str(uuid.uuid4())
        print(code)
        data[email] = code

        with open("codes.json", "w") as file:
            json.dump(data, file)
    return code


def send_email(email, code, address):
    print(f"sending to {email}, with code: {code} and address: {address}")
    # User configuration
    sender_email = "team@vocal.email"
    sender_name = "Nathan from Vocal"

    verification_link = f"{os.environ['SERVER_URL']}/verify/{urllib.parse.quote(code)}/{urllib.parse.quote(email)}/{urllib.parse.quote(str(address))}"
    print(verification_link)

    html_text = f"""
            Hey !
            <br><br>
            Thanks for using 3Safe to generate an NFT from your verified email address! 
            <br><br>
            <a href="{verification_link}">Click here to verify your email</a>.
             <br><br>
             Have a wonderful day, <br><br> Nathan

            """

    msg = MIMEMultipart()
    msg['To'] = formataddr((email, email))
    msg['From'] = formataddr((sender_name, sender_email))
    msg['Subject'] = f'Verify your email ({email}) for 3Safe!'
    msg.attach(MIMEText(html_text, 'html'))


    smtp = smtplib.SMTP('smtp.gmass.co', 587)

    smtp.starttls()
    smtp.login('gmass', os.environ['GMASS_KEY'])
    smtp.sendmail(sender_email, email, msg.as_string())
    smtp.quit()
    # Sending email from sender, to receiver with the email body
    print('Email has been sent')

def verify_code(email, code):
    with open("codes.json", "r") as json_data:
        data = json.load(json_data)
        real_code = data.get(email)
        if code == real_code:
            data.pop(email)
            with open("codes.json", "w") as file:
                json.dump(data, file)

            return True
        else:
            return False

