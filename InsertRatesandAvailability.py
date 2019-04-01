import json
import datetime
from sqlwrapper import gensql,dbget,dbput
def insertratesandavailability(request):
    d = request.json
    e = { k : v for k,v in d.items() if k in ('business_id','room_type')}
    f = { k : v for k,v in d.items() if k in ('rooms')}
    res = json.loads(gensql('select','extranet_room_list','id',e))
    print(res[0]['id'],type(res[0]['id']))
    f = f['rooms']
    for i in f:
      print(i)  
      sql = json.loads(dbget("select count(*) from extranet_availableroom where id = '"+str(res[0]['id'])+"'\
                             and room_date = '"+i['date']+"' "))
      print(sql[0]['count'])
      if sql[0]['count'] == 0:
         if  i['Available_Room_Count'] == "" and i['Price'] == "":
             pass
         elif i['Available_Room_Count'] == "":
           dbput("INSERT INTO public.extranet_availableroom(\
	        id, room_date,room_rate,room_open)\
	        VALUES ("+str(res[0]['id'])+", '"+i['date']+"',"+str(i['Price'])+","+str(i['room_open'])+" )")
         elif i['Price'] == "":
           dbput("INSERT INTO public.extranet_availableroom(\
	        id, room_date, available_count,room_open)\
	        VALUES ("+str(res[0]['id'])+", '"+i['date']+"', "+str(i['Available_Room_Count'])+","+str(i['room_open'])+")")
         else:
             dbput("INSERT INTO public.extranet_availableroom(\
	        id, room_date, available_count, room_rate,room_open)\
	        VALUES ("+str(res[0]['id'])+", '"+i['date']+"', "+str(i['Available_Room_Count'])+", "+str(i['Price'])+","+str(i['room_open'])+")")
      else:
         if i['Available_Room_Count'] == "" and  i['Price'] == "":
             pass
         elif i['Available_Room_Count'] == "": 
           dbput("UPDATE public.extranet_availableroom set room_rate="+str(i['Price'])+",room_open="+i['room_open']+"  WHERE  id="+str(res[0]['id'])+" and room_date='"+i['date']+"'  ") 
         elif i['Price'] == "":
            dbput("UPDATE public.extranet_availableroom set available_count="+str(i['Available_Room_Count'])+",room_open="+i['room_open']+" WHERE  id="+str(res[0]['id'])+" and room_date='"+i['date']+"'  ")
         else:
             dbput("UPDATE public.extranet_availableroom\
	        set available_count="+str(i['Available_Room_Count'])+", room_rate="+str(i['Price'])+",room_open="+str(i['room_open'])+"\
	        WHERE  id="+str(res[0]['id'])+" and room_date='"+i['date']+"'")  
             
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
