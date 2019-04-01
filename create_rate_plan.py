import json
from sqlwrapper import gensql,dbfetch,dbget,dbput

def create_rate_plan(request):
    res = request.json
    print(res)
    a = { k : v for k,v in res.items()  if k not in ('room_types_id','packages_id')}
    for rm_id in res['room_types_id']:
        for pl_id in res['packages_id']:
            a['room_types_id'] = rm_id
            a['packages_id'] = pl_id
            gensql('insert','rate_plan',a)
    rate_id = json.loads(gensql('select','rate_plan','max(rate_plan_id) as plan_id',a))
    #print(rate_id)
    for i in res['room_types_id']:
        rate_plan ={}
        rate_plan['rate_plan_id'] = rate_id[0]['plan_id']
        rate_plan['room_id'] = i
        rate_plan['business_id'] = res['business_id']
        gensql('insert','room_type_select',rate_plan)
    for i in res['packages_id']:
        rooms ={}
        rooms['rate_plan_id'] = rate_id[0]['plan_id']
        rooms['packages_id'] = i
        rooms['business_id'] = res['business_id']
        gensql('insert','package_select',rooms)
        
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def update_rate_plan(request):
    res = request.json
    print(res)
    a = { k : v for k,v in res.items() if v != '' if k  not in ('business_id','room_types_id','packages_id')}
    e = { k : v for k,v in res.items() if v != '' if k   in ('business_id','rate_plan_id')}
    
    #gensql('update','rate_plan',a,e)
    dbput("delete from package_select where rate_plan_id='"+str(res['rate_plan_id'])+"' and business_id='"+res['business_id']+"'")
    dbput("delete from room_type_select where rate_plan_id='"+str(res['rate_plan_id'])+"' and business_id='"+res['business_id']+"'")
    for i in res['packages_id']:
        rooms ={}
        rooms['rate_plan_id'] = res['rate_plan_id']
        rooms['packages_id'] = i
        rooms['business_id'] = res['business_id']
        gensql('insert','package_select',rooms)
    for i in res['room_types_id']:
        rate_plan ={}
        rate_plan['rate_plan_id'] = res['rate_plan_id']
        rate_plan['room_id'] = i
        rate_plan['business_id'] = res['business_id']
        gensql('insert','room_type_select',rate_plan)
    gensql('update','rate_plan',a,e)    
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def delete_rate_plan(request):
    plan_id = request.json['rate_plan_id']
    b_id = request.json['business_id']
    dbput("delete from rate_plan where rate_plan_id="+str(plan_id)+" and business_id = '"+b_id+"' ")
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def select_rate_plan(request):
    business_id = request.json['business_id']
    '''
    res = json.loads(dbget("select rate_plan.rate_plan_id, rate_plan.rate_plan, cancellation_policy.*, room_id, room_name, packages.*, start_date, end_date, rate_plan.business_id\
                            from rate_plan join cancellation_policy on rate_plan.cancellation_policy_id = cancellation_policy.policy_id \
                            join configration on rate_plan.room_types_id = configration.room_id \
                            join packages on rate_plan.packages_id = packages.packages_id \
                            where rate_plan.business_id="+business_id+" "))
    '''
    res = json.loads(dbget("select rate_plan.rate_plan_id, rate_plan.rate_plan, cancellation_policy.*, start_date, end_date, rate_plan.business_id\
                            from rate_plan join cancellation_policy on rate_plan.cancellation_policy_id = cancellation_policy.policy_id \
                            where rate_plan.business_id='"+business_id+"' "))
    packes = json.loads(dbget("select select_id,rate_plan_id, packages.* from package_select\
                            join packages on package_select.packages_id = packages.packages_id \
                            where package_select.business_id='"+business_id+"' "))
    rooms = json.loads(dbget("select select_id, room_type_select.rate_plan_id, configration.room_id, configration.room_name \
                            from room_type_select join \
                            configration on room_type_select.room_id = configration.room_id \
                            where room_type_select.business_id='"+business_id+"' "))
    print(res)
    print(packes)
    print(rooms)
    pack_count, room_count =[],[]
    for i in res:
        print(i)
        print("res",i['rate_plan_id'])
        for pack in packes:
            if pack['rate_plan_id'] == i['rate_plan_id']:
               dict1 = {}
               dict1['packages_id'] = pack['packages_id']
               dict1['package'] = pack['package']
               #dict1['select_id'] = pack['select_id']
               pack_count.append(dict1)
               print("pack",pack['rate_plan_id'])
            i['packages'] = pack_count
        pack_count = []
        for room in rooms:
            if room['rate_plan_id'] == i['rate_plan_id']:
               dict1 = {}
               dict1['room_id'] = room['room_id']
               dict1['room_name'] = room['room_name']
               #dict1['select_id'] = room['select_id']
               room_count.append(dict1)
               print("room",room['rate_plan_id'])
            i['rooms'] = room_count
        room_count = []
        print('final',i)
    print(res,len(res))    
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
    
def select_room_types(request):
    d = request.json
    res = json.loads(dbget("select room_id, room_name from configration where business_id = '"+d['business_id']+"'"))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
    
def select_cancellation_policy(request):
    res = json.loads(dbget("select * from cancellation_policy"))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
 
def Insert_Packages(request):
    d = request.json
    gensql('insert','public.packages',d)
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
def select_packages(request):
    d = request.json
    res = json.loads(dbget("select * from packages where business_id = '"+d['business_id']+"'"))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))
 
 
def select_rateplanid(request):
    business_id = request.json['business_id']
    res = json.loads(dbget("select rate_plan_id, rate_plan from public.rate_plan where business_id='"+business_id+"' "))
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res},indent=2))

def select_plan(request):
    business_id = request.json['business_id']
    rm_id = request.json['room_id']
    st_date =request.json['start_date']
    en_date = request.json['end_date']
    print(business_id,rm_id,st_date,en_date,type(business_id))
    '''
    res = json.loads(dbget("select rate_plan.rate_plan_id, rate_plan.rate_plan from rate_plan join room_type_select \
                            on rate_plan.rate_plan_id  = room_type_select.rate_plan_id \
                            where room_type_select.room_id='5' and rate_plan.business_id='8991897773' \
			    and rate_plan.start_date<= '2018-10-13' and rate_plan.end_date >= '2018-10-22'"))
    '''
    res = json.loads(dbget("select rate_plan.rate_plan_id, rate_plan.rate_plan from rate_plan join room_type_select \
                            on rate_plan.rate_plan_id  = room_type_select.rate_plan_id \
                            where room_type_select.room_id='"+str(rm_id)+"' and rate_plan.business_id='"+str(business_id)+"' \
			    and rate_plan.start_date<= '"+str(st_date)+"' and rate_plan.end_date >= '"+str(en_date)+"'"))
    
    print(res)
    sql = json.loads(dbget("select min_price from configration where room_id='"+str(rm_id)+"'"))
    
    print(res)
    
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Result":res,
                       "minimumprice":sql[0]['min_price']},indent=2))
 
    
    
    
    

    
