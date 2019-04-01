import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendemailivr(request):
     name = request.json['name']
     email = request.json['email']
     message = request.json['message']
     conf_no = request.json['conf_no']
     hotel_name = request.json['hotel_name']
     arrival = request.json['arrival']
     depature = request.json['depature']
     room_type = request.json['room_type']
     
     sender = "siva.infocuit@gmail.com"
     receiver = email
     print(sender,type(sender),receiver,type(receiver))
     #message = request.json['message']
     #data = message.split("|")
     #print(data)
     subject = request.json['msg_subject']
     msg = MIMEMultipart()
     msg['from'] = sender
     msg['to'] = receiver
     msg['subject'] = subject
     # Create the body of the message (a plain-text and an HTML version)
     html = """\
     <html>
      <head></head>
      <body>
        <dl>
        <dt>
        <p><font size="2" color="black">hi,"""+name+"""</font></p>
        <p><font size="4" color="blue">"""+message+"""</font></p>
  
        <p><font size="2" color="black">Confirmation Number:"""+ conf_no+"""</font></p>
        <p><font size="2" color="black">Arrival Date:"""+ arrival+"""</font></p>
        <p><font size="2" color="black">Depature Date0:"""+ depature+"""</font></p>
        <p><font size="2" color="black">Room Type:"""+ room_type+"""</font></p>
        <p><font size="4" color="blue">  -"""+  hotel_name+"""</font></p>
        
        </dl>

      </body>
     </html>
     """
     
     #msg.attach(MIMEText(msg['subject'],'plain'))
     msg.attach(MIMEText(html,'html'))
     
     gmailuser = 'siva.infocuit@gmail.com'
     password = 'P@s$w0rds$'
     server = smtplib.SMTP('smtp.gmail.com',587)
     server.starttls()
     server.login(gmailuser,password)
     text = msg.as_string()
     server.sendmail(sender,receiver,text)
     print ("the message has been sent successfully")
     server.quit()
     return(json.dumps({'Return': 'Message Send Successfully',"Return_Code":"MSS","Status": "Success","Status_Code": "200"}, sort_keys=True, indent=4))
