import json
import datetime
import calendar
from sqlwrapper import gensql,dbget,dbput
def insertcancelpolicy(request):
    d = request.json
    print(d)
    e = { k : v for k,v in d.items() if k in ('business_id')}
    f = { k : v for k,v in d.items() if k not in ('business_id')}
    sql = json.loads(dbget("select count(*) from cancel_policy where business_id='"+d['business_id']+"' "))
    print(sql[0]['count'])
    if sql[0]['count'] != 0:
        print(gensql('update','cancel_policy',f,e))
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    print(gensql('insert','cancel_policy',d))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

    
def QueryStatistics(request):
    b_id = request.json['business_id']
    #print(b_id)
    today = datetime.datetime.utcnow().date()
    bid = json.loads(dbget("select id from ivr_hotel_list where business_id='"+b_id+"'"))
    #print(bid[0]['id'])
    sql = json.loads(dbget("select customer_arrival_date,customer_room_type from ivr_room_customer_booked join ivr_hotel_list on \
                            ivr_room_customer_booked.id = ivr_hotel_list.id where  \
                            ivr_hotel_list.id='"+str(bid[0]['id'])+"' and \
                            customer_arrival_date < '"+str(today)+"' order by customer_arrival_date desc"))
    #print(sql)
    
    a,b,c,d = 0,0,0,0
    e,f,g,h = 0,0,0,0
    k,l,m,n = 0,0,0,0
    m1,m2,m3,result = {},{},{},[] 
    for i in sql:
        #print(i)
        #print(i['customer_arrival_date'],type(i['customer_arrival_date']))
        j = datetime.datetime.strptime(i['customer_arrival_date'], "%Y-%m-%d").date()
        #print(i,type(i))
        
        if j.month == today.month:
            if i['customer_room_type'] == "Delux Room":
                a += 1
            elif  i['customer_room_type'] == "Standard Room":
                b += 1
            elif  i['customer_room_type'] == "Superior Room":
                c += 1
            elif i['customer_room_type']  == "Deluxe Suite":
                d += 1
        elif j.month == today.month-1:
            if i['customer_room_type'] == "Delux Room":
                e += 1
            elif  i['customer_room_type'] == "Standard Room":
                f += 1
            elif  i['customer_room_type'] == "Superior Room":
                g += 1
            elif i['customer_room_type']  == "Deluxe Suite":
                h += 1            
        elif j.month == today.month-2:
            if i['customer_room_type'] == "Delux Room":
                k += 1
            elif  i['customer_room_type'] == "Standard Room":
                l += 1
            elif  i['customer_room_type'] == "Superior Room":
                m += 1
            elif i['customer_room_type']  == "Deluxe Suite":
                n += 1            
    m1["month"] = ""+calendar.month_name[today.month]+""
    m1['deluxRoomTotal'] = a
    m1['standardRoomTotal'] = b
    m1['superiorRoomTotal'] = c
    m1['deluxSuiteRoomTotal'] = d
    m1['year'] = ""+str(j.year)+""
    result.append(m1)
    m2["month"] = ""+calendar.month_name[today.month-1]+""
    m2['deluxRoomTotal'] = e
    m2['standardRoomTotal'] = f
    m2['superiorRoomTotal'] = g
    m2['deluxSuiteRoomTotal'] = h
    m2['year'] = ""+str(j.year)+""
    result.append(m2)
    m3["month"] = ""+calendar.month_name[today.month-2]+""
    m3['deluxRoomTotal'] = k
    m3['standardRoomTotal'] = l
    m3['superiorRoomTotal'] = m
    m3['deluxSuiteRoomTotal'] = n
    m3['year'] = ""+str(j.year)+""
    result.append(m3)
    print(result)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":result},indent=2))
