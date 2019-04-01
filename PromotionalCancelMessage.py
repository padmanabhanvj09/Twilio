from sqlwrapper import dbget,dbput,gensql
import json
import datetime
def promotionalcancelmessage(request):
    try:
        tfn = request.json['TFN']
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id[0]['id'])
        message = json.loads(dbget("select ivr_promotional_message from ivr_promotional_cancellation_message join \
                                    ivr_hotel_list on ivr_hotel_list.id = ivr_promotional_cancellation_message.id \
                                    where ivr_promotional_cancellation_message.id='"+str(b_id[0]['id'])+"' "))
        message = message[0]['ivr_promotional_message']
        print(message)
        a = {"ServiceStatus":"Success","ServiceMessage":"Success","message":message}
        return(json.dumps(a))
    except:
        a = {"ServiceStatus":"Success","ServiceMessage":"Success"}
        return(json.dumps(a))

def insertcancelmessage(request):
    #e = request.json
    bus_id = request.json['business_id']
    message = request.json['cancel_message']
    b_id = json.loads(dbget("select id from ivr_hotel_list where business_id='"+bus_id+"' "))
    print(b_id[0]['id'])
    count = json.loads(dbget("select count(*) from ivr_promotional_cancellation_message where \
                              id='"+str(b_id[0]['id'])+"' "))
    print(count)
    e = {}
    e['ivr_promotional_message'] = message
    e['id'] = b_id[0]['id']
    if count[0]['count'] != 1:
        print(gensql('insert','ivr_promotional_cancellation_message',e))
    else:
        print(dbput("update ivr_promotional_cancellation_message set ivr_promotional_message \
                    ='"+message+"' where id='"+str(b_id[0]['id'])+"' "))
    a = {"ServiceStatus":"Success","ServiceMessage":"Success"}
    return(json.dumps(a))
   
