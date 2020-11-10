import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import time
# from datetime import datetime
# now = datetime.now()
def emailconfirmation(firstname,emailaddress):
    port = 2525
    smtp_server = "smtp.mailtrap.io"
    login = 'vermashanaya1234@gmail.com'
    password = 'sh12345678@#'
    sender_email = 'vermashanaya1234@gmail.com'
    receiver_email = emailaddress
    message = MIMEMultipart("alternative")
    message["Subject"] = firstname+" , your appointment is scheduled!!"
    message["From"] = sender_email
    message["To"] = receiver_email
    # write the plain text part
    text = """\
    """
    # write the HTML part
    html = """\
    <html>
    <body>
    <p style="margin-left:10px">hello \n</p>
    <p style="margin-left:10px" >Thank you for scheduling your appointment with us.\n</p>
    <p style="margin-left:60px" ><strong>Appointment Date:</strong></p>
    <p style="margin-left:60px" ><strong>Appoinment Time:</strong></p>
    <p style="margin-left:10px" >We look forward to seeing you. Please feel free to contact us if you have any questions regarding this notification. Thank you!\n\n\n</p>
    <p style="margin-left:10px" ><strong>Company Name</strong></p>
    <p style="margin-left:10px" ><strong>+91 8767890657</strong></p>
    <p style="margin-left:10px" >company1234@gmail.com</p>

    </body>
    </html>
    """
    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    # send your email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('vermashanaya1234@gmail.com', 'sh12345678@#')
        smtp.send_message(message)
    print('Sent')
