# -*- coding: utf-8 -*-
import pathlib
import json
import requests
#import datetime
import requests.packages.urllib3
import psycopg2
from datetime import datetime
from datetime import timedelta

requests.packages.urllib3.disable_warnings()

fhir = 'http://192.168.211.9:8080/fhir/'#4600VM

headers = {    
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Basic ZmhpcnVzZXI6Y2hhbmdlLXBhc3N3b3Jk'
}
payload={}

#postgresip = "20.205.134.146"
postgresip = "104.208.68.39"
port="8081"
def postlog(request):
    ip_addr = request.remote_addr
    method = request.method
    host_url  = request.url
    headers=dict(request.headers)
    conn = psycopg2.connect(database="consent", user="postgres", password="1qaz@WSX3edc", host=postgresip, port=port)
    #print('Opened database')
    cur = conn.cursor()
    #sql="INSERT INTO public.log (ip_addr, method, host_url, headers, datetime ) VALUES ( '123.123.123.123', 'GET', 'http://1', 'header', '2023-10-11 08:12:22');"
    sql="INSERT INTO public.log (ip_addr, method, host_url, headers, datetime ) VALUES ('" + ip_addr + "', '" + \
            method + "', '" + host_url + "', '" + json.dumps(headers) + "', '" + (datetime.now()+timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S") + "');"
    #print(sql)
    cur.execute(sql)
    conn.commit()

    cur.execute('SELECT * FROM public.log')
    rows = cur.fetchall()
    #for row in rows:
        #print(row)
    conn.close()
    #print('Close database')
    return rows
def PatientCURD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Patient病人資料.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)

    DiagnosticReportNursingjsonurl = fhir+'Patient?'
   
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    DiagnosticReportNursingjson['id']=resourceTypeid
    
    patient=request.POST['patient']
    
    DiagnosticReportNursingjson['identifier'][0]['value']=patient
    patient1=request.POST['patient1']
    DiagnosticReportNursingjson['identifier'][1]['value']=patient1
    
    code=request.POST['code']
    DiagnosticReportNursingjson['extension'][0]['extension'][0]['valueCodeableConcept']['coding'][0]['code']=code
    start=request.POST['start']
    DiagnosticReportNursingjson['extension'][0]['extension'][1]['valuePeriod']['start']=start
    
    family=request.POST['family']
    DiagnosticReportNursingjson['name'][0]['family']=family
    given=request.POST['given']
    DiagnosticReportNursingjson['name'][0]['given']=given
    telecom=request.POST['telecom']
    DiagnosticReportNursingjson['telecom'][2]['value']=telecom
    home=request.POST['home']
    DiagnosticReportNursingjson['telecom'][0]['value']=home
    company=request.POST['company']
    DiagnosticReportNursingjson['telecom'][1]['value']=company
    other=request.POST['other']
    DiagnosticReportNursingjson['telecom'][3]['value']=other
    email=request.POST['email']
    DiagnosticReportNursingjson['telecom'][4]['value']=email
    gender=request.POST['gender']
    DiagnosticReportNursingjson['gender']=gender
    birthDate=request.POST['birthDate']
    DiagnosticReportNursingjson['birthDate']=birthDate
    managingOrganization=request.POST['managingOrganization']
    DiagnosticReportNursingjson['managingOrganization']='Organization/'+managingOrganization
    deceasedBoolean=request.POST['deceasedBoolean']
    DiagnosticReportNursingjson['deceasedBoolean']=deceasedBoolean
    
    addresstext=request.POST['addresstext']
    DiagnosticReportNursingjson['address'][0]['text']=addresstext
    country=request.POST['country']
    DiagnosticReportNursingjson['address'][0]['city']=country
    postalCode=request.POST['postalCode']
    DiagnosticReportNursingjson['address'][0]['postalCode']=postalCode
    addressline=request.POST['addressline']
    DiagnosticReportNursingjson['address'][0]['line'][0]=addressline
    
    communication=request.POST['communication']
    DiagnosticReportNursingjson['communication'][0]['language']['text']=communication
    
    addresstext1=request.POST['addresstext1']
    DiagnosticReportNursingjson['address'][1]['text']=addresstext1
    country1=request.POST['country1']
    DiagnosticReportNursingjson['address'][1]['city']=country1
    postalCode1=request.POST['postalCode1']
    DiagnosticReportNursingjson['address'][1]['postalCode']=postalCode1
    addressline1=request.POST['addressline1']
    DiagnosticReportNursingjson['address'][1]['line'][0]=addressline1
    
    communication1=request.POST['communication1']
    DiagnosticReportNursingjson['communication'][1]['language']['text']=communication1
    
    addresstext2=request.POST['addresstext2']
    DiagnosticReportNursingjson['address'][2]['text']=addresstext2
    country2=request.POST['country2']    
    DiagnosticReportNursingjson['address'][2]['city']=country2
    postalCode2=request.POST['postalCode2']
    DiagnosticReportNursingjson['address'][2]['postalCode']=postalCode2
    addressline2=request.POST['addressline2']
    DiagnosticReportNursingjson['address'][2]['line'][0]=addressline2
   
    cfamily=request.POST['cfamily']
    DiagnosticReportNursingjson['contact'][0]['name']['family']=cfamily
    cgiven=request.POST['cgiven']
    DiagnosticReportNursingjson['contact'][0]['name']['given'][0]=cgiven
    ctelecom=request.POST['ctelecom']
    DiagnosticReportNursingjson['contact'][0]['telecom']=ctelecom
    caddresstext=request.POST['caddresstext']
    DiagnosticReportNursingjson['contact'][0]['address']['text']=caddresstext
    ccountry=request.POST['ccountry']
    DiagnosticReportNursingjson['contact'][0]['address']['city']=ccountry
    cpostalCode=request.POST['cpostalCode']
    DiagnosticReportNursingjson['contact'][0]['address']['postalCode']=cpostalCode
    caddressline=request.POST['caddressline']
    DiagnosticReportNursingjson['contact'][0]['address']['line'][0]=caddressline
        
    #print(DiagnosticReportNursingjson)
    payload = json.dumps(DiagnosticReportNursingjson)
    
    if method=='GET':
        if resourceTypeid!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_id='+resourceTypeid+'&'
        if patient!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'identifier='+patient+'&'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads(response.text)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(response.status_code)
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Patient/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Patient/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def OrganizationCURD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Organization組織資料.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    
    DiagnosticReportNursingjsonurl = fhir+'Organization?'
   
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    if resourceTypeid!='':        
        DiagnosticReportNursingjson['id']=resourceTypeid
    resourceIdentifier=request.POST['identifier']
    if resourceIdentifier!='':
        DiagnosticReportNursingjson['identifier'][0]['value']=resourceIdentifier    
    name=request.POST['name']
    if name!='':        
        DiagnosticReportNursingjson['name']=name

    ListTelecom=[]
    telecom=request.POST['telecom']
    if telecom!='':
        Dict={ "system": "phone", "value": telecom }
        ListTelecom.append(Dict)
    fax=request.POST['fax']
    if fax!='':        
        Dict={ "system": "fax", "value": fax }
        ListTelecom.append(Dict)
    email=request.POST['email']
    if email!='':
        Dict={ "system": "email", "value": email }
        ListTelecom.append(Dict)
    if ListTelecom!=[]:
        DiagnosticReportNursingjson['telecom']=ListTelecom
    #print(1)
    Dict={}
    city=request.POST['city']
    if city!='': 
        Dict["city"]= city
    postalCode=request.POST['postalCode']
    if postalCode!='': 
        Dict["postalCode"] = postalCode         

    addressline=request.POST['addressline']
    if addressline!='':
        List=[]
        List.append( addressline )
        Dict["line"] = List 
    #print(Dict)
    if Dict!={}:
        List=[]
        List.append(Dict)
        DiagnosticReportNursingjson['address']=List
    
    #print(DiagnosticReportNursingjson)
    payload = json.dumps(DiagnosticReportNursingjson)
    
    if method=='GET':
        if resourceTypeid!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_id='+resourceTypeid+'&'
        DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_count=100'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(response.status_code)
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Organization/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Organization/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def PractitionerCURD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Practitioner醫師.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    
    DiagnosticReportNursingjsonurl = fhir+'Practitioner?'
   
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    if resourceTypeid!='':        
        DiagnosticReportNursingjson['id']=resourceTypeid
    resourceIdentifier=request.POST['identifier']
    if resourceIdentifier!='':
        DiagnosticReportNursingjson['identifier'][0]['value']=resourceIdentifier    
    name=request.POST['name']
    if name!='':        
        DiagnosticReportNursingjson['name']=name

    ListTelecom=[]
    telecom=request.POST['telecom']
    if telecom!='':
        Dict={ "system": "phone", "value": telecom }
        ListTelecom.append(Dict)
    fax=request.POST['fax']
    if fax!='':        
        Dict={ "system": "fax", "value": fax }
        ListTelecom.append(Dict)
    email=request.POST['email']
    if email!='':
        Dict={ "system": "email", "value": email }
        ListTelecom.append(Dict)
    if ListTelecom!=[]:
        DiagnosticReportNursingjson['telecom']=ListTelecom
    #print(1)
    Dict={}
    city=request.POST['city']
    if city!='': 
        Dict["city"]= city
    postalCode=request.POST['postalCode']
    if postalCode!='': 
        Dict["postalCode"] = postalCode         

    addressline=request.POST['addressline']
    if addressline!='':
        List=[]
        List.append( addressline )
        Dict["line"] = List 
    #print(Dict)
    if Dict!={}:
        List=[]
        List.append(Dict)
        DiagnosticReportNursingjson['address']=List
    
    #print(DiagnosticReportNursingjson)
    payload = json.dumps(DiagnosticReportNursingjson)
    
    if method=='GET':
        if resourceTypeid!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_id='+resourceTypeid+'&'
        DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_count=100'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(response.status_code)
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Practitioner/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Practitioner/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')
    
def patient_medical_recordsCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Composition_patient_medical_records.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    
    DiagnosticReportNursingjsonurl = fhir+'Composition?'
   
    #fhirip=request.POST['fhirip']
    #if fhirip!='':        
    #    print(fhirip)
    #url = fhirip+'Organization?'
    method=request.POST['method']
    #response = requests.request(method, url, headers=headers, data=payload, verify=False)    
    #print(response.text)
    resourceTypeid=request.POST['id']
    if resourceTypeid!='':        
        DiagnosticReportNursingjson['id']=resourceTypeid
    #resourceIdentifier=request.POST['identifier']
    #if resourceIdentifier!='':
    #    DiagnosticReportNursingjson['identifier'][0]['value']=resourceIdentifier    
    #print(method,DiagnosticReportNursingjsonurl,headers)
    if method=='GET':
        if resourceTypeid!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_id='+resourceTypeid+'&'
        DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_count=100'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(response.status_code)
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Composition/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Composition/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def DischargeSummaryCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Composition_DischargeSummary135726.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    
    fhirip=request.POST['fhirip']
    if fhirip!='':        
        DiagnosticReportNursingjsonurl = fhirip +'Composition?'
    else:
        DiagnosticReportNursingjsonurl = fhir +'Composition?'

    method=request.POST['method']
    #response = requests.request(method, url, headers=headers, data=payload, verify=False)    
    #print(response.text)
    resourceTypeid=request.POST['id']
    if resourceTypeid!='':        
        DiagnosticReportNursingjson['id']=resourceTypeid
    #resourceIdentifier=request.POST['identifier']
    #if resourceIdentifier!='':
    #    DiagnosticReportNursingjson['identifier'][0]['value']=resourceIdentifier    
    #print(method,DiagnosticReportNursingjsonurl,headers)
    if method=='GET':
        if resourceTypeid!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_id='+resourceTypeid+'&'
        Patientname=request.POST['name']
        if Patientname!='':        
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'subject:Patient.name='+Patientname+'&'
        DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'title=出院&_count=200'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('查詢完畢',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(response.status_code)
        return ('新增完畢',resultjson)
    elif method=='PUT':
        if fhirip!='':        
            PUTurl = fhirip + "Composition/" + str(resourceTypeid)
        else:
            PUTurl = fhir + "Composition/" + str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('修改完畢',resultjson)
    elif method=='DELETE':
        if fhirip!='':        
            DELETEurl = fhirip + "Composition/" + str(resourceTypeid)
        else:
            DELETEurl = fhir + "Composition/" + str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        #print(method,DiagnosticReportNursingjsonurl,headers,payload)
        resultjson=json.loads(response.text)        
        return ('刪除完畢',resultjson['issue'][0])

def VisitNoteCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Composition_DischargeSummary135726.json"
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    fhirip=request.POST['fhirip']
    if fhirip!='':        
        DiagnosticReportNursingjsonurl = fhirip +'Composition?'
    else:
        DiagnosticReportNursingjsonurl = fhir +'Composition?'
    method=request.POST['method']

    resourceTypeid=request.POST['id']
    #print(resourceTypeid)
    if resourceTypeid!='':        
        DiagnosticReportNursingjson['id']=resourceTypeid
        
    #?subject:Patient.name=Sarah
    if method=='GET':
        if resourceTypeid!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'_id='+resourceTypeid+'&'
        Patientname=request.POST['name']
        if Patientname!='':        
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'subject:Patient.name='+Patientname+'&'
        pid=request.POST['pid']
        if pid!='':        
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'patient='+pid+'&'
        DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'title=門診&_count=200'
        #print(DiagnosticReportNursingjsonurl)
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        return ('查詢完畢',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('新增完畢',resultjson)
    elif method=='PUT':
        if fhirip!='':        
            PUTurl = fhirip + "Composition/" + str(resourceTypeid)
        else:
            PUTurl = fhir + "Composition/" + str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('修改完畢',resultjson)
    elif method=='DELETE':
        if fhirip!='':        
            DELETEurl = fhirip + "Composition/" + str(resourceTypeid)
        else:
            DELETEurl = fhir + "Composition/" + str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('刪除完畢',resultjson['issue'][0])

def ConsentCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Composition_DischargeSummary135726.json"
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    fhirip=request.POST['fhirip']
    if fhirip!='':        
        DiagnosticReportNursingjsonurl = fhirip +'Consent?_count=200'
    else:
        DiagnosticReportNursingjsonurl = fhir +'Consent?_count=200'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    #print(resourceTypeid)
    if resourceTypeid!='':        
        DiagnosticReportNursingjson['id']=resourceTypeid
        
    #?subject:Patient.name=Sarah
    if method=='GET':
        if resourceTypeid!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'&_id='+resourceTypeid+'&'
        DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl
        #print(DiagnosticReportNursingjsonurl)
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        return ('查詢完畢',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('新增完畢',resultjson)
    elif method=='PUT':
        if fhirip!='':        
            PUTurl = fhirip + "Composition/" + str(resourceTypeid)
        else:
            PUTurl = fhir + "Composition/" + str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('修改完畢',resultjson)
    elif method=='DELETE':
        if fhirip!='':        
            DELETEurl = fhirip + "Composition/" + str(resourceTypeid)
        else:
            DELETEurl = fhir + "Composition/" + str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('刪除完畢',resultjson['issue'][0])
    
def PatientUpload(df,method):
    #print(df)
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Patient病人資料.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    payload={}

    DiagnosticReportNursingjsonurl = fhir+'Patient?'
       
    #method=request.POST['method']
    #method='GET'
    resourceTypeid=df['病歷號'][0]
    DiagnosticReportNursingjson['id']=resourceTypeid
    patient=df['病歷號'][0]
    DiagnosticReportNursingjson['identifier'][0]['value']=df['病歷號']
    DiagnosticReportNursingjson['identifier'][1]['value']=df['身分證ID']
    
    DiagnosticReportNursingjson['extension'][0]['extension'][0]['valueCodeableConcept']['coding'][0]['code']=df['國籍']
    #print(df['生日'])
    DiagnosticReportNursingjson['extension'][0]['extension'][1]['valuePeriod']['start']=df['生日']
    DiagnosticReportNursingjson['name'][0]['family']=df['姓名'][0]
    DiagnosticReportNursingjson['name'][0]['given']=df['姓名'][1:]
    
    DiagnosticReportNursingjson['telecom'][2]['value']=df['電話(M)']
    DiagnosticReportNursingjson['telecom'][0]['value']=df['電話(H)']
    DiagnosticReportNursingjson['telecom'][1]['value']=df['電話(O)']
    
    DiagnosticReportNursingjson['telecom'][3]['value']=df['電話2']
    DiagnosticReportNursingjson['telecom'][4]['value']=df['Email']
    #print('ok2')
    DiagnosticReportNursingjson['gender']=df['性別']
    DiagnosticReportNursingjson['birthDate']=df['生日']

    DiagnosticReportNursingjson['address'][0]['text']=df['戶籍地址']
    DiagnosticReportNursingjson['address'][1]['text']=df['聯絡地址']
    DiagnosticReportNursingjson['address'][2]['text']=df['聯絡地址2']
    #print(DiagnosticReportNursingjson)
    payload = json.dumps(DiagnosticReportNursingjson)
    #print(method)
    if method=='GET':
        if patient!='':
           DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'identifier='+patient+'&'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        #resultjson=json.loads('{"entry":[{"resource":'+payload+'}]}')
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(response.status_code)
        try:
            #print(resultjson['entry'][0]['resource']['issue'][0]['diagnostics'])
            diagnostics=resultjson['entry'][0]['resource']['issue'][0]['diagnostics']
        except:
            diagnostics=''
        return ('POST OK',resultjson,response.status_code,diagnostics)
    elif method=='PUT':
        PUTurl = fhir+"Patient/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(response.status_code)
        try:
            #print(resultjson['entry'][0]['resource']['issue'][0]['diagnostics'])
            diagnostics=resultjson['entry'][0]['resource']['issue'][0]['diagnostics']
        except:
            diagnostics=''
        return ('PUT OK',resultjson,response.status_code,diagnostics)
    elif method=='DELETE':
        DELETEurl = fhir+"Patient/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def PhenopacketCURD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/doc/BR20003-1.json"
    #print(jsonPath)
    Phenopacketjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Phenopacketjson)
    method=request.POST['method']
    resourceTypeid = request.POST['id']
    resultjson=Phenopacketjson
    #print(resultjson)
    if method=='GET':
        return ('GET OK',resultjson)
    elif method=='POST':
        return ('POST OK')
    elif method=='PUT':
        return ('PUT OK')
    elif method=='DELETE':
        return ('DELETE OK')
    else:
        return ('method NG')

def BiosampleCURD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/doc/BR20003-1.json"
    #print(jsonPath)
    Phenopacketjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Phenopacketjson)
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    resultjson=Phenopacketjson
    if method=='GET':
        return ('GET OK',resultjson)
    elif method=='POST':
        return ('POST OK')
    elif method=='PUT':
        return ('PUT OK')
    elif method=='DELETE':
        return ('DELETE OK')
    else:
        return ('method NG')
    
def IndividualCURD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/doc/BR20003-1.json"
    #print(jsonPath)
    Phenopacketjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Phenopacketjson)
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    resultjson=Phenopacketjson
    if method=='GET':
        return ('GET OK',resultjson)
    elif method=='POST':
        return ('POST OK')
    elif method=='PUT':
        return ('PUT OK')
    elif method=='DELETE':
        return ('DELETE OK')
    else:
        return ('method NG')

def ClinvarVariantCURD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/doc/BR20003-1.json"
    #print(jsonPath)
    Phenopacketjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Phenopacketjson)
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    resultjson=Phenopacketjson
    if method=='GET':
        return ('GET OK',resultjson)
    elif method=='POST':
        return ('POST OK')
    elif method=='PUT':
        return ('PUT OK')
    elif method=='DELETE':
        return ('DELETE OK')
    else:
        return ('method NG')

def InterpretationCURD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/doc/BR20003-1.json"
    #print(jsonPath)
    Phenopacketjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Phenopacketjson)
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    resultjson=Phenopacketjson
    if method=='GET':
        return ('GET OK',resultjson)
    elif method=='POST':
        return ('POST OK')
    elif method=='PUT':
        return ('PUT OK')
    elif method=='DELETE':
        return ('DELETE OK')
    else:
        return ('method NG')

def AllergyIntoleranceCRUD(request):
    AllergyPath=str(pathlib.Path().absolute()) + "/static/template/AllergyIntolerance過敏資料.json"
    Allergyjson = json.load(open(AllergyPath,encoding="utf-8"))
    #print(Allergyjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Allergyurl = fhir+'AllergyIntolerance?'
    method=request.POST['method']
    AllergyIntolerance=request.POST['AllergyIntolerance']
    Allergyjson['id']=AllergyIntolerance
    patient=request.POST['patient']
    Allergyjson['patient']['reference']='Patient/'+patient
    snomed=request.POST['snomed']
    Allergyjson['code']['coding'][0]['code']=snomed
    display=request.POST['display']
    Allergyjson['code']['coding'][0]['display']=display
    text=request.POST['text']
    Allergyjson['code']['text']=text
    #print(Allergyjson)
    payload = json.dumps(Allergyjson)
    
    if method=='GET':
        if patient!='':
            Allergyurl=Allergyurl+'patient='+patient+'&'
        if snomed!='':
            Allergyurl=Allergyurl+'code='+snomed+'&'
        response = requests.request(method, Allergyurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Allergyurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(resstr)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"AllergyIntolerance/"+str(AllergyIntolerance)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"AllergyIntolerance/"+str(AllergyIntolerance)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def FamilyMemberHistoryCRUD(request):
    FamilyMemberHistoryPath=str(pathlib.Path().absolute()) + "/static/template/FamilyMemberHistory家族病史.json"
    Familyjson = json.load(open(FamilyMemberHistoryPath,encoding="utf-8"))
    #print(Allergyjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Familyurl = fhir+'FamilyMemberHistory?'
    method=request.POST['method']
    FamilyMemberHistory=request.POST['FamilyMemberHistory']
    Familyjson['id']=FamilyMemberHistory
    patient=request.POST['patient']
    Familyjson['patient']['reference']='Patient/'+patient
    relationshipcode=request.POST['relationshipcode']
    Familyjson['relationship']['coding'][0]['code']=relationshipcode
    relationshipdisplay=request.POST['relationshipdisplay']
    Familyjson['relationship']['coding'][0]['display']=relationshipdisplay
    gender=request.POST['gender']
    Familyjson['sex']['coding'][0]['code']=gender
    snomed=request.POST['snomed']
    Familyjson['condition'][0]['code']['coding'][0]['code']=snomed
    display=request.POST['display']
    Familyjson['condition'][0]['code']['coding'][0]['display']=display
    text=request.POST['text']
    Familyjson['condition'][0]['code']['text']=text
    #print(Familyjson)
    payload = json.dumps(Familyjson)
    
    if method=='GET':
        if patient!='':
            Familyurl=Familyurl+'patient='+patient+'&'
        if relationshipcode!='':
            Familyurl=Familyurl+'relationship='+relationshipcode+'&'
        if gender!='':
            Familyurl=Familyurl+'sex='+gender+'&'
        if snomed!='':
            Familyurl=Familyurl+'code='+snomed+'&'
        response = requests.request(method, Familyurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Familyurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(resstr)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"/FamilyMemberHistory/"+str(FamilyMemberHistory)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"/FamilyMemberHistory/"+str(FamilyMemberHistory)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def EncounterCRUD(request):
    EncounterPath=str(pathlib.Path().absolute()) + "/static/template/Encounter住院.json"
    #print(EncounterPath)
    Encounterjson = json.load(open(EncounterPath,encoding="utf-8"))
    #print(Encounterjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Encounterurl = fhir+'Encounter?'
    method=request.POST['method']
    Encounter=request.POST['Encounter']
    Encounterjson['id']=Encounter
    patient=request.POST['patient']
    Encounterjson['subject']['reference']='Patient/'+patient
    location=request.POST['location']
    Encounterjson['location'][0]['location']['display']=location
    start=request.POST['start']
    if start!='':
        start=start+':00'
    Encounterjson['location'][0]['period']['start']=start
    end=request.POST['end']
    if end!='':
        end=end+':00'
    Encounterjson['location'][0]['period']['end']=end
    #print(Encounterjson)
    payload = json.dumps(Encounterjson)
    
    if method=='GET':
        if patient!='':
            Encounterurl=Encounterurl+'patient='+patient+'&'
        response = requests.request(method, Encounterurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Encounterurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Encounter/"+str(Encounter)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Encounter/"+str(Encounter)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')
    
def ProcedureCRUD(request):
    ProcedurePath=str(pathlib.Path().absolute()) + "/static/template/Procedure手術.json"
    #print(ProcedurePath)
    Procedurejson = json.load(open(ProcedurePath,encoding="utf-8"))
    #print(Procedurejson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Procedureurl = fhir+'Procedure?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    Procedurejson['id']=resourceTypeid
    patient=request.POST['patient']
    Procedurejson['subject']['reference']='Patient/'+patient
    encounter=request.POST['encounter']
    Procedurejson['encounter']['reference']='Encounter/'+encounter
    report=request.POST['report']
    Procedurejson['report'][0]['reference']='DiagnosticReport/'+report
    
    reasonCode=request.POST['reasonCode']
    Procedurejson['reasonCode'][0]['coding'][0]['code']=reasonCode
    
    start=request.POST['start']
    if start!='':
        start=start+':00'
    Procedurejson['performedPeriod']['start']=start    
    end=request.POST['end']
    if end!='':
        end=end+':00'
    Procedurejson['performedPeriod']['end']=end    
    #print(Procedurejson)
    payload = json.dumps(Procedurejson)
    
    if method=='GET':
        if patient!='':
            Procedureurl=Procedureurl+'patient='+patient+'&'
        response = requests.request(method, Procedureurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Procedureurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Procedure/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Procedure/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def iot5g(request):
    url = "https://bgceget982.execute-api.us-west-2.amazonaws.com/dev/device_data/blood_oxygen?userId=8d410255-ebad-45ee-8753-255341160894&mac=C026DA1744DA"
    url1 = "https://bgceget982.execute-api.us-west-2.amazonaws.com/dev/device_data/body_temp?userId=8d410255-ebad-45ee-8753-255341160894&mac=C026DA1B07EA"
    url2 = "https://bgceget982.execute-api.us-west-2.amazonaws.com/dev/device_data/blood_pressure?userId=8d410255-ebad-45ee-8753-255341160894&mac=C026DA10EB01"
    urln = "https://bgceget982.execute-api.us-west-2.amazonaws.com/dev/device_data/devices?userId=8d410255-ebad-45ee-8753-255341160894"
    payload={}
    headers = {}
    
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    response1 = requests.request("GET", url1, headers=headers, data=payload, verify=False)
    response2 = requests.request("GET", url2, headers=headers, data=payload, verify=False)
    responsen = requests.request("GET", urln, headers=headers, data=payload, verify=False)
    #print(response.text)

    resultjson=json.loads(response.text)
    #print(resultjson)
    resultjson1=json.loads(response1.text)
    resultjson2=json.loads(response2.text)
    resultjsonn=json.loads(responsen.text)
    dtime = datetime.datetime.fromtimestamp(resultjson[0]['epoch'])
    latestdatetime=[]
    for i in range(len(resultjsonn)):
        latestdatetime.append(str(datetime.datetime.fromtimestamp(resultjsonn[i]['latest'][0]['epoch'])))
    
    datejson=[]
    for i in range(len(resultjson)):    
        #datejson.append(str(dtime.date()+datetime.timedelta(i))[5:10])
        datejson.append(str(datetime.datetime.fromtimestamp(resultjson[i]['epoch']).month)+'-'+\
                        str(datetime.datetime.fromtimestamp(resultjson[i]['epoch']).day)+' '+\
                        str(datetime.datetime.fromtimestamp(resultjson[i]['epoch']).hour)+':'+\
                        str(datetime.datetime.fromtimestamp(resultjson[i]['epoch']).minute))
            
        #print(datetime.datetime.fromtimestamp(resultjson[i]['epoch']).month)
    dtime1 = datetime.datetime.fromtimestamp(resultjson1[0]['epoch'])
    datejson1=[]
    for i in range(len(resultjson1)):    
        #datejson1.append(str(dtime1.date()+datetime.timedelta(i))[5:10])
        datejson1.append(str(datetime.datetime.fromtimestamp(resultjson1[i]['epoch']).month)+'-'+\
                         str(datetime.datetime.fromtimestamp(resultjson1[i]['epoch']).day)+' '+\
                         str(datetime.datetime.fromtimestamp(resultjson1[i]['epoch']).hour)+':'+\
                         str(datetime.datetime.fromtimestamp(resultjson1[i]['epoch']).minute))
        #print(datetime.datetime.fromtimestamp(resultjson1[i]['epoch']).day)
    datejson2=[]
    for i in range(len(resultjson2)):    
        #datejson1.append(str(dtime1.date()+datetime.timedelta(i))[5:10])
        datejson2.append(str(datetime.datetime.fromtimestamp(resultjson2[i]['epoch']).month)+'-'+\
                         str(datetime.datetime.fromtimestamp(resultjson2[i]['epoch']).day)+' '+\
                         str(datetime.datetime.fromtimestamp(resultjson2[i]['epoch']).hour)+':'+\
                         str(datetime.datetime.fromtimestamp(resultjson2[i]['epoch']).minute))
        #print(datetime.datetime.fromtimestamp(resultjson1[i]['epoch']).day)

    return ('GET OK',resultjson,datejson,resultjson1,datejson1,latestdatetime\
            ,resultjsonn,resultjson2,datejson2)


def ServiceRequestCRUD(request):
    ServiceRequestPath=str(pathlib.Path().absolute()) + "/static/template/ServiceRequest化療處方歷程.json"
    #print(ProcedurePath)
    ServiceRequestjson = json.load(open(ServiceRequestPath,encoding="utf-8"))
    #print(ServiceRequestjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    ServiceRequesturl = fhir+'ServiceRequest?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    ServiceRequestjson['id']=resourceTypeid
    patient=request.POST['patient']
    ServiceRequestjson['subject']['reference']='Patient/'+patient
    
    requester=request.POST['requester']
    ServiceRequestjson['requester']['reference']='Practitioner/'+requester
    
    authorString=request.POST['authorString']
    ServiceRequestjson['note'][0]['authorString']=authorString
    text=request.POST['text']
    ServiceRequestjson['note'][0]['text']=text
    
    time=request.POST['time']
    if time!='':
        time=time+':00'
    ServiceRequestjson['note'][0]['time']=time
   
    #print(ServiceRequestjson)
    payload = json.dumps(ServiceRequestjson)
    
    if method=='GET':
        if patient!='':
            ServiceRequesturl=ServiceRequesturl+'patient='+patient+'&'
        response = requests.request(method, ServiceRequesturl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, ServiceRequesturl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"ServiceRequest/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"ServiceRequest/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def CarePlanCRUD(request):
    CarePlanPath=str(pathlib.Path().absolute()) + "/static/template/CarePlan護理紀錄.json"
    #print(CarePlanPath)
    CarePlanjson = json.load(open(CarePlanPath,encoding="utf-8"))
    #print(CarePlanjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    CarePlanurl = fhir+'CarePlan?'
    method=request.POST['method']
    CarePlan=request.POST['CarePlan']
    CarePlanjson['id']=CarePlan
    patient=request.POST['patient']
    CarePlanjson['subject']['reference']='Patient/'+patient

    encounter=request.POST['encounter']
    CarePlanjson['encounter']['reference']='Encounter/'+encounter
    contributor=request.POST['contributor']
    CarePlanjson['contributor'][0]['reference']='Practitioner/'+contributor
    
    created=request.POST['created']
    if created!='':
        created=created+':00'
    CarePlanjson['created']=created

    #print(CarePlanjson)
    payload = json.dumps(CarePlanjson)
    
    if method=='GET':
        if patient!='':
            CarePlanurl=CarePlanurl+'patient='+patient+'&'
        if encounter!='':
            CarePlanurl=CarePlanurl+'encounter='+encounter+'&'
        response = requests.request(method, CarePlanurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, CarePlanurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"CarePlan/"+str(CarePlan)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"CarePlan/"+str(CarePlan)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')
    
def DiagnosticReportNursingCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/DiagnosticReport護理紀錄.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    DiagnosticReportNursingjsonurl = fhir+'DiagnosticReport?code=28623-7&'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    DiagnosticReportNursingjson['id']=resourceTypeid
    patient=request.POST['patient']
    DiagnosticReportNursingjson['subject']['reference']='Patient/'+patient

    basedOn=request.POST['basedOn']
    DiagnosticReportNursingjson['basedOn'][0]['reference']='CarePlan/'+basedOn
    encounter=request.POST['encounter']
    DiagnosticReportNursingjson['encounter']['reference']='Encounter/'+encounter

    performer=request.POST['performer']
    DiagnosticReportNursingjson['performer'][0]['reference']='Organization/'+performer
    result=request.POST['result']
    DiagnosticReportNursingjson['result'][0]['reference']='Observation/'+result
    
    issued=request.POST['issued']
    if issued!='':
        issued=issued+':00'
    DiagnosticReportNursingjson['issued']=issued
    
    #print(DiagnosticReportNursingjson)
    payload = json.dumps(DiagnosticReportNursingjson)
    
    if method=='GET':
        if patient!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'patient='+patient+'&'
        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"DiagnosticReport/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"DiagnosticReport/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def DiagnosticReportRadiationTreatmentCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/DiagnosticReport放腫報告.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    DiagnosticReportNursingjsonurl = fhir+'DiagnosticReport?code=21880-0&'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    DiagnosticReportNursingjson['id']=resourceTypeid
    DiagnosticReportNursingjson['identifier'][0]['value']=resourceTypeid
    patient=request.POST['patient']
    DiagnosticReportNursingjson['subject']['reference']='Patient/'+patient
    
    basedOn=request.POST['basedOn']
    DiagnosticReportNursingjson['basedOn'][0]['reference']='ServiceRequest/'+basedOn

    performer=request.POST['performer']
    DiagnosticReportNursingjson['performer'][0]['reference']='Organization/'+performer
    conclusion=request.POST['conclusion']
    DiagnosticReportNursingjson['conclusion']=conclusion
    
    issued=request.POST['issued']
    if issued!='':
        issued=issued+':00'
    DiagnosticReportNursingjson['issued']=issued
        
    #print(DiagnosticReportNursingjson)
    payload = json.dumps(DiagnosticReportNursingjson)
    
    if method=='GET':
        if patient!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'patient='+patient+'&'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)

        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"DiagnosticReport/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"DiagnosticReport/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def DiagnosticReportPathologyReportCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/DiagnosticReport病理報告.json"
    #print(jsonPath)
    DiagnosticReportNursingjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    DiagnosticReportNursingjsonurl = fhir+'DiagnosticReport?code=22637-3&'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    DiagnosticReportNursingjson['id']=resourceTypeid

    DiagnosticReportNursingjson['identifier'][0]['value']=resourceTypeid
    patient=request.POST['patient']
    DiagnosticReportNursingjson['subject']['reference']='Patient/'+patient

    performer=request.POST['performer']
    DiagnosticReportNursingjson['performer'][0]['reference']='Organization/'+performer

    conclusion=request.POST['conclusion']
    DiagnosticReportNursingjson['conclusion']=conclusion
    conclusionCode=request.POST['conclusionCode']
    DiagnosticReportNursingjson['conclusionCode'][0]['text']=conclusionCode
    conclusionCode1=request.POST['conclusionCode1']
    DiagnosticReportNursingjson['conclusionCode'][1]['text']=conclusionCode1
    
    issued=request.POST['issued']
    if issued!='':
        issued=issued+':00'
    DiagnosticReportNursingjson['issued']=issued
       
    #print(DiagnosticReportNursingjson)
    payload = json.dumps(DiagnosticReportNursingjson)
    
    if method=='GET':
        if patient!='':
            DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'patient='+patient+'&'
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)

        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, DiagnosticReportNursingjsonurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"DiagnosticReport/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"DiagnosticReport/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def ConditionStageCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Condition癌症分期.json"
    #print(jsonPath)
    Conditionjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(DiagnosticReportNursingjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Conditionurl = fhir+'Condition?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    Conditionjson['id']=resourceTypeid
    patient=request.POST['patient']
    Conditionjson['subject']['reference']='Patient/'+patient

    asserter=request.POST['asserter']
    Conditionjson['asserter']['reference']='Practitioner/'+asserter

    snomed=request.POST['snomed']
    Conditionjson['code']['coding'][0]['code']=snomed
    display=request.POST['display']
    Conditionjson['code']['coding'][0]['display']=display
    
    category=request.POST['category']
    Conditionjson['category'][0]['coding'][0]['code']=category
    tumor=request.POST['tumor']
    Conditionjson['stage'][0]['summary']['coding'][0]['code']=tumor
    nodes=request.POST['nodes']
    Conditionjson['stage'][1]['summary']['coding'][0]['code']=nodes
    metastasis=request.POST['metastasis']
    Conditionjson['stage'][2]['summary']['coding'][0]['code']=metastasis
    
    onsetDateTime=request.POST['onsetDateTime']
    if onsetDateTime!='':
        onsetDateTime=onsetDateTime+':00'
    Conditionjson['onsetDateTime']=onsetDateTime
        
    #print(Conditionjson)
    payload = json.dumps(Conditionjson)
    
    if method=='GET':
        if patient!='':
            Conditionurl=Conditionurl+'patient='+patient+'&'
        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Condition/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Condition/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')
    
def ImagingStudyCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/ImagingStudy.json"
    #print(jsonPath)
    Conditionjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Conditionjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Conditionurl = fhir+'ImagingStudy?'
    #print(Conditionurl)
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    Conditionjson['id']=resourceTypeid
    patient=request.POST['patient']
    Conditionjson['subject']['reference']='Patient/'+patient
    '''
    asserter=request.POST['asserter']
    Conditionjson['asserter']['reference']='Practitioner/'+asserter

    snomed=request.POST['snomed']
    Conditionjson['code']['coding'][0]['code']=snomed
    display=request.POST['display']
    Conditionjson['code']['coding'][0]['display']=display
    
    category=request.POST['category']
    Conditionjson['category'][0]['coding'][0]['code']=category
    tumor=request.POST['tumor']
    Conditionjson['stage'][0]['summary']['coding'][0]['code']=tumor
    nodes=request.POST['nodes']
    Conditionjson['stage'][1]['summary']['coding'][0]['code']=nodes
    metastasis=request.POST['metastasis']
    Conditionjson['stage'][2]['summary']['coding'][0]['code']=metastasis
    
    onsetDateTime=request.POST['onsetDateTime']
    if onsetDateTime!='':
        onsetDateTime=onsetDateTime+':00'
    Conditionjson['onsetDateTime']=onsetDateTime
    '''        
    #print(Conditionjson)
    payload = json.dumps(Conditionjson)
    
    if method=='GET':
        if patient!='':
            Conditionurl=Conditionurl+'patient='+patient+'&'
        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"ImagingStudy/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"ImagingStudy/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')
    
def EndpointCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Endpoint.json"
    #print(jsonPath)
    Conditionjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Conditionjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Conditionurl = fhir+'Endpoint?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    Conditionjson['id']=resourceTypeid
    patient=request.POST['patient']
    #Conditionjson['subject']['reference']='Patient/'+patient
    '''
    asserter=request.POST['asserter']
    Conditionjson['asserter']['reference']='Practitioner/'+asserter

    snomed=request.POST['snomed']
    Conditionjson['code']['coding'][0]['code']=snomed
    display=request.POST['display']
    Conditionjson['code']['coding'][0]['display']=display
    
    category=request.POST['category']
    Conditionjson['category'][0]['coding'][0]['code']=category
    tumor=request.POST['tumor']
    Conditionjson['stage'][0]['summary']['coding'][0]['code']=tumor
    nodes=request.POST['nodes']
    Conditionjson['stage'][1]['summary']['coding'][0]['code']=nodes
    metastasis=request.POST['metastasis']
    Conditionjson['stage'][2]['summary']['coding'][0]['code']=metastasis
    
    onsetDateTime=request.POST['onsetDateTime']
    if onsetDateTime!='':
        onsetDateTime=onsetDateTime+':00'
    Conditionjson['onsetDateTime']=onsetDateTime
    '''        
    #print(Conditionjson)
    payload = json.dumps(Conditionjson)
    
    if method=='GET':
        if patient!='':
            Conditionurl=Conditionurl+'patient='+patient+'&'
        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Endpoint/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Endpoint/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def MedicationCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Medication.json"
    #print(jsonPath)
    Conditionjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Conditionjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Conditionurl = fhir+'Medication?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    Conditionjson['id']=resourceTypeid
    nhicode=request.POST['nhicode']
    Conditionjson['code']['coding'][0]['code']=nhicode
    Conditionjson['code']['coding'][0]['display']=nhicode[3:7]
    atccode=request.POST['atccode']
    Conditionjson['code']['coding'][1]['code']=atccode
    display=request.POST['display']
    Conditionjson['code']['coding'][1]['display']=display
    text=request.POST['text']
    Conditionjson['code']['text']=text
  
    #print(Conditionjson)
    payload = json.dumps(Conditionjson)
    
    if method=='GET':
        if nhicode!='':
            Conditionurl=Conditionurl+'code='+nhicode+'&'
        if atccode!='':
            Conditionurl=Conditionurl+'code='+atccode+'&'
        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Medication/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Medication/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def MedicationRequestCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/MedicationRequest.json"
    #print(jsonPath)
    Conditionjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Conditionjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Conditionurl = fhir+'MedicationRequest?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    Conditionjson['id']=resourceTypeid
    patient=request.POST['patient']
    Conditionjson['subject']['reference']='Patient/'+patient
    category=request.POST['category']
    Conditionjson['category'][0]['coding'][0]['code']=category
    medicationReference=request.POST['medicationReference']
    Conditionjson['medicationReference']['reference']='Medication/'+medicationReference
    Conditionjson['medicationCodeableConcept']['coding'][0]['code']=medicationReference
    authoredOn=request.POST['authoredOn']
    Conditionjson['authoredOn']=authoredOn
    
    text=request.POST['text']
    Conditionjson['medicationCodeableConcept']['text']=text
    display=request.POST['display']
    Conditionjson['medicationCodeableConcept']['coding'][0]['display']=display
    timing=request.POST['timing']
    Conditionjson['dosageInstruction'][0]['timing']['code']['coding'][0]['code']=timing
    dosageroute=request.POST['dosageroute']
    Conditionjson['dosageInstruction'][0]['route']['coding'][0]['code']=dosageroute
    dosagemethod=request.POST['dosagemethod']
    Conditionjson['dosageInstruction'][0]['method']['coding'][0]['code']=dosagemethod
    start=request.POST['start']
    Conditionjson['dispenseRequest']['validityPeriod']['start']=start
    end=request.POST['end']
    Conditionjson['dispenseRequest']['validityPeriod']['end']=end    
    expectedSupplyDuration=request.POST['expectedSupplyDuration']
    Conditionjson['dispenseRequest']['expectedSupplyDuration']['value']=expectedSupplyDuration
    
    quantity=request.POST['quantity']
    Conditionjson['dispenseRequest']['quantity']['value']=quantity
    quantitycode=request.POST['quantitycode']
    Conditionjson['dispenseRequest']['quantity']['code']=quantitycode 
    Conditionjson['dispenseRequest']['quantity']['unit']=quantitycode
  
    #print(Conditionjson)
    payload = json.dumps(Conditionjson)
    
    if method=='GET':
        if patient!='':
            Conditionurl=Conditionurl+'patient='+patient+'&'

        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"MedicationRequest/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"MedicationRequest/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def MedicationAdministrationCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/MedicationAdministration.json"
    #print(jsonPath)
    Conditionjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Conditionjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Conditionurl = fhir+'MedicationAdministration?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    Conditionjson['id']=resourceTypeid
    patient=request.POST['patient']
    Conditionjson['subject']['reference']='Patient/'+patient

    medicationReference=request.POST['medicationReference']
    Conditionjson['medicationReference']['reference']='Medication/' + medicationReference
    
    medicationrequest=request.POST['medicationrequest']
    Conditionjson['request']['reference']='MedicationRequest/' + medicationrequest
    
    dosageroute=request.POST['dosageroute']
    Conditionjson['dosage']['route']['coding'][0]['code']=dosageroute
    dosagemethod=request.POST['dosagemethod']
    Conditionjson['dosage']['method']['coding'][0]['code']=dosagemethod
    start=request.POST['start']
    Conditionjson['effectivePeriod']['start']=start
    end=request.POST['end']
    Conditionjson['effectivePeriod']['end']=end    
    
    quantity=request.POST['quantity']
    Conditionjson['dosage']['dose']['value']=quantity
    quantitycode=request.POST['quantitycode']
    Conditionjson['dosage']['dose']['code']=quantitycode 
    Conditionjson['dosage']['dose']['unit']=quantitycode
  
    #print(Conditionjson)
    payload = json.dumps(Conditionjson)
    
    if method=='GET':
        if patient!='':
            Conditionurl=Conditionurl+'patient='+patient+'&'

        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"MedicationAdministration/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"MedicationAdministration/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def ImmunizationCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Immunization.json"
    #print(jsonPath)
    Conditionjson = json.load(open(jsonPath,encoding="utf-8"))
    #print(Conditionjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Conditionurl = fhir+'Immunization?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    Conditionjson['id']=resourceTypeid
    patient=request.POST['patient']
    Conditionjson['patient']['reference']='Patient/'+patient
    status=request.POST['status']
    Conditionjson['status']=status
    occurrenceDateTime=request.POST['occurrenceDateTime']
    Conditionjson['occurrenceDateTime']=occurrenceDateTime
    manufacturer=request.POST['manufacturer']
    Conditionjson['manufacturer']['reference']='Organization/' + manufacturer
    lotNumber=request.POST['lotNumber']
    Conditionjson['lotNumber']=lotNumber
    doseNumberPositiveInt=request.POST['doseNumberPositiveInt']
    Conditionjson['protocolApplied'][0]['doseNumberPositiveInt']=doseNumberPositiveInt
    seriesDosesPositiveInt=request.POST['seriesDosesPositiveInt']
    Conditionjson['protocolApplied'][0]['seriesDosesPositiveInt']=seriesDosesPositiveInt    
    #print(Conditionjson)
    payload = json.dumps(Conditionjson)
    
    if method=='GET':
        if patient!='':
            Conditionurl=Conditionurl+'patient='+patient+'&'
        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, Conditionurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Immunization/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Immunization/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def MolecularSequenceCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/MolecularSequence.json"
    #print(jsonPath)
    templatejson = json.load(open(jsonPath,encoding="utf-8"))
    #print(templatejson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    templateurl = fhir+'MolecularSequence?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    templatejson['id']=resourceTypeid
    patient=request.POST['patient']
    templatejson['patient']['reference']='Patient/'+patient
    specimen=request.POST['specimen']
    templatejson['specimen']['reference']='Specimen/'+specimen
    chromosome=request.POST['chromosome']
    templatejson['referenceSeq']['chromosome']['coding'][0]['code']=chromosome
    templatejson['referenceSeq']['chromosome']['coding'][0]['display']='chromosome '+chromosome
    genomeBuild=request.POST['genomeBuild']
    templatejson['referenceSeq']['genomeBuild']=genomeBuild
    observedAllele=request.POST['observedAllele']
    templatejson['variant'][0]['observedAllele']=observedAllele
    referenceAllele=request.POST['referenceAllele']
    templatejson['variant'][0]['referenceAllele']=referenceAllele
    try:
        start=int(request.POST['start'])
        templatejson['referenceSeq']['windowStart']=start
        templatejson['variant'][0]['start']=start
        end=int(request.POST['end'])
        templatejson['referenceSeq']['windowEnd']=end
        templatejson['variant'][0]['end']=end

    except:
        None
        #print(templatejson)
    payload = json.dumps(templatejson)
    #print(method)
    #print(patient)
    
    if method=='GET':
        #print(patient)        
        if patient!='':
            templateurl=templateurl+'patient='+patient+'&'
        if chromosome!='':
            templateurl=templateurl+'chromosome='+chromosome+'&'
        try:
            if start!='':
                templateurl=templateurl+'window-start='+start+'&'
            if end!='':
                templateurl=templateurl+'window-end='+end+'&'
        except:
            None
        #print(templateurl)
        response = requests.request(method, templateurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, templateurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Medication/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Medication/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def ObservationGeneticsCRUD(request):
    jsonPath=str(pathlib.Path().absolute()) + "/static/template/Observation-genetics.json"
    #print(jsonPath)
    templatejson = json.load(open(jsonPath,encoding="utf-8"))
    #print(templatejson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    templateurl = fhir+'Observation?code=69548-6'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    templatejson['id']=resourceTypeid
    patient=request.POST['patient']
    templatejson['subject']['reference']='Patient/'+patient
    specimen=request.POST['specimen']
    templatejson['specimen']['reference']='Specimen/'+specimen
    effectiveDateTime=request.POST['effectiveDateTime']
    #print(effectiveDateTime)
    templatejson['effectiveDateTime']=effectiveDateTime+':00'
    Genecode=request.POST['Genecode']
    templatejson['component'][0]['valueCodeableConcept']['coding'][0]['code']=Genecode
    Gene=request.POST['Gene']
    templatejson['component'][0]['valueCodeableConcept']['coding'][0]['display']=Gene
    DNAchange=request.POST['DNAchange']
    templatejson['component'][1]['valueCodeableConcept']['coding'][0]['code']=DNAchange
    AcidChange=request.POST['AcidChange']
    templatejson['component'][2]['valueCodeableConcept']['coding'][0]['display']=AcidChange

    #print(templatejson)
    payload = json.dumps(templatejson)
    #print(method)
    #print(Conditionurl)
    if method=='GET':
        #if encounter!='':
        #    DiagnosticReportNursingjsonurl=DiagnosticReportNursingjsonurl+'encounter='+encounter+'&'
        response = requests.request(method, templateurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return ('GET OK',resultjson)
    elif method=='POST':
        response = requests.request(method, templateurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Medication/"+str(resourceTypeid)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Medication/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')

def ObservationImagingCRUD(request):
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    templateurl = fhir+'Observation?'
    method=request.POST['method']
    resourceTypeid=request.POST['id']
    patient=request.POST['patient']

    if method=='GET':
        if resourceTypeid!='':
            templateurl=templateurl+'_id='+resourceTypeid+'&'
        if patient!='':
            templateurl=templateurl+'subject='+patient+'&'
        response = requests.request(method, templateurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)
        return ('GET OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Observation/"+str(resourceTypeid)
        GetResponse = requests.request('GET', PUTurl, headers=headers, data=payload, verify=False)
        OriginJson = json.loads(GetResponse.text)
        patient=request.POST['patient']
        if patient!='':
            reference={'reference' : 'Patient/'+patient }
            OriginJson['subject']=reference
        icd10=request.POST['icd10']
        if icd10!='':
            OriginJson['code']['coding'][0]['code']=icd10
        display=request.POST['display']
        if display!='':
            OriginJson['code']['coding'][0]['display']=display
        payload = json.dumps(OriginJson)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Observation/"+str(resourceTypeid)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')
    
def GeneCRUD(request):
    try:
        PatientID=request.POST['PatientID']
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }
        payload={}
        Observationurl=fhir+'Observation?'
        getObservationurl = Observationurl+'subject='+PatientID.replace('_','')
        
        #print(getObservationurl,headers,payload)
        Observationresponse = requests.request("GET", getObservationurl, headers=headers, data=payload, verify=False)
        #print(Observationresponse.text)
        ObservationResultjson=json.loads(Observationresponse.text)
        HBBlist=[]
        Obes_list=[]
        ABCG2list=[]
        ALDH2list=[]
        NOTCH3list=[]
        LDLRlist=[]
        CYP2C19list=[]
        PCSK9list=[]
        APOBlist=[]
        KCNJ11list=[]
        ABCC8list=[] 
        HNF4Alist=[]
        HNF1Alist=[]
        GCKlist=[]
        TPMTlist=[]
        import math
        cycle=math.ceil(ObservationResultjson['total']/20)
        if cycle > 0:
            for page in range(1,cycle):
                 pageurl='&_getpagesoffset='+str(page*20)
                 #print(getObservationurl+pageurl)
                 pageurlresponse = requests.request("GET", getObservationurl+pageurl, headers=headers, data=payload, verify=False)
                 pageurlResultjson=json.loads(pageurlresponse.text)
                 ObservationResultjson['entry'].extend(pageurlResultjson['entry'])
        #print(ObservationResultjson['total'])
        for i in range(ObservationResultjson['total']):
            #print(i)
            #print(ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['code'])
            ##51968-6
            if ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['code']=='51968-6':
               #print(ObservationResultjson['entry'][i]['resource']['component'][0]['valueString'])
                final_comment=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
            ##diagnostic-implication
            elif ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['code']=='diagnostic-implication':
                #print(ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code'],i)
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='65959000':
                    #print(ObservationResultjson['entry'][i]['resource']['component'][0]['valueString'])
                    HBB_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                    #print(HBB_risk)
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='414916001':
                    Obes_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='398036000':
                    FH_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='609561005':
                    MODY_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='Azathioprine藥物代謝風險':
                    TPMT_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                if ObservationResultjson['entry'][i]['resource']['component'][1]['valueCodeableConcept']['coding'][0]['code']=='clopidogrel藥物代謝風險':
                    CYP2C19_risk=ObservationResultjson['entry'][i]['resource']['component'][0]['valueString']
                    print(CYP2C19_risk)
            
            ##84413-4
            elif ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['code']=='84413-4':
                #print(ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])
                #print(ObservationResultjson['entry'][i]['resource']['component'][0]['valueCodeableConcept']['coding'][0]['display'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='HBB':
                    #print(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                    HBBlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                    #print(HBBlist)
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='FTO':
                    Obes_list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='ABCG2':
                    ABCG2list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                                        
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='ALDH2':
                    ALDH2list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='NOTCH3':
                    NOTCH3list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                                               
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='CYP2C19':
                    CYP2C19list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='LDLR':
                    LDLRlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='PCSK9':
                    PCSK9list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='APOB':
                    APOBlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='ABCC8':
                    ABCC8list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='KCNJ11':
                    KCNJ11list.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='HNF4A':
                    HNF4Alist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='HNF1A':
                    HNF1Alist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                    
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='GCK':
                    GCKlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                    
                if (ObservationResultjson['entry'][i]['resource']['code']['coding'][0]['display'])=='TPMT':
                    TPMTlist.append(ObservationResultjson['entry'][i]['resource']['valueCodeableConcept']['text'])                    
            else:
                None
        #print(1)
            
        context = {
                'PatientID' : PatientID,
                'ALDH2list' : ALDH2list,
                'Obes_list' : Obes_list,
                'ABCG2list' : ABCG2list,
                'HBBlist' : HBBlist,
                'LDLRlist' : LDLRlist,
                'PCSK9list' : PCSK9list,
                'APOBlist' : APOBlist,
                'NOTCH3list' : NOTCH3list,
                'CYP2C19list' : CYP2C19list,
                'KCNJ11list' : KCNJ11list,
                'ABCC8list' : ABCC8list,
                'HNF4Alist' : HNF4Alist,
                'HNF1Alist' : HNF1Alist,
                'GCKlist' : GCKlist,
                'TPMTlist' : TPMTlist,
                'HBB_risk' : HBB_risk,
                'Obes_risk' : Obes_risk,
                'FH_risk' : FH_risk,
                'MODY_risk' : MODY_risk,
                'CYP2C19_risk' : CYP2C19_risk,
                'TPMT_risk' : TPMT_risk,
                'final_comment' : final_comment
                }
        #print(context)
        return context
    except:
        return None
        #print('except')

def ReferralCRUD(request):
    EncounterPath=str(pathlib.Path().absolute()) + "/static/template/Encounter住院.json"
    #print(EncounterPath)
    Encounterjson = json.load(open(EncounterPath,encoding="utf-8"))
    #print(Encounterjson)
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    Encounterurl = fhir+'Encounter?'
    method=request.POST['method']
    Encounter=request.POST['Encounter']
    Encounterjson['id']=Encounter
    patient=request.POST['patient']
    Encounterjson['subject']['reference']='Patient/'+patient
    location=request.POST['location']
    Encounterjson['location'][0]['location']['display']=location
    start=request.POST['start']
    if start!='':
        start=start+':00'
    Encounterjson['location'][0]['period']['start']=start
    end=request.POST['end']
    if end!='':
        end=end+':00'
    Encounterjson['location'][0]['period']['end']=end
    #print(Encounterjson)
    payload = json.dumps(Encounterjson)
    
    if method=='GET':
        if patient!='':
            Encounterurl=Encounterurl+'patient='+patient+'&'
            response = requests.request(method, Encounterurl, headers=headers, data=payload, verify=False)
            resultjson=json.loads(response.text)
            prtj=''
            ohrtj=''
            ihrtj=''
            crtj=''
            odrtj=''
            idrtj=''
        elif Encounter!='':
            Encounterurl=Encounterurl.replace('?','/')+Encounter
            response = requests.request(method, Encounterurl, headers=headers, data=payload, verify=False)
            resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
            patienturl=fhir+resultjson['entry'][0]['resource']['subject']['reference']
            prt = requests.request(method, patienturl, headers=headers, data=payload, verify=False)
            prtj=json.loads(prt.text)
            originurl=fhir+resultjson['entry'][0]['resource']['hospitalization']['origin']['reference']
            ohrt = requests.request(method, originurl, headers=headers, data=payload, verify=False)
            ohrtj=json.loads(ohrt.text)
            destinationurl=fhir+resultjson['entry'][0]['resource']['hospitalization']['destination']['reference']
            ihrt = requests.request(method, destinationurl, headers=headers, data=payload, verify=False)
            ihrtj=json.loads(ihrt.text)
            Curl=fhir+resultjson['entry'][0]['resource']['reasonReference'][0]['reference']
            crt = requests.request(method, Curl, headers=headers, data=payload, verify=False)
            crtj=json.loads(crt.text)
            outdrurl=fhir+resultjson['entry'][0]['resource']['participant'][1]['individual']['reference']            
            odrt = requests.request(method, outdrurl, headers=headers, data=payload, verify=False)
            odrtj=json.loads(odrt.text)
            indrurl=fhir+resultjson['entry'][0]['resource']['participant'][0]['individual']['reference']            
            idrt = requests.request(method, indrurl, headers=headers, data=payload, verify=False)
            idrtj=json.loads(idrt.text)
        else:
            response = requests.request(method, Encounterurl, headers=headers, data=payload, verify=False)
            resultjson=json.loads(response.text)
            prtj=''
            ohrtj=''
            ihrtj=''
            crtj=''
            odrtj=''
            idrtj=''
        return ('GET OK',resultjson,prtj,ohrtj,ihrtj,crtj,odrtj,idrtj)
    elif method=='POST':
        response = requests.request(method, Encounterurl, headers=headers, data=payload, verify=False)
        #resstr='{"entry":[{"resource":'+response.text+'}]}'
        #print(response.text)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        #print(resultjson)        
        return ('POST OK',resultjson)
    elif method=='PUT':
        PUTurl = fhir+"Encounter/"+str(Encounter)
        response = requests.request(method, PUTurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads('{"entry":[{"resource":'+response.text+'}]}')
        return ('PUT OK',resultjson)
    elif method=='DELETE':
        DELETEurl = fhir+"Encounter/"+str(Encounter)
        response = requests.request(method, DELETEurl, headers=headers, data=payload, verify=False)
        resultjson=json.loads(response.text)        
        return ('DELETE OK',resultjson['issue'][0])
    else:
        return ('method NG')