import requests
import json
import smtplib
from sqlwrapper import gensql,dbget
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from dateutil import parser
import sys
def sendemailwhatsapp(request):
     if request.method == 'GET':
          tfn = '+'+request.args['TFN']
          con_no = request.args['customer_confirmation_number']
     if request.method == 'POST':
          tfn = request.json['TFN']
          con_no = request.json['customer_confirmation_number']
     #print(name,email,type(email),message,conf_no,arrival,depature, room_type)
     sys.stdout.flush()
     #e = request.json
     #print(e)
     email = []
     Hotel_name = 'Kconnect24/7'
     print(con_no,type(con_no))    
     b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
     #print(b_id)
     bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
     print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))

     rate_day = json.loads(dbget("select * from customer_rate_detail where \
                          business_id='"+str(bi_id[0]['business_id'])+"' and customer_confirmation_number='"+con_no+"' "))
     print("rate_day",rate_day)
     
     d = json.loads(dbget("SELECT ivr_room_customer_booked.*,ivr_hotel_list.* FROM public.ivr_room_customer_booked \
                           join ivr_hotel_list on \
                           ivr_room_customer_booked.business_id = ivr_hotel_list.business_id\
                           where ivr_room_customer_booked.business_id='"+str(bi_id[0]['business_id'])+"' \
                           and ivr_room_customer_booked.customer_confirmation_number='"+str(con_no)+"' "))
     print("d",d)
     #print(d[0]['customer_amount'],type(d[0]['customer_amount']))
     #email = ['infocuit.santhakumar@gmail.com','infocuit.raja@gmail.com']
     
     email.append(d[0]['email'])
     email.append(d[0]['customer_email'])
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

          if len(receiver)==0:
               continue
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
              <table style="width:700px">
              <tr style="height:10">
              <td style="width:350px;"><p style="line-height:0.7 ">Arrival</p></td>
              <td style="width:350px;"><p style="float:center">Guest Name:</p></td>
              </tr>
              
              <tr style="height:10"
              <td style="width:350px;"><p style="line-height:0.7">"""+str(d[0]['customer_arrival_date'])+"""</p></td>
              <td style="width:350px;"><p >"""+str(d[0]['customer_name'])+"""</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Departure</p></td>
              <td style="width:350px"><p>Preferred Language</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7">"""+str(d[0]['customer_depature_date'])+"""</p></td>
              <td style="width:350px"><p >"""+str(d[0]['ivr_language'])+"""</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Hotel Name:</p></td>
              <td style="width:350px"><p >Channel</p></td>
              </tr>

              <tr>
              <td style="line-height:0.7;width:350px"><p >"""+str(d[0]['hotel_name'])+"""</p></td>
              <td style="width:350px"><p>"""+d[0]['channel']+"""</p></td>
              </tr>
              
              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Total Adult</p></td>
              <td style="width:350px"><p >Confirmation Number</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7">"""+str(d[0]['customer_adult'])+"""</p></td>
              <td style="width:350px"><p >"""+d[0]['customer_confirmation_number']+"""</p></td>
              </tr>
        
              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Total Child</p></td>
              <td style="width:350px"><p > Booked On</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7">"""+str(d[0]['customer_child'])+"""</p></td>
              <td style="width:350px"><p >"""+booked_on+"""</p></td>
              </tr>   
              
              <tr>
              <td style="width:350px"><p style="line-height:0.7;padding-top:10px;">Total Price</p></td>
              <td style="width:350px"><p > No Of Rooms</p></td>
              </tr>

              <tr>
              <td style="width:350px"><p style="line-height:0.7">"""+str(d[0]['customer_amount'])+"""</p></td>
              <td style="width:350px"><p >"""+str(d[0]['customer_no_of_rooms'])+"""</p></td>
              </tr>
            </table>
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

