from sqlwrapper import gensql,dbget,dbput
from botocore.client import Config
import boto3
import json
import requests


def upload_file(request):
   print(type(request.files))
   name1 = str(request.form['name'])
   print("FORM DATAAAA",name1,type(name1))
   list1 = name1.split('|')
   print(list1,type(list1))
   #print("FORM DATAAAA",name1,type(name1))
   image = request.files['Image']
   name = image.filename
   bucket = 'image-upload-rekognition'
   key = name
   print(name)
   client = boto3.client('s3')
   s3 = boto3.resource('s3',region_name='us-east-1',aws_access_key_id=list1[0],aws_secret_access_key=list1[1])

   s3.Bucket(bucket).put_object(Key=key,Body=request.files['Image'])
   
   url = 'https://s3.amazonaws.com/'+bucket+'/'+key
   
   return (json.dumps({"Status":"Image Uploaded in S3 Bucket","url":url}))


def get_aws_keys(request):

    tb_id = {"tb_id":1}

    res = json.loads(gensql('select','aws_keys','*',tb_id))
    
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success",
                      "Status_Code": "200","Returnvalue":res },indent=2))
    
