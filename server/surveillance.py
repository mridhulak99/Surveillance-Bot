from flask import Flask
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, jsonify
import json
import boto3
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

s3=boto3.resource('s3')
dynamodb=boto3.resource('dynamodb')
rek = boto3.client('rekognition')
@app.route("/")
@cross_origin()
def hello_world():
    return 'Hello from Flask!'
@app.route('/users', methods=['GET','POST'])
@cross_origin()
def users():
    dynamodbTable=dynamodb.Table('makeathon_users')
    response = dynamodbTable.scan()
    item=response
    print(item)
    return (json.dumps(item))
    return (item)
@app.route('/adduser',methods=['POST','GET'])
@cross_origin()
def upload(): 
    file=request.files['image']
    filename=file.filename.split('.')[0]+'_new.'+file.filename.split('.')[-1]
    path=app.config['UPLOAD_FOLDER']+'/'+filename
    print (file.filename,filename,path)
    file.save(path) 
    print ('GET=',file.filename)
    print ('UPLOAD=',filename)
    return jsonify({"path":path})
@app.route('/newpic',methods=['POST','GET'])
@cross_origin()
def newpic():
    img = request.form['dateandtime']
    url = request.form['url']
    print(img)
    print(url)
    dynamodbTable=dynamodb.Table('makeathon_users')
    response = dynamodbTable.scan()
    print(response)
    item=response['Items']
    print(item)
    for i in range(response['Count']):
        print(item[i]['name'])
    for i in range(response['Count']):
        p=0
        try:
            res = rek.compare_faces(
    	    SourceImage={
	        'S3Object': {
		    'Bucket': 'makeathonpis',
		    'Name':"images/"+ img+".jpg",
			    },
			},
	    TargetImage={
		'S3Object': {
		    'Bucket': 'makeathonusers',
		    'Name': item[i]['name']+".jpg",
			    },
		        },
		)
            print(res)
            p=1
        except Exception:
            p=0
            res="0"

        c=0
        try:
            s1 = json.dumps(res)
            d2 = json.loads(s1)
            print(d2)
            print(d2['FaceMatches'][0]['Similarity'])
            if (res['FaceMatches'][0]['Similarity']>90):
                c=1   
                dynamodbTable=dynamodb.Table('makeathon_history')
                try:
                    dynamodbTable.put_item(
		    Item={
		    'dateandtime': img,
		    'url':url,
		    'name':item[i]['name'],
		    'status': 'known'
		    }
		    )
                    break
                except Exception :
                    print ("error")
        except Exception:
            print("error")
        if (p==0):
            dynamodbTable=dynamodb.Table('makeathon_history')
            try:
                dynamodbTable.put_item(
		Item={
		'dateandtime': img,
		'url':url,
		'name':'no person',
		'status': 'no person'
		}
		)
            except Exception :
                print ("error")
            return"no preson"

        if (c==0):			
            dynamodbTable=dynamodb.Table('makeathon_history')
            try:
                dynamodbTable.put_item(
		Item={
		'dateandtime': img,
		'url':url,
		'name':'unknown',
		'status': 'stranger'
		}
		)
            except Exception :
                print ("error")
    return"hi"
@app.route('/history', methods=['GET','POST'])
@cross_origin()
def his():
    dynamodbTable=dynamodb.Table('makeathon_history')
    response = dynamodbTable.scan()
    item=response
    print(item)
    return (json.dumps(item))
    return (item)
@app.route('/livetrack', methods=['GET','POST'])
@cross_origin()
def livetrack():
    dynamodbTable=dynamodb.Table('makeathon_history')
    response = dynamodbTable.scan()
    item=response
    print(item)
    return (json.dumps(item))
    return (item)
@app.route('/front', methods=['POST','GET'])
@cross_origin()
def front():
    print(request.data)
    table=dynamodb.Table('makeathon_control')
    v = request.form['a']
    table.update_item(
    Key={
        'val': '1'
    },
    UpdateExpression="set dir = :r",
    ExpressionAttributeValues={
        ':r': v,
    },
    ReturnValues="UPDATED_NEW"
    )
    return"done"
@app.route('/back', methods=['POST','GET'])
@cross_origin()
def back():
    print(request.data)
    table=dynamodb.Table('makeathon_control')
    v = request.form['a']
    table.update_item(
    Key={
        'val': '1'
    },
    UpdateExpression="set dir = :r",
    ExpressionAttributeValues={
        ':r': v,
    },
    ReturnValues="UPDATED_NEW"
    )
    return"done"	
@app.route('/left', methods=['POST','GET'])
@cross_origin()
def left():
    print(request.data)
    table=dynamodb.Table('makeathon_control')
    v = request.form['a']
    table.update_item(
    Key={
        'val': '1'
    },
    UpdateExpression="set dir = :r",
    ExpressionAttributeValues={
        ':r': v,
    },
    ReturnValues="UPDATED_NEW"
    )
    return"done"	
@app.route('/right', methods=['POST','GET'])
@cross_origin()
def right():
    print(request.data)
    table=dynamodb.Table('makeathon_control')
    v = request.form['a']
    table.update_item(
    Key={
        'val': '1'
    },
    UpdateExpression="set dir = :r",
    ExpressionAttributeValues={
        ':r': v,
    },
    ReturnValues="UPDATED_NEW"
    )
    return"done"
@app.route('/stop', methods=['POST','GET'])
@cross_origin()
def stop():
    print(request.data)
    table=dynamodb.Table('makeathon_control')
    v = request.form['a']
    table.update_item(
    Key={
        'val': '1'
    },
    UpdateExpression="set dir = :r",
    ExpressionAttributeValues={
        ':r': v,
    },
    ReturnValues="UPDATED_NEW"
    )
    return"done"

if __name__ == '__main__':
    app.debug=True
    app.run(host = '0.0.0.0',port=5000,threaded=True)
