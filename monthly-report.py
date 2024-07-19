import smtplib
from email.message import EmailMessage
import csv
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

try:
    # Connect to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host
    )
    cur = conn.cursor()

    # Query the database to retrieve data
    cur.execute("SELECT * FROM monthly_report")
    data = cur.fetchall()

    # Close the database connection
    conn.close()

    # Define email details
    email_address = "support@aptpath.in"
    email_password = "btpdcnfkgjyzdndh"
    recipient_address = "21nn1a0522.yogitha@gmail.com"
    subject = "Project"
    body = "Automated attendance system"

    # Create an EmailMessage object
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = recipient_address

    # Add CSV file as attachment
    with open('/content/monthly report.csv', 'rb') as csvfile:
        msg.add_attachment(csvfile.read(), maintype='text', subtype='csv', filename='monthly report.csv')

    # Set up SMTP server
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(email_address, email_password)

    # Send the email
    server.send_message(msg)

    # Close the SMTP server connection
    server.quit()

    print("Monthly report csv Email sent successfully!")

except Exception as e:
    print(f"Error: {e}")
