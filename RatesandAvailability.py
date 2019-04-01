import json
import datetime
from sqlwrapper import gensql,dbfetch,dbget

def ratesandavailability(request):
    
    req = request.json
    #print(req)
    a = {k:v for k,v in req.items() if v == '' }
    #print(len(a))
    if len(a) != 0:
       from_date = datetime.datetime.utcnow().date()
       to_date = from_date +datetime.timedelta(days=14)
    else:
       from_date = datetime.datetime.strptime(req['from_date'],'%Y-%m-%d').date()
       to_date = datetime.datetime.strptime(req['to_date'],'%Y-%m-%d').date()
       
    res_from_date = from_date
    res_to_date = to_date 

    res = json.loads(dbget("SELECT extranet_availableroom.business_id,configration.room_id, configration.room_name ,\
                            room_date, \
                            room_rate, room_open, s_no,   rate_plan.rate_plan_id,rate_plan.rate_plan, \
                            min_stay, max_stay, close_arrival, close_departure, house_close, extra_adult_rate \
	                    FROM public.extranet_availableroom join configration on extranet_availableroom.room_id = configration.room_id\
	                    join rate_plan on extranet_availableroom.rate_plan_id = rate_plan.rate_plan_id \
                            where configration.business_id='"+req['business_id']+"' and room_date \
	                    between '"+str(from_date)+"' and '"+str(to_date)+"' \
                            order by room_id,rate_plan_id,room_date"))
    
    #print(res,type(res),len(res))
    
    room_id,colle_rooms,rate_plan_id = [],[],[]
    count_type, count_plan = 0,0
    
    for i in res:
      #print(i,type(i),res.index(i))  
      #l={k:v for k,v in i.items() if k in('business_id','room_id','room_name','room_date','rate_plan','rate_plan_id','room_open','min_stay','max_stay','room_rate','extra_adult_rate','booked_count',
      #                                    'close_arrival','close_departure','house_close') }
      #print('lll',i['room_id'],i['rate_plan_id'])
      if i['room_id'] in  room_id:
          pass
      else:
          
          rate_plan = []
          rate_plan_id = []
          count_plan = 0
          count_type = count_type+1
          room_id.append(i['room_id'])
          print("room_iddddd",room_id)    
      if i['rate_plan_id'] in rate_plan_id:
         pass
      else:
          count_plan = count_plan+1
          rate_plan_id.append(i['rate_plan_id'])
          print("plan_iddddd",rate_plan_id)    
      k={}
      k['room_plan'+str(count_plan)] = i
      
      j={}
      j['room_type'+str(count_type)] = k
      colle_rooms.append(j)         
      
      #print(i)
    #print(room_name)
    #print("colle_rooms",colle_rooms,len(colle_rooms))
    
    r_key,p_key = [],[]
    total,room_total,plan_total,plan_total01 = [],[],[],[]
    room_to_sell = []
    for i in colle_rooms:
        #print("i",i,colle_rooms.index(i))
        room_k = [k for k,v in i.items()]
        rooms = i[""+room_k[0]+""]
        #print("rrrrrrrrrrrrrrrrrrrrrooms  ",rooms)
        
        plan_k = [k for k,v in rooms.items()]
        plans = rooms[""+plan_k[0]+""]
        #print("ppppppppppppppppppppplans  ",plans)
        
        if room_k[0] not in r_key:           
           r_key.append(room_k[0])
           plan_total = []
           room_to_sell = json.loads(dbget("select room_to_sell.*, configration.room_name as con_room_name from room_to_sell \
                             join configration on room_to_sell.room_id = configration.room_id where room_date between  \
                             '"+str(from_date)+"' and '"+str(to_date)+"' and  \
                             room_to_sell.business_id='"+req['business_id']+"' and \
                             room_to_sell.room_id='"+str(plans['room_id'])+"' order by room_date "))           
           total.append({""+room_k[0]+"":{'room_name': plans['room_name'],'room_to_sell':room_to_sell,'plans':plan_total}})
        else:
           pass

        plan_total.append(rooms)
        
    #print(total)
    Date = []
    while from_date <= to_date:
        Date.append(str(from_date))
        from_date+=datetime.timedelta(days=1)
    #print(Date)       
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":total,
                       "from_date":str(res_from_date),"to_date":str(res_to_date),"Date":Date},indent=2))   
  
 
 
def daterange(request):
    res = request.json
    print(res,type(res))
    a = { k : v for k,v in res.items() if k not in ('st_date','ed_date','days','available_count') }
    print("a",a)
    x = { k : v for k,v in a.items() if k not in ('business_id','room_id','rate_plan_id') }
    y = { k : v for k,v in a.items() if k  in ('business_id','room_id','rate_plan_id') }
    z = { k : v for k,v in a.items() if k  in ('business_id','room_id') }
    print("zzz",z)
    print("x",x)
    print("y",y)
    days = res['days']
    #day0 = [ k  for k,v in res.items() if v == 0 ]
    day1 = [ k  for k,v in days.items() if v != 0 ]
    #print(a,days,day1)
    from_date = request.json['st_date']
    to_date = request.json['ed_date']
    from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d').date()
    
    while from_date <= to_date:
          #print(from_date,from_date.strftime("%A")[0:3].lower())
          if from_date.strftime("%A")[0:3].lower() in day1:
             y1={} 
             y1 = y
             y1['room_date'] = from_date
             count = json.loads(gensql('select','extranet_availableroom','count(*)',y1) )
             #print(count,type(count),count[0]['count'])
             if count[0]['count'] == 0:
               #print("insert",from_date)  
               #a['booked_count'] = 0
               a['room_date'] = from_date
               a['room_open'] = 1
               #print("insert a",a)
               gensql('insert','extranet_availableroom',a)
             else:
               #print("update",from_date)  
               gensql('update','extranet_availableroom',x,y)
          else:
              pass
          from_date+=datetime.timedelta(days=1)
     
    from_date = request.json['st_date']
    to_date = request.json['ed_date']
    from_date = datetime.datetime.strptime(from_date,'%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(to_date,'%Y-%m-%d').date()
    
    z1 = z.copy()
    sell_detail = z1
    sell_detail['available_count'] = res['available_count']
    sell_detail['booked_count'] = 0
    u_x = {'available_count':res['available_count']}
    while from_date <= to_date:
            z['room_date'] = from_date
            #print("zzzzz",z)
            count = json.loads(gensql('select','room_to_sell','count(*)',z) )
            if count[0]['count'] == 0:
                print("insert a",a)
                sell_detail['room_date'] = from_date
                gensql('insert','room_to_sell',sell_detail)
            else:
               print("update",from_date)
               z['room_date'] = from_date
               gensql('update','room_to_sell',u_x,z)
            from_date+=datetime.timedelta(days=1)   
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":""},indent=2))
    
def room_open_update(request):
    d = request.json['records']
    print(d,type(d))
    
    for i in d:
        j = {k:v for k,v in i.items() if k not in ('s_no')}
        ids = {k:v for k,v in j.items() if k in ('rate_plan_id','room_id','business_id','room_date')}
        
        values = {k:v for k,v in j.items() if v!=None if k not in ('rate_plan_id','room_id','business_id',
                                                        'rate_plan','room_name','room_date')}
        
        gensql('update','extranet_availableroom',values,ids)

    return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Record Updated Successfully',
                        'ReturnCode':'RUS'}], sort_keys=True, indent=4))    

def room_to_sell_update(request):
    d = request.json['records']
    print(d,type(d))
    
    for i in d:
        j = {k:v for k,v in i.items() if k not in ('sell_id')}
        ids = {k:v for k,v in j.items() if k in ('room_id','business_id','room_date')}
        
        values = {k:v for k,v in j.items() if v!=None if k not in ('room_id','business_id','room_date','booked_count','con_room_name')}
        
        gensql('update','room_to_sell',values,ids)
    
    return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Record Updated Successfully',
                        'ReturnCode':'RUS'}], sort_keys=True, indent=4))    
 

    


