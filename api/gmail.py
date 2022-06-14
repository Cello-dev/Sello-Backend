import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(message):
    try:
        gmail_user = 'selloapidev@gmail.com'
        gmail_password = 'gqpccevfllakqpbv'
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, message['To'], message.as_string())
        server.close()
        return True
    except:
        return False

def make_verify_email(to, code):
    message = MIMEMultipart()
    message['To'] = to
    message['From'] = 'selloapidev@gmail.com'
    message['Subject'] = 'Sello Email Verification'

    html = '''
        <html>
            <body>
                <h1>Please use the code below to verify your email.</h1>
                <h2>{code}</h2>
                <p>Enter your code <a href="http://127.0.0.1:8000/verifyemail">here</a> to verify your email address.</p>
                <p>If this was not you simply ignore this email.</p>
            </body>
        </html>
        '''.format(code=code)
    body = MIMEText(html, "html")
    message.attach(body)
    return message

def make_reset_email(to, code):
    message = MIMEMultipart()
    message['To'] = to
    message['From'] = 'selloapidev@gmail.com'
    message['Subject'] = 'Sello Account Recovery'

    html = '''
        <html>
            <body>
                <h1>Please use the code below to reset your password.</h1>
                <h2>{code}</h2>
                <p>Please enter your code <a href="http://127.0.0.1:8000/verifyemail">here</a> to reset your password.</p>
                <p>If this was not you simply ignore this email.</p>
            </body>
        </html>
        '''.format(code=code)
    body = MIMEText(html, "html")
    message.attach(body)
    return message