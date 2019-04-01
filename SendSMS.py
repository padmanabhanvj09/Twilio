from sqlwrapper import gensql,dbput
import urllib.request
import time
import json

def sendsms(request):
     #print(request.json)
     countrycode = request.json['countrycode']
     #print(countrycode)
     name = request.json['name']
     phone = request.json['phone']
     message = request.json['message']
     conf_no = request.json['conf_no']
     hotel_name = request.json['hotel_name']
     arrival = request.json['arrival']
     depature = request.json['depature']
     room_type = request.json['room_type']
     all_message = ("Dear "+name+", "+message+".  Confirmation Number is "+conf_no+", Arrival Date: "+arrival+", Depature Date:"+depature+", Room Type:"+room_type+". by "+hotel_name+"")
     url = "https://control.msg91.com/api/sendhttp.php?authkey=195833ANU0xiap5a708d1f&mobiles="+phone+"&message="+all_message+"&sender=Infoit&route=4&country="+countrycode+""
     req = urllib.request.Request(url)
     with urllib.request.urlopen(req) as response:
         the_page = response.read()
         the_page = the_page[1:]
         print(the_page)
         the_page = str(the_page)
     return(json.dumps({"Return":"SMS Sent Successfully","Return_Code":"SSS","Status": "Success","Status_Code": "200","Key":the_page},indent =2))


      
def UpdateSMSmessage(request):
     sms = request.json['sms']
     confirmation = request.json['confirmation_number']
     
     sql_value = dbput("update ivr_resevation set sms = '"+sms+"' where confirmation_number ='"+confirmation+"' ")
     print(sql_value)
    
     return(json.dumps({"Return":"Record Updated Successfully","Return_Code":"RUS","Status": "Success","Status_Code": "200"},indent =2))
def Updateivrsmsmessage(request):
     sms = request.json['send_sms']
     confirmation = request.json['customer_confirmation_number']
     sql_value = dbput("update ivr_room_customer_booked set send_sms = '"+sms+"' where customer_confirmation_number ='"+confirmation+"' ")
     print(sql_value)
    
     return(json.dumps({"Return":"Record Updated Successfully","Return_Code":"RUS","Status": "Success","Status_Code": "200"},indent =2))


