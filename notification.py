import urllib.request
import pandas as pd
from html_table_parser.parser import HTMLTableParser
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def scrape_table(url): #scraping the table
    #making request to the website
    request = urllib.request.Request(url=url)
    f = urllib.request.urlopen(request)
    #reading contents of the website
    web_content= f.read().decode('utf-8')
    parser = HTMLTableParser()
    parser.feed(web_content)
    tables = parser.tables
    # Assuming you want the first table found on the page
    if tables:
        return tables[0]  # Return the first table found
    else:
        return None


def send_email(subject, body, mailing_list):
    from_email = 'strefainwestora69@02.pl'
    from_password = 'fexqen-vicqem-0wetVo'
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(mailing_list)
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('poczta.o2.pl', 465) as server:
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, mailing_list, text)

# Function to check for changes
def check_for_changes(url, state_file, notification_emails):
    current_state = scrape_table(url)
    if current_state:
        # Read previous state from file
        try:
            with open(state_file, 'r') as file:
                previous_state = file.read()
        except FileNotFoundError:
            previous_state = ''
        
        # Compare current state with previous state
        if str(current_state) != previous_state:
            # Update state file with current state
            with open(state_file, 'w') as file:
                file.write(str(current_state))
            
            # Send email notification
            send_email('Table Change Detected', 'A change has been detected in the table.', notification_emails)
            print('Change detected and email sent.')
        else:
            print('No changes detected.')
    else:
        print('Error: Unable to scrape table.')

url = 'https://strefainwestorow.pl/rekomendacje/lista-rekomendacji/wszystkie'
state_file= 'table.txt'
notification_emails = ['luizasemeniuk@gmail.com']  # List of recipient email addresses

while True:
    check_for_changes(url, state_file, notification_emails)
    time.sleep(3)
