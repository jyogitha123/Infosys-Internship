
import smtplib
from email.message import EmailMessage
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

# Set up SMTP server
server = smtplib.SMTP('smtp.office365.com', 587)
server.starttls()
server.login(email_address, email_password)

# Send the email
server.send_message(msg)
server.quit()

print("Email sent successfully")
