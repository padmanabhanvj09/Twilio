import json
import datetime
from sqlwrapper import gensql,dbfetch,dbget

def querydiscount(request):
    res = request.json
    print(res)
    d = { k : v for k,v in res.items() if k not in ('room_date')}
    print(d)
    res_id = json.loads(gensql('select','extranet_room_list','id,room_type',d))
    print(res_id)
    id1 = ''
    room_type = []
    for i in res_id:
        print(i)
        if len(id1) == 0:
            id1 += "'"+str(i['id'])+"'"
            print(id1)
        else:
            id1 += ','+"'"+str(i['id'])+"'"
    print(room_type,type(room_type))
    print(id1)
    result = json.loads(dbget("select *  from extranet_discount where id in ("+id1+") and room_date = '"+res['room_date']+"'"))
    print("resutl",result,type(result))
    e = { k : v for k,v in result[0].items() if k not in ('id')}
    print(e)
    id2 = ''
    for i in result:
        if len(id2) == 0:
           id2 += "'"+str(i['id'])+"'"
        else:
           id2 += ','+"'"+str(i['id'])+"'"
    print(id2)
    res = json.loads(dbget("select room_type from  extranet_room_list where id in ("+id2+")"))
    print(res,type(res))
    for j in res:
        room_type.append(""+str(j['room_type'])+"")
    
    e['room_type'] = room_type
    print(e)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":e},indent=2))
