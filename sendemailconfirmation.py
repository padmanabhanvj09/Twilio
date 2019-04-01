import requests
import json
import smtplib
from sqlwrapper import gensql,dbget
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from dateutil import parser
import sys
def sendemailconfirmation(request):
     #print(name,email,type(email),message,conf_no,arrival,depature, room_type)
     sys.stdout.flush()
     e = request.json
     print(e)
     Hotel_name = 'Kconnect24/7'
     business_id = request.json['business_id']
     con_no = request.json['customer_confirmation_number']
     print(con_no,type(con_no))    
  
  

     rate_day = json.loads(dbget("select * from customer_rate_detail where \
                          business_id='"+str(business_id)+"' and customer_confirmation_number='"+con_no+"' "))
     print("rate_day",rate_day)
     
     d = json.loads(dbget("SELECT ivr_room_customer_booked.*,ivr_hotel_list.* FROM public.ivr_room_customer_booked \
                           join ivr_hotel_list on \
                           ivr_room_customer_booked.business_id = ivr_hotel_list.business_id\
                           where ivr_room_customer_booked.business_id='"+str(business_id)+"' \
                           and ivr_room_customer_booked.customer_confirmation_number='"+str(con_no)+"' "))
     print("d",d)
     #print(d[0]['customer_amount'],type(d[0]['customer_amount']))
     email = ['infocuit.banupriya@gmail.com','infocuit.raja@gmail.com']
     
     #email.append(d[0]['email'])
     #email.append(d[0]['customer_email'])
     print(email)
     on = d[0]['booked_date']
     print(on[:11], type(on[:11]))
     booked_on = parser.parse(on[:11]).date().strftime('%Y-%m-%d')
     sender = "infocuit.testing@gmail.com"
     
     t_body = """
                       <tr style="border:1px solid gray">
                         <th align="left">Date</th>
                         <th align="left">Price Per Night in $</th>
                       </tr>

             """

     for rate in rate_day:
         print(rate)
         t_body += """
                       <tr style="border:1px solid gray">
                         <td>"""+rate['rate_date']+"""</td>
                         <td align="left">"""+str(rate['amount'])+"""</td>
                       </tr>
                   """
     t_body += """
                       <tr style="border:1px solid gray">
                         <td><b>Total</b></td>
                         <td align="left">"""+str(d[0]['customer_amount'])+"""</td>
                       </tr>
              """
     print("t_body-----------------------")
     print(t_body)
     
     for receiver in email:

          
          #print(sender,type(sender),receiver,type(receiver))
          subject = "Hotel Booking"
          msg = MIMEMultipart()
          msg['from'] = sender
          msg['to'] = receiver
          msg['subject'] = subject
          

          html = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Title of the document</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>

<body>
 <div class="panel panel-primary">
        <div class="panel-body">
          <div class="row" style="border:1px solid lightgrey;margin:10px ">
            <div class="col-md-4" style="padding:10px;">
            <h1 align="center" style="color:#216CEC;border-bottom:1px solid grey">konnect 247</h1>
            <br>
              <p><b> Dear Customer,</b></p>
              <p style="margin-left:100px">Thank you for Choosing our Hotel, It is our pleasure to confirm your reservation as follows. </p>
              
              <p style="line-height:0.7;padding-top:20px;"> <span>Arrival</span> <span style="margin-left:25em">Guest Name:</span></p> 
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_arrival_date'])+"""</span> <span style="margin-left:23em">"""+str(d[0]['customer_name'])+"""</span></p>
                     
              <p style="line-height:0.7;padding-top:10px;"><span>Departure</span> <span style="margin-left:23.5em">Preferred Language</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_depature_date'])+"""</span><span style="margin-left:23em">"""+str(d[0]['ivr_language'])+"""</span></p>
              
              <p style="line-height:0.7;padding-top:10px;"><span>Hotel Name:</span><span style="margin-left:22.5em">Channel</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['hotel_name'])+"""</span><span style="margin-left:22.5em">"""+d[0]['channel']+"""</span></p>
              
              <p style="line-height:0.7;padding-top:10px;"><span>Total</span> Adult <span style="margin-left:23em">Confirmation Number</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_adult'])+"""</span><span style="margin-left:27.5em">"""+d[0]['customer_confirmation_number']+"""</span></p>
        
              <p style="line-height:0.7;padding-top:10px;"><span>Total Child</span><span style="margin-left:23em"> Booked On</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_child'])+"""</span><span style="margin-left:27.5em">"""+booked_on+"""</span></p>   
              
              <p style="line-height:0.7;padding-top:10px;"><span>Total Price</span><span style="margin-left:23em"> No Of Rooms</span></p>
              <p style="line-height:0.7"><span>"""+str(d[0]['customer_amount'])+"""</span><span style="margin-left:25em">"""+str(d[0]['customer_no_of_rooms'])+"""</span></p>
            
                <hr>
                <p style="line-height:0.7">Room Type</p>
                <p style="line-height:0.7">"""+d[0]['customer_room_type']+"""</p> 
             
                <p style="line-height:0.7;padding-top:10px;">Guest Name</p>
                <p style="line-height:0.7">"""+str(d[0]['customer_name'])+""" </p>  
               
                <p style="line-height:0.7;padding-top:10px;">Max Guest</p>
                <p style="line-height:0.7">"""+str(d[0]['customer_adult']+d[0]['customer_child'])+"""</p>
                
                <p style="line-height:0.7;padding-top:10px;">Room Options</p>
               
               <p style="float:left">   <img src="https://www.riversidehotel.com.au/wp-content/uploads/2016/01/RH-12.jpg" alt="" width="400px" height="250px"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
               <span style="float:left;"> <table style=" border:1px solid gray; width:400px;height:250px">
                     <tbody style="border:1px solid gray">
                     """+t_body+"""
                     </tbody>
                   </table>
                   </span>
                </p> 
                 <br>
                 <p><b>Address:</b></p>
                 <p style="margin-left:30px;line-height:0.7"> No,25, 1st cross street,</p>
                 <p style="margin-left:30px;line-height:0.7"> New Colony,</p>
                 <p style="margin-left:30px;line-height:0.7"> Chrompet,</p>
                 <p style="margin-left:30px;line-height:0.7"> Chennai</p>
                 <h3>Regards,</h3>
                 <p>Admin- Hotel Management</p>
                 <hr>
                 <h5 align="center" style="color:red"> This is an Auto generated Email, Please do not reply.</h5> 
                 
              </div>
          
		    
            <br>
          </div>
        
        </div>
      </div>
            
</body>

</html>
          """

          msg.attach(MIMEText(html,'html'))
          
          gmailuser = 'infocuit.testing@gmail.com'
          password = 'infocuit@123'
          server = smtplib.SMTP('smtp.gmail.com',587)
          server.starttls()
          server.login(gmailuser,password)
          text = msg.as_string()
          server.sendmail(sender,receiver,text)
          print ("the message has been sent successfully")
          server.quit()
    
     return(json.dumps({'Return': 'Message Send Successfully',"Return_Code":"MSS","Status": "Success","Status_Code": "200"}, sort_keys=True, indent=4))

