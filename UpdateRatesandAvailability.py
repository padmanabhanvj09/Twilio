import json
import datetime
from sqlwrapper import gensql,dbfetch,dbget

def updateratesandavailability(request):
    d = request.json
    print(d)
    e = { k : v for k,v in d.items() if k in ('business_id','room_type','room_name')}
    f = { k : v for k,v in d.items() if k not in ('business_id','room_type','room_name')}
    print(e)
    print(f)
    res = json.loads(gensql('select','extranet_room_list','id',e))
    #print(res[0]['id'],type(res[0]['id']))
    f['id'] = res[0]['id']
    g = { k : v for k,v in f.items() if k  in ('id','room_date')} 
    result = json.loads(gensql('select','extranet_availableroom','count(*)',g))
    print(result[0]['count'],type(result[0]['count']))
    if result[0]['count'] != 0:
        u = { k : v for k,v in f.items() if k  in ('available_count','room_rate')} 
        sql = gensql('update','extranet_availableroom',u,g)
        print(sql)
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Record Updated"},indent=2))
    else:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Record Not Exists"},indent=2))
