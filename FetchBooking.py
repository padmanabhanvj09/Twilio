from sqlwrapper import gensql,dbget
import json
import datetime
def fetchbooking(request):
    today_date = datetime.datetime.utcnow().date()
    no = request.json["conf_no"]
    #no = request.json['mobile']
    try:    
        #d = {}
        #d['customer_mobile'] = no
        result = (dbget("select * from ivr_room_customer_booked  where customer_confirmation_number='"+no+"' order by customer_arrival_date desc limit 1"))
        result = json.loads(result)
        result = result[0]
        print(result)
        #return(json.dumps({"Return":"Record Retrieved Successfully","Return Code":"RRS", "Status": "Success",
         #                  "Status Code": "200", "Return Value":result},indent=2))
        dict1 = {"Return":"Record Retrieved Successfully","Return_Code":"RRS", "Status": "Success",
                          "ServiceMessage":"Success"}
        print(dict1,type(dict1))
        dict1.update(result)
        print(dict1)
        return(json.dumps(dict1))
    except:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))
   

   
