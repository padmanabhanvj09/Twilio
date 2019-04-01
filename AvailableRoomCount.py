import json
from sqlwrapper import gensql,dbfetch,dbget

def availableroomcount(request):
    d = request.json
    print(d)
    print(d['business_id'])
    res = json.loads(dbget("select available_count,booked_count,room_name from room_to_sell \
                          join configration on configration.room_id = room_to_sell.room_id \
                          where room_date = '"+d['available_date']+"' and room_to_sell.business_id = '"+str(d['business_id'])+"'"))
    print(res,type(res))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Available_Rooms":res},indent=2))
