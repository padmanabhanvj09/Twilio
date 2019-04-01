from sqlwrapper import dbget,dbput,gensql
import json


def config(request):
    
    res = request.json
    roomtype = request.json['room_name']
    res['room_name'] = roomtype.title()
    rooms = json.loads(dbget("select count(*) from configration where room_name='"+res['room_name']+"'"))
    if rooms[0]['count'] == 0:
       print(res)
       gensql('insert','configration',res)
       return(json.dumps({"Return":"Record Inserted Successfully","ReturnCode":"RIS","ReturnMessage":"Success"},indent=2))
    else:
       return(json.dumps({"Return":"Room Name Already Exist","ReturnCode":"RNAE","ReturnMessage":"Success"},indent=2))
def select_config(request):
    d = request.json
    res = json.loads(dbget("select room_id, room_name, max_adults, max_child, room_size.*, bedding_options.* ,max_extra_bed.*,\
                            bed_size.*, upload_photos, room_amenitie.*, smoking, rate_plan_id, advance_booking_window,\
                            prepayment_policy, cancellation_policy, inclusions.*, important_information,min_price \
                            from configration \
                            join room_size on configration.room_size_id = room_size.room_size_id\
                            join bedding_options on configration.bedding_options_id = bedding_options.bedding_option_id\
                            join max_extra_bed on configration.maximum_extrabed_id = max_extra_bed.extrabed_id\
                            join bed_size on configration.bed_size_id = bed_size.bed_size_id\
                            left join inclusions on configration.inculsions_id = inclusions.inclusion_id\
                            join room_amenitie on configration.room_amenities_id = room_amenitie.amenitie_id \
                            where configration.business_id='"+d['business_id']+"' "))
    for i in res:
        a = i['amenitie'].split('|')
        del i['amenitie']
        i['amenitie'] = a
    print("res",res)  
    return(json.dumps({"Result":res,"ReturnCode":"RRS","ReturnMessage":"Success"},indent=2))

def update_config(request):
    res = request.json
    a = { k : v for k,v in res.items()  if k not in ('room_id','business_id')}
    e = { k : v for k,v in res.items()  if k  in ('room_id','business_id')}
    gensql('update','configration',a,e)
    return(json.dumps({"ReturnCode":"RUS","ReturnMessage":"Success"},indent=2))
