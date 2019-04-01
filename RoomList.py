import json
from sqlwrapper import gensql,dbfetch,dbget,dbput

def roomlist(request):
    business_id = request.json['business_id']
    res = json.loads(dbget("select * from extranet_room_list where business_id='"+business_id+"' "))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Room_List":res},indent=2))
def insertroomlist(request):
 try: 
    d = request.json
    for i in d:
        print(i)
    print(i)
    no = json.loads(dbget("select count(*) from extranet_room_list"))
    print(no[0]['count'])
    id1 = no[0]['count']+1
    print(id1)
    i['id']= id1
    print(gensql('insert','extranet_room_list',i))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
 except:
     return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2)) 

def restriction(request):
    d = request.json
    l = []
    #gensql('insert','restriction',d)
    print(d)
    min_stay = {k:v for k,v in d.items() if v != '' if k in ('min_stay','min_stay_date')}
    max_stay = {k:v for k,v in d.items() if v != '' if k in ('max_stay','max_stay_date')}
    colse_arrival = {k:v for k,v in d.items() if v != ''  if k in ('close_arrival','close_arrival_to')}
    close_departure = {k:v for k,v in d.items() if v != ''  if k in ('close_departure','close_departure_to')}
    open_arrival = {k:v for k,v in d.items() if v != ''  if k in ('open_arrival','open_arrival_to')}
    open_departure = {k:v for k,v in d.items() if v != ''  if k in ('open_departure','open_departure_to')}
    house_close = {k:v for k,v in d.items() if v != ''  if k in ('house_close')}
    #print(len(min_stay),len(max_stay))
    business_id = d['business_id']
    print("busines_id",business_id,type(business_id))
    room_id = json.loads(dbget("select room_id from configration where business_id='"+str(business_id)+"' "))

    r_id = ''
    for i in room_id:
        
        if r_id == '':
            r_id += "'"+str(i['room_id'])+"'"
        else:
            r_id += ','+"'"+str(i['room_id'])+"'"
    print(r_id,type(r_id))        
    
    
    l.append(r_id)
    min_stays =d.get('min_stay')
    max_stays = d.get('min_stay_date')
    print(l)
    
    if len(min_stay) != 0:
        print(dbput("update extranet_availableroom set min_stay='"+str(min_stays)+"' where room_date='"+str(max_stays)+"' and room_id in (%s)" % ",".join(map(str,l))) )
   
    if len(max_stay) != 0:
        print(dbput("update extranet_availableroom set max_stay='"+str(d['max_stay'])+"' where room_date='"+str(d['max_stay_date'])+"' and room_id in (%s)" % ",".join(map(str,l))))

    if len(house_close) != 0:
        print(dbput("update extranet_availableroom set house_close='1' where room_date='"+str(d['house_close'])+"' and room_id in (%s)" % ",".join(map(str,l))))

    if len(colse_arrival) != 0:
       print(dbput("update extranet_availableroom set close_arrival='1' where room_date between '"+str(d['close_arrival'])+"' and '"+str(d['close_arrival_to'])+"' and room_id in (%s)" % ",".join(map(str,l))))
    if len(close_departure) != 0:
       print(dbput("update extranet_availableroom set close_departure='1' where room_date between '"+str(d['close_departure'])+"' and '"+str(d['close_departure_to'])+"' and room_id in (%s)" % ",".join(map(str,l))))
    if len(open_arrival) != 0:
        print(dbput("update extranet_availableroom set close_arrival='0' where room_date between '"+str(d['open_arrival'])+"' and '"+str(d['open_arrival_to'])+"' and room_id in (%s)" % ",".join(map(str,l))))
    if len(open_departure) != 0:
        print(dbput("update extranet_availableroom set close_departure='1' where room_date between '"+str(d['open_departure'])+"' and '"+str(d['open_departure_to'])+"' and room_id in (%s)" % ",".join(map(str,l)) ))
    
    
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def select_restriction(request):
    business_id = request.json['business_id']
    res = json.loads(dbget("select * from restriction where business_id= '"+business_id+"' "))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
