from sqlwrapper import gensql,dbget,dbput
import json
import datetime
from flask import Flask,request, jsonify

def Getchannelcounts(request):
    
    
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
    business_id = request.json['business_id']

    channelchatbot = json.loads(dbget("select count(*) from ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between  '"+date_from+"' and  '"+date_to+"' and channel in ('whatsapp')"))
    print(channelchatbot)

    #channelivr = json.loads(dbget("select count(*) from ivr_resevation where arrival_date between  '"+date_from+"' and  '"+date_to+"' and channel in ('IVR')"))
    #print(channelivr)

    ivrcount = json.loads(dbget("select count (*) from ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between  '"+date_from+"' and  '"+date_to+"' and channel in ('IVR')"))
    print(ivrcount)

    

    
    json_input = [{"title":"Chatbot","value":channelchatbot[0]['count']},
                  {"title":"Ivr","value":ivrcount[0]['count']}
                   ]
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success",
                      "Status_Code": "200","Returnvalue":json_input },indent=2))
    
    
    

    
