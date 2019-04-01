from sqlwrapper import gensql,dbget,dbput
import json
import datetime

def cancelcurrentbooking(request):
   try: 
    no = request.args["conf_no"]
    d = {}
    d['customer_confirmation_number'] = no
    res = (gensql('select','ivr_room_customer_booked','*',d))
    print(res)
    if len(res) == 2 :
        return(json.dumps({"Return":"Invalid Confirmation Number","Return_Code":"ICN","Status": "Success",
                      "Status_Code": "200"},indent=2))  
    result  = json.loads(res)
    data = result[0]
    date = data['customer_arrival_date']
    date1 = data['customer_depature_date']
    arrival_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    depature_date = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    str_date = "'"+str(arrival_date)+"'"
    while arrival_date < depature_date:
          arrival_date = arrival_date+datetime.timedelta(days=1)
          str_date += ","+"'"+str(arrival_date)+"'"
    #print(str_date)    
    room_type = data['customer_room_type']
    #print(room_type)
    no_of_room = data['customer_no_of_rooms']
    b_id = data['id']
    #print(no_of_room,b_id)
    
    today_date = datetime.datetime.utcnow().date()
    if arrival_date < today_date:
       return(json.dumps({"Return":"Can't Cancel Reservation","Return_Code":"CCR","Status": "Success",
                      "Status_Code": "200"},indent=2))
    s = {}
    s['customer_booked_status'] = "canceled"    
    print(gensql('update','ivr_room_customer_booked',s,d))
    bu_id = json.loads(dbget("select business_id from ivr_hotel_list where id = "+str(b_id)+" "))
    #print(bu_id[0]['business_id'])
    r_id = json.loads(dbget("select id from extranet_room_list where business_id= '"+bu_id[0]['business_id']+"' \
                             and room_type = '"+room_type+"' "))
    #print(r_id[0]['id'])
    print(dbput("update extranet_availableroom set available_count = available_count+"+str(no_of_room)+" where \
                       id= "+str(r_id[0]['id'])+" and room_date in ("+str_date+")"))
    return(json.dumps({"Return":"Reservation Canceled Sucessfully","Return_Code":"RCS","Status": "Success",
                      "Status_Code": "200"},indent=2))
   except:
      return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"}))
   
  
