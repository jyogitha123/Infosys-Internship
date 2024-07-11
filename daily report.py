import smtplib
from email.message import EmailMessage
import csv
import zipfile
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import psycopg2

# Database connection parameters
dbname = "College DB"
user = "postgres"
password = "Geetha@522"
host = "localhost"

# Connect to the database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host
)
cur = conn.cursor()

# Query the database to retrieve data
cur.execute("SELECT * FROM daily_report")
data = cur.fetchall()

# Create a CSV file from the query results
with open('daily report.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

# Define email details
email_address = "support@aptpath.in"
email_password = "btpdcnfkgjyzdndh"
recipient_address = "21nn1a0522.yogitha@gmail.com"
subject = "Project"
body = "Automated attendance system"

# Create an EmailMessage object
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = email_address
msg['To'] = recipient_address

# Attach the daily report CSV file
with open('/content/daily report.csv', 'rb') as csvfile:
    msg.add_attachment(csvfile.read(), maintype='text', subtype='csv', filename='daily report.csv')

# Attach images from the subject_images dictionary as separate attachments
subject_images = {
    'Math': '/content/Group images/Maths 2024-06-28 03000400.jpeg',
    'English': '/content/Group images/English 2024-06-18 11001200 (1).jpeg',
    'History': '/content/Group images/History 2024-06-22 12000100.jpeg',
    'Economy': '/content/Group images/Economy 2024-06-15 10001100.jpeg',
    'AI': '/content/Group images/AI 2024-06-11 09001000.jpeg',
    'OS': '/content/Group images/OS 2024-06-28 03000400.jpeg'
}

for subject, image_file in subject_images.items():
    if os.path.exists(image_file):
        with open(image_file, 'rb') as img:
            msg.add_attachment(img.read(), maintype='image', subtype='jpeg', filename=f"{subject}.jpeg")
    else:
        print(f"Failed to find image file: {image_file}")

# Set up SMTP server
server = smtplib.SMTP('smtp.office365.com', 587)
server.starttls()
server.login(email_address, email_password)

# Send the email
try:
    server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")

# Quit the SMTP server
server.quit()
