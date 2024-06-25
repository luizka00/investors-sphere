import urllib.request
import pandas as pd
from html_table_parser.parser import HTMLTableParser
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import difflib
import os

def scrape_table(url): #scraping the table
    #making request to the website
    request = urllib.request.Request(url=url)
    f = urllib.request.urlopen(request)

    #reading contents of the website
    web_content= f.read().decode('utf-8')
    tabela = HTMLTableParser()
    tabela.feed(web_content)
    print(tabela.tables[0])

def send_email(subject, body, mailing_list):
    from_email = 'strefainwestorow69@gmail.com'
    from_password = 'Polska123'
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(mailing_list)
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, mailing_list, text)

# Function to check for changes
def check_for_changes(url, state_file, notification_emails):
    current_state = scrape_table(url)
    
    if os.path.exists(state_file):
        with open(state_file, 'r') as file:
            previous_state = file.read()
    else:
        previous_state = ''
    
    if current_state != previous_state:
        with open(state_file, 'w') as file:
            file.write(current_state)
        
        diff = difflib.unified_diff(
            previous_state.splitlines(), 
            current_state.splitlines(), 
            fromfile='previous', 
            tofile='current', 
            lineterm=''
        )
        diff_text = '\n'.join(list(diff))
        send_email('Na Strefie Inwestora dropnęła nowa rekomendacja', diff_text, notification_emails)
        print('Change detected and email sent.')
    else:
        print('No changes detected.')

url = 'https://strefainwestorow.pl/rekomendacje/lista-rekomendacji/wszystkie'
state_file= "1,2,3"
notification_emails = ['luizasemeniuk@gmail.com']  # List of recipient email addresses
while True:
    check_for_changes(url, state_file, notification_emails)
    time.sleep(60) 

