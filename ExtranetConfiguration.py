from sqlwrapper import gensql,dbget,dbput
import json
import datetime

def RoomsizeConfiguration(request):
    d = request.json
    gensql('insert','room_size',d)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Inserted Successfully','ReturnCode':'RIS'}, sort_keys=True, indent=4))
    
def BeddingoptionsConfiguration(request):
    d = request.json
    gensql('insert','bedding_options',d)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Inserted Successfully','ReturnCode':'RIS'}, sort_keys=True, indent=4))
    
def BedsizeConfiguration(request):
    d = request.json
    gensql('insert','bed_size',d)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Inserted Successfully','ReturnCode':'RIS'}, sort_keys=True, indent=4))
    
def RoomamenitieConfiguration(request):
    d = request.json
    gensql('insert','room_amenitie',d)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Inserted Successfully','ReturnCode':'RIS'}, sort_keys=True, indent=4))
    
def InclusionsConfiguration(request):
    d = request.json
    gensql('insert','inclusions',d)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Inserted Successfully','ReturnCode':'RIS'}, sort_keys=True, indent=4))

def ExtrabedConfiguration(request):
    d = request.json
    gensql('insert','max_extra_bed',d)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Inserted Successfully','ReturnCode':'RIS'}, sort_keys=True, indent=4))
    
   
def DeleteRoomsizeConfiguration(request):
    
    size_id = request.json['room_size_id']
    sql = dbput("DELETE FROM public.room_size WHERE  room_size_id = '"+size_id+"'")
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Deleted Successfully','ReturnCode':'RDS'}, sort_keys=True, indent=4))
    
def DeleteBeddingoptionsConfiguration(request):
    
    bedding_option_id = request.json['bedding_option_id']
    sql = dbput("DELETE FROM public.bedding_options WHERE  bedding_option_id = '"+bedding_option_id+"'")
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Deleted Successfully','ReturnCode':'RDS'}, sort_keys=True, indent=4))
    
def DeleteBedSizeConfiguration(request):
    
    bed_size_id = request.json['bed_size_id']
    sql = dbput("DELETE FROM public.bed_size WHERE  bed_size_id = '"+bed_size_id+"'")
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Deleted Successfully','ReturnCode':'RDS'}, sort_keys=True, indent=4))
    
def DeleteInclusionsConfiguration(request):
    
    inclusion_id = request.json['inclusion_id']
    sql = dbput("DELETE FROM public.inclusions WHERE  inclusion_id = '"+inclusion_id+"'")
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Deleted Successfully','ReturnCode':'RDS'}, sort_keys=True, indent=4))
    
def DeleteRoomamenitieConfiguration(request):
    
    amenitie_id = request.json['amenitie_id']
    sql = dbput("DELETE FROM public.room_amenitie WHERE  amenitie_id = '"+amenitie_id+"'")
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Deleted Successfully','ReturnCode':'RDS'}, sort_keys=True, indent=4))
   
def RoomnameConfiguration(request):
    d = json.loads(dbget("select room_name from configration"))
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnCode':'RRS','Result':d}, sort_keys=True, indent=4))
 
 
def SelectRoomsizeConfiguration(request):
    d = request.json
    sql = json.loads(dbget("select * from room_size where business_id = '"+d['business_id']+"'"))
    print(sql)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnCode':'RTS','Result':sql}, sort_keys=True, indent=4))
def SelectBeddingoptionsConfiguration(request):
    d = request.json
    sql = json.loads(dbget("select * from bedding_options where business_id = '"+d['business_id']+"'"))
    print(sql)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnCode':'RTS','Result':sql}, sort_keys=True, indent=4))
 
def SelectBedsizeConfiguration(request):
    d = request.json
    sql = json.loads(dbget("select * from bed_size where business_id = '"+d['business_id']+"'"))
    print(sql)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnCode':'RTS','Result':sql}, sort_keys=True, indent=4))
 
def SelectRoomamenitieConfiguration(request):
    d = request.json
    sql = json.loads(dbget("select * from room_amenitie where business_id = '"+d['business_id']+"'"))
    print(sql)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnCode':'RTS','Result':sql}, sort_keys=True, indent=4))
def SelectInclusionsConfiguration():
    sql = json.loads(dbget("select * from inclusions"))
    print(sql)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnCode':'RTS','Result':sql}, sort_keys=True, indent=4))
def SelectExtrabed(request):
    d = request.json
    sql = json.loads(dbget("select * from max_extra_bed where business_id = '"+d['business_id']+"'"))
    print(sql)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnCode':'RTS','Result':sql}, sort_keys=True, indent=4))
