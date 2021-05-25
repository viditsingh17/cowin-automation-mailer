import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from datetime import date, timedelta

# COWIN API 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=651&date=23
# -05-2021'

# Get the list of hospital having vaccine availability for:
# 18+
# First dose

# If the list is greater than 0, send a WhatsApp html to 7022775309 & ###########

# Data is available for 9 days including today, so the GET request must be made 9 times for all these dates

# vars
today = date.today()
available_dates = []
selected_slots = []

# Email receivers

receivers = ['viditsinghbrahmania@gmail.com','vipulsinghbrahmania@gmail.com']


def mail_code(receivers, slots_data):
    sender = "vaccinationmailbot@gmail.com"
    password = "Covid-19"
    html = '''
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <style type="text/css">
          table, td, th {  
          border: 1px solid #ddd;
          text-align: left;
        }
        
        table {
          border-collapse: collapse;
          width: 100%;
        }
        
        th, td {
          padding: 15px;
        }
        </style>
      </head>
      <body>
    <h1> Hurry Vaccination Slots Available!</h1> <table id="summary" class="display" 
    style="width:100%"><thead><tr><th data-orderable="false">Name of 
    Hospital</th><th data-orderable="false">Dose 1(availability)</th><th data-orderable="false">Dose 2(availability)</th><th data-orderable="false">Address</th><th 
    data-orderable="false">From(Timing)</th><th data-orderable="false">To(Timing)</th><th 
    data-orderable="false">Date</th></thead> '''
    for i in slots_data:
        name = i[0]
        availibility1 = i[1]
        availibility2 = i[2]
        address = i[3]
        from_time = i[4]
        to_time = i[5]
        date = i[6]
        html += "<tr>"
        html += "<td>" + str(name) + "</td>"
        html += "<td>" + str(availibility1) + "</td>"
        html += "<td>" + str(availibility2) + "</td>"
        html += "<td>" + str(address) + "</td>"
        html += "<td>" + str(from_time) + "</td>"
        html += "<td>" + str(to_time) + "</td>"
        html += "<td>" + str(date) + "</td>"
        html += "</tr>"
    html += "</table>"
    html += '''This is an automated mail
    </body>
    </html>'''

    message = MIMEMultipart("alternative", None, [MIMEText(html, 'html')])
    message['Subject'] = "Vaccination Alert!"
    message['From'] = sender
    message['To'] = str(receivers)
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(sender, password)
    s.sendmail(sender, receivers, message.as_string())
    print("Email sent")
    s.quit()

print("Started running")
for i in range(9):
    _date = today + timedelta(days=i)
    _date = _date.strftime("%d-%m-%y")
    available_dates.append(_date)

for k in available_dates:
    cowinapi = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=651&date=' + k
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    response = requests.get(cowinapi, headers=headers)
    vaccination_centers = response.json()["centers"]
    if len(vaccination_centers) != 0:
        for i in vaccination_centers:
            sessions = i["sessions"]
            for j in sessions:
                if j["available_capacity_dose1"] > 0 and j["min_age_limit"] == 18:
                    slot_data = (
                        i["name"], j["available_capacity_dose1"],j["available_capacity_dose2"], str(i["address"]) + str(i["block_name"]), i["from"],
                        i["to"], k)
                    selected_slots.append(slot_data)
# if selected_slots has data then send it to email
if len(selected_slots) != 0:
    mail_code(receivers, selected_slots)
else:
    print("No data to mail")

print("Finishing")
# print(response.status_code)
