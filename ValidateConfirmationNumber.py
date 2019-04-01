from sqlwrapper import gensql,dbget
import json

def validateconfirmationnumber(request):
    no = request.json['conf_no']
    print(no)
    c_no = b_id = json.loads(dbget("select count(*) from ivr_room_customer_booked where \
                                    customer_confirmation_number= '"+no+"' "))
    print(c_no[0]['count'],type(c_no[0]['count']))
    if c_no[0]['count'] != 0 : 
       return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"}))
    else:
       return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"})) 
