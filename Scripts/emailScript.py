import smtplib
from email.mime.text import MIMEText

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password):

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr_list

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

sendemail('timothy.ruscica@gmail.com', 'timothy.ruscica@gmail.com',[],'Validate Email', 'This is a test','timothy.ruscica', '335557567')
