from sqlwrapper import dbget,dbput,gensql
import json
import random

def Insert_Ivr_Reservation(request):
    d = request.json
    confirmation = (random.randint(1000,9999))
    d['confirmation_number'] = confirmation
    gensql('insert','ivr_resevation',d)
    confirmation = d.get('confirmation_number')
    a = {"Return":"Record Inserted Successfully","ReturnCode":"RIS","ReturnMessage":"Success","Confirmation_Number":confirmation}
    return(json.dumps(a,indent=2))

def Query_Reservation(request):
    b_id = request.json
    d = json.loads(dbget("SELECT ivr_room_customer_booked.*,ivr_hotel_list.* FROM \
                          public.ivr_room_customer_booked join ivr_hotel_list on \
                          ivr_room_customer_booked.business_id = ivr_hotel_list.business_id where \
                          ivr_room_customer_booked.business_id='"+b_id['business_id']+"'"))
                              
    
    #print(d)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","result":d},indent=2))

def Query_Rate_Per_day(request):
    confi_num = request.json['conf_num']
    b_id = request.json['business_id']
    #print(request.json)
    d = json.loads(dbget("select * from customer_rate_detail where \
                          business_id='"+b_id+"' and customer_confirmation_number='"+confi_num+"' "))
        
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","result":d},indent=2))
