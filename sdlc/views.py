from django.shortcuts import render,redirect#, from django.shortcuts import redirectget_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
#from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import pandas as pd
import pathlib
import os
import json 
import requests
import psycopg2
import shutil
import zipfile
from . import gene2cbio
from . import Function
from . import models

from django.core.servers.basehttp import WSGIServer
WSGIServer.handle_error = lambda *args, **kwargs: None

import warnings
warnings.filterwarnings('ignore')

def flatten_dict(d):
    flattened_dict = {}

    def flatten(item, key=''):
        if isinstance(item, dict):
            for sub_key, sub_item in item.items():
                flatten(sub_item, key + sub_key + '_')
        elif isinstance(item, list):
            for i, sub_item in enumerate(item):
                flatten(sub_item, key + str(i) + '_')
        else:
            flattened_dict[key[:-1]] = item

    flatten(d)
    return flattened_dict

def unflatten_dict(flat_dict):
    unflattened_dict = {}
    for key, value in flat_dict.items():
        parts = key.split('_')  # 拆分键名中的点号
        current_dict = unflattened_dict
        for part in parts[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        current_dict[parts[-1]] = value
    return unflattened_dict

DocumentPath = str(pathlib.Path().absolute()) + "/static/doc/"
risk = DocumentPath + 'risk.csv'
riskdf = pd.read_csv(risk, encoding='utf8')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#genepostgresip = "104.208.68.39"
genepostgresip = "104.215.60.228"

#genepostgresport="8081"
genepostgresport="5432"
jsonPath=str(pathlib.Path().absolute()) + "/static/template/Observation-Imaging-EKG.json"
ObservationImagingEKGJson = json.load(open(jsonPath,encoding="utf-8"))

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

@csrf_exempt 
def auth(request):
    user = request.user
    #print(user.username)
    Generight=models.Genepermission.objects.filter(user__username__startswith=user.username).values()
    #print(Generight[0].get('cbioportal'))
    #print(Generight[0].get('cbioportal1'))
    if request.user.is_authenticated and Generight[0].get('cbioportal'):
        #return redirect('https://20.212.244.127:8080')
        return HttpResponse('Authenticated' ,status = 200)
        #return HttpResponse('Authenticated')
    elif request.user.is_authenticated and Generight[0].get('cbioportal1'):
        return HttpResponse('Unauthenticated',status = 401)
        #return redirect('https://104.42.221.219/accounts/login/')
    else:
        return HttpResponse('forbidden',status = 403)
        #return HttpResponse('Authenticated')

def index(request):
    try:
        #User = get_user_model()
        #usersdf = User.objects.all().values()
        #print(type([{i.title: i.specs} for i in User.objects.all()]))
        #print([{i.title: i.specs} for i in User.objects.all()])
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        context = {
                'Generight' : Generight,
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'index.html', context)
    except:
        context = {
                'Generight' : Generight,
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'index.html', context)
@csrf_exempt
def convert(request):
    try:
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Resourcejsonall=models.Resourcejson.objects.all()
        
        rows=''
        flattendict=''
        Resource=''
        try:
            uploadedFile = request.FILES["uploadedFile"]
            Resourcejson = models.Resourcejson(
                uploadedFile = uploadedFile
            )
            Resourcejson.save()  
        except:
            uploadedFile = '' 
        try:
            if request.POST['DBtype'] != '' and request.POST['IP'] != '' and request.POST['Port'] != '' and request.POST['ID'] != '' and request.POST['PassWord'] != '' and request.POST['table'] != '' and  request.POST['db'] != '':
                DBtype=request.POST['DBtype']
                IP=request.POST['IP']
                Port=request.POST['Port']
                ID=request.POST['ID'] 
                PassWord=request.POST['PassWord']
                db=request.POST['db']
                table=request.POST['table']
                dbconn={
                    'DBtype':DBtype,
                    'IP':IP,
                    'Port':Port,
                    'ID':ID,
                    'PassWord':PassWord,
                    'db':db,
                    'table':table                
                    }
                #print(dbconn)
                conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
                #conn = psycopg2.connect(database=db, user=ID, password=PassWord, host=IP, port=Port)
                cur = conn.cursor()
                #db list
                #consentsql = "SELECT table_schema,table_name FROM information_schema.tables where table_schema='public';"
                #table list
                consentsql = "SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'reportxml';"
                #consentsql = "SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '"+table+"';"
                #print(consentsql)
                cur.execute(consentsql)
                rows = cur.fetchall()
                #print(rows)
        except:
            dbconn={}
            rows={}

        if request.POST['Resource'] != '':
            #print(request.POST['Resource'])
            Resource=request.POST['Resource']        
            jsonPath=str(pathlib.Path().absolute()) + '/media/'+Resource
            cancerbasejson = json.load(open(jsonPath,encoding="utf-8"))
            flattendict=flatten_dict(cancerbasejson)
            for k in flattendict.keys():
                if request.POST[k+'_select']!='':
                    #print(request.POST[k+'_select'])
                    flattendict[k]='SQL_'+table + '_' + request.POST[k+'_select']
                else:
                    pass
            with open('static/doc/Resource.json', 'w', encoding='utf-8') as fp:
                json.dump(flattendict, fp, indent=1) 

    except:
        pass
    
    try:
        context = {
                'dbconn' : dbconn,
                'Resource' : Resource,
                'Resourcejsonall' : Resourcejsonall,
                'rows':rows,
                'flattendict' : flattendict,
                'Generight' : Generight,
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'convert.html', context)
    except:
        context = {
                'Generight' : Generight,
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'convert.html', context)
    
def GeneReport(request):
    #Function.postlog(request)
    try:
        ReportNo=''
        MPNo=''
        MRN=''
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
        cur = conn.cursor()
        consentsql = 'SELECT * FROM public.reportxml where true '
        #consentsql = 'SELECT * FROM public.reportxml WHERE "ReportNo" = \'M111-10001\''

        if request.POST['ReportNo'] != '':
            ReportNo = request.POST['ReportNo']
            consentsql = consentsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\' '
        if request.POST['MPNo'] != '':
            MPNo = request.POST['MPNo']
            consentsql = consentsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\' '
        if request.POST['MRN'] != '':
            MRN = request.POST['MRN']
            consentsql = consentsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%' "
        #elif request.POST['PatientName'] != '':
        #    consentsql = consentsql + "WHERE  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'FullName' LIKE '%" + request.POST['PatientName'] + "%';"
        #elif request.POST['OrderingMD'] != '':
        #    consentsql = consentsql + "WHERE  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'OrderingMD' LIKE '%" + request.POST['OrderingMD'] + "%';"
        #elif request.POST['Diagnosis'] != '':
        #    consentsql = consentsql + "WHERE  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'SubmittedDiagnosis' LIKE '%" + request.POST['Diagnosis'] + "%';"
        #consentsql = consentsql + ' LIMIT 200'
        search={'ReportNo' : ReportNo,
                'MPNo' : MPNo,
                'MRN' : MRN
                }        
        cur.execute(consentsql)
        rows = cur.fetchall()
        print(type(rows))
        df = pd.DataFrame(rows)
        #print(consentsql)
        df.to_csv('static/doc/datalist.csv', sep='\t', encoding='utf-8')
        #print(len(rows))
        SELECTint=len(rows)
        conn.close()
        cur.close()
        context = {
                'Generight' : Generight,
                'search' : search,
                'right' : right,
                'FuncResult' : SELECTint,
                'rows' : rows,
                'ReportNo':ReportNo,
                'MPNo':MPNo,
                'MRN':MRN
                }
        return render(request, 'GeneReport.html', context)
    except:
        conn.close()
        cur.close()
        context = {
                'Generight' : Generight,
                'right' : right,
                'FuncResult' : 'Function',
                'ReportNo':ReportNo,
                'MPNo':MPNo,
                'MRN':MRN
                }
        return render(request, 'GeneReport.html', context)

def PMI(request):
    try:
        #ReportNo=''
        #MPNo=''
        #MRN=''
        Diagnosis=''
        TestType=''
        OrderingMD=''
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
        cur = conn.cursor()
        consentsql = 'SELECT * FROM public.reportxml where true '
        #if request.POST['ReportNo'] != '':
        #    ReportNo = request.POST['ReportNo']
        #    consentsql = consentsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\' '
        #if request.POST['MPNo'] != '':
        #    MPNo = request.POST['MPNo']
        #    consentsql = consentsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\' '
        #if request.POST['MRN'] != '':
        #    MRN = request.POST['MRN']
        #    consentsql = consentsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%' "
        if request.POST['Diagnosis'] != '':
            Diagnosis = request.POST['Diagnosis']
            consentsql = consentsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'SubmittedDiagnosis' LIKE '%" + request.POST['Diagnosis'] + "%' " 
        if request.POST['TestType'] != '':
            TestType = request.POST['TestType']
            consentsql = consentsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'Sample' ->> 'TestType' LIKE '%" + request.POST['TestType'] + "%' "
        if request.POST['OrderingMD'] != '':
            OrderingMD = request.POST['OrderingMD']
            consentsql = consentsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'OrderingMD' LIKE '%" + request.POST['OrderingMD'] + "%' " 
        
        cur.execute(consentsql)
        rows = cur.fetchall()
        
        datalistsql = "SELECT id, \"ReportNo\",\"MPNo\", \
            resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' as \"MRN\", \
                resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'SubmittedDiagnosis' as \"Diagnosis\", \
                    resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'Sample' ->> 'TestType' as \"NGS Assay\", \
                        resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'OrderingMD' as \"OrderingMD\" \
                            FROM public.reportxml where true "
        #if request.POST['ReportNo'] != '':            
        #    datalistsql = datalistsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\''
        #if request.POST['MPNo'] != '':            
        #    datalistsql = datalistsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\''
        #if request.POST['MRN'] != '':           
        #    datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%'"
        if request.POST['Diagnosis'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'SubmittedDiagnosis' LIKE '%" + request.POST['Diagnosis'] + "%'" 
        if request.POST['TestType'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'Sample' ->> 'TestType' LIKE '%" + request.POST['TestType'] + "%'"
        if request.POST['OrderingMD'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'OrderingMD' LIKE '%" + request.POST['OrderingMD'] + "%'" 
            
        cur.execute(datalistsql)
        datalist = cur.fetchall()
        df = pd.DataFrame(datalist)
        #print(consentsql)
        column_list = ["Id", "報告號碼", "分生號碼", "病歷號", "Diagnosis", "檢測項目", "臨床主治醫師"]  
        df.columns=column_list
        df.to_csv('static/doc/datalist.csv', encoding='utf-8-sig' ,index=False)
        
        SELECTint=len(rows)
        conn.close()
        search={#'ReportNo' : ReportNo,
                #'MPNo' : MPNo,
                #'MRN' : MRN,
                'Diagnosis' : Diagnosis,
                'TestType' : TestType,
                'OrderingMD' : OrderingMD
                } 
        context = {
                'Generight' : Generight,
                'search' : search,
                'right' : right,
                'FuncResult' : SELECTint,
                'rows' : rows
                }
        return render(request, 'PMI.html', context)
    except Exception as e:
        print("发生错误:", e)
        context = {
                'Generight' : Generight,                
                #'search' : search,
                'right' : right,
                'FuncResult' : 'FuncResult'
                }
        return render(request, 'PMI.html', context)

def Biomarker(request):
    try:
        #ReportNo=''
        #MPNo=''
        #MRN=''
        status=''
        score=''
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
        cur = conn.cursor()
        consentsql = 'SELECT * FROM public.reportxml where true '       
        #if request.POST['ReportNo'] != '':
        #    ReportNo = request.POST['ReportNo']
        #    consentsql = consentsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\' '
        #if request.POST['MPNo'] != '':
        #    MPNo = request.POST['MPNo']
        #    consentsql = consentsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\' '
        #if request.POST['MRN'] != '':
        #    MRN = request.POST['MRN']
        #    consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%' "
        if request.POST['status'] != '':
            status = request.POST['status']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'biomarkers' -> 'microsatellite_instability' ->> 'status' LIKE '%" + request.POST['status'] + "%'"
        if request.POST['score'] != '':
            score = request.POST['score']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'biomarkers' -> 'tumor_mutation_burden' ->> 'score' LIKE '%" + request.POST['score'] + "%'" 
        #print(consentsql)
        cur.execute(consentsql)
        rows = cur.fetchall()
        
        datalistsql = "SELECT id, \"ReportNo\",\"MPNo\", \
            resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' as \"MRN\", \
                resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'biomarkers' -> 'microsatellite_instability' ->> 'status' as \"Microsatellite Status\", \
                    resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'biomarkers' -> 'tumor_mutation_burden' ->> 'score' as \"Tumor Mutational Burden score\" \
                        FROM public.reportxml where true "
        #if request.POST['ReportNo'] != '':
        #    datalistsql = datalistsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\''
        #if request.POST['MPNo'] != '':
        #    datalistsql = datalistsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\''
        #if request.POST['MRN'] != '':
        #    datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%'"
        if request.POST['status'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'biomarkers' -> 'microsatellite_instability' ->> 'status' LIKE '%" + request.POST['status'] + "%'"
        if request.POST['score'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'biomarkers' -> 'tumor_mutation_burden' ->> 'score' LIKE '%" + request.POST['score'] + "%'" 
            
        cur.execute(datalistsql)
        datalist = cur.fetchall()
        df = pd.DataFrame(datalist)
        column_list = ["Id", "報告號碼", "分生號碼", "病歷號", "Microsatellite Status", "Tumor Mutational Burden score"]  
        df.columns=column_list
        df.to_csv('static/doc/datalist.csv', encoding='utf-8-sig' ,index=False)
        
        SELECTint=len(rows)
        conn.close()
        search={#'ReportNo' : ReportNo,
                #'MPNo' : MPNo,
                #'MRN' : MRN,
                'status' : status,
                'score' : score
                } 
        context = {
                'Generight' : Generight,
                'search' : search,
                'right' : right,
                'FuncResult' : SELECTint,
                'rows' : rows
                }
        return render(request, 'Biomarker.html', context)
    except:
        context = {
                'Generight' : Generight,
                #'search' : search,
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'Biomarker.html', context)
    
def ShortVariants(request):
    try:
        #ReportNo=''
        #MPNo=''
        #MRN=''
        gene=''
        protein_effect=''
        cds_effect=''
        allele_fraction=''
        functional_effect=''
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
        cur = conn.cursor()
        consentsql = 'SELECT * FROM public.reportxml where true '       
        #if request.POST['ReportNo'] != '':
        #    ReportNo = request.POST['ReportNo']
        #    consentsql = consentsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\' '
        #if request.POST['MPNo'] != '':
        #    MPNo = request.POST['MPNo']
        #    consentsql = consentsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\' '
        #if request.POST['MRN'] != '':
        #    MRN = request.POST['MRN']
        #    consentsql = consentsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%'"
            
        if request.POST['gene'] != '':
            gene = request.POST['gene']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['gene'] + "%'" 
        if request.POST['protein_effect'] != '':
            protein_effect = request.POST['protein_effect']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['protein_effect'] + "%'"
        if request.POST['cds_effect'] != '':
            cds_effect = request.POST['cds_effect']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['cds_effect'] + "%'"        
        if request.POST['allele_fraction'] != '':
            allele_fraction = request.POST['allele_fraction']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['allele_fraction'] + "%'" 
        if request.POST['functional_effect'] != '':
            functional_effect = request.POST['functional_effect']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['functional_effect'] + "%'" 
        #print(consentsql)
        cur.execute(consentsql)
        rows = cur.fetchall()
        '''
        datalistsql = "SELECT id, \"ReportNo\",\"MPNo\", \
            resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' as \"MRN\", \
                resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' as \"short variants\" \
                    FROM public.reportxml where true "
        #if request.POST['ReportNo'] != '':
        #    datalistsql = datalistsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\''
        #if request.POST['MPNo'] != '':
        #    datalistsql = datalistsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\''
        #if request.POST['MRN'] != '':
        #    datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%'"
        
        if request.POST['gene'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['gene'] + "%'" 
        if request.POST['protein_effect'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['protein_effect'] + "%'"
        if request.POST['cds_effect'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['cds_effect'] + "%'"        
        if request.POST['allele_fraction'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['allele_fraction'] + "%'" 
        if request.POST['functional_effect'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'short_variants' ->> 'short_variant' LIKE '%" + request.POST['functional_effect'] + "%'" 
        #print(datalistsql)   
        cur.execute(datalistsql)
        datalist = cur.fetchall()
        df = pd.DataFrame(datalist)

        column_list = ["Id", "報告號碼", "分生號碼", "病歷號", "short variants"]  
        df.columns=column_list
        df.to_csv('static/doc/datalist.csv', encoding='utf-8-sig' ,index=False)
        '''
        SELECTint=len(rows)
        conn.close()
        search={#'ReportNo' : ReportNo,
                #'MPNo' : MPNo,
                #'MRN' : MRN,
                'gene':gene,
                'protein_effect':protein_effect,
                'cds_effect':cds_effect,
                'allele_fraction':allele_fraction,
                'functional_effect':functional_effect
                } 
        context = {
                'Generight' : Generight,
                'search' : search,
                'right' : right,
                'FuncResult' : SELECTint,
                'rows' : rows
                }
        return render(request, 'ShortVariants.html', context)
    except:
        context = {
                'Generight' : Generight,
                #'search' : search,
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'ShortVariants.html', context)

def CopyNumberAlterations(request):
    try:
        #ReportNo=''
        #MPNo=''
        #MRN=''
        gene=''
        type=''
        copy_number=''
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
        cur = conn.cursor()
        consentsql = 'SELECT * FROM public.reportxml where true '       
        #if request.POST['ReportNo'] != '':
        #    ReportNo = request.POST['ReportNo']
        #    consentsql = consentsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\' '
        #if request.POST['MPNo'] != '':
        #    MPNo = request.POST['MPNo']
        #    consentsql = consentsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\' '
        #if request.POST['MRN'] != '':
        #    MRN = request.POST['MRN']
        #    consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%'"
        
        if request.POST['gene'] != '':
            gene = request.POST['gene']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'copy_number_alterations' ->> 'copy_number_alteration' LIKE '%" + request.POST['gene'] + "%'"
        if request.POST['type'] != '':
            type = request.POST['type']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'copy_number_alterations' ->> 'copy_number_alteration' LIKE '%" + request.POST['type'] + "%'"
        if request.POST['copy_number'] != '':
            copy_number = request.POST['copy_number']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'copy_number_alterations' ->> 'copy_number_alteration' LIKE '%" + request.POST['copy_number'] + "%'"
        #print(consentsql)
        cur.execute(consentsql)
        rows = cur.fetchall()
        '''
        datalistsql = "SELECT id, \"ReportNo\",\"MPNo\", \
            resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' as \"MRN\", \
                resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'copy_number_alterations' ->> 'copy_number_alteration' as \"copy number alterations\" \
                    FROM public.reportxml where true "
        #if request.POST['ReportNo'] != '':
        #    datalistsql = datalistsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\''
        #if request.POST['MPNo'] != '':
        #    datalistsql = datalistsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\''
        #if request.POST['MRN'] != '':
        #    datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%'"
        
        if request.POST['gene'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'copy_number_alterations' ->> 'copy_number_alteration' LIKE '%" + request.POST['gene'] + "%'"
        if request.POST['type'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'copy_number_alterations' ->> 'copy_number_alteration' LIKE '%" + request.POST['type'] + "%'"
        if request.POST['copy_number'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'copy_number_alterations' ->> 'copy_number_alteration' LIKE '%" + request.POST['copy_number'] + "%'"
            
        cur.execute(datalistsql)
        datalist = cur.fetchall()
        df = pd.DataFrame(datalist)
        
        column_list = ["Id", "報告號碼", "分生號碼", "病歷號", "copy number alterations"]  
        df.columns=column_list
        df.to_csv('static/doc/datalist.csv', encoding='utf-8-sig' ,index=False)
        '''
        SELECTint=len(rows)
        conn.close()
        search={#'ReportNo' : ReportNo,
                #'MPNo' : MPNo,
                #'MRN' : MRN,
                'gene':gene,
                'type':type,
                'copy_number':copy_number,
                } 
        context = {
                'Generight' : Generight,
                'search' : search,
                'right' : right,
                'FuncResult' : SELECTint,
                'rows' : rows
                }
        return render(request, 'CopyNumberAlterations.html', context)
    except:
        context = {
                'Generight' : Generight,
                #'search' : search,
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'CopyNumberAlterations.html', context)

def Rearrangement(request):
    try:
        #ReportNo=''
        #MPNo=''
        #MRN=''
        description=''
        targeted_gene=''
        other_gene=''
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
        cur = conn.cursor()
        consentsql = 'SELECT * FROM public.reportxml where true '       
        #if request.POST['ReportNo'] != '':
        #    ReportNo = request.POST['ReportNo']
        #    consentsql = consentsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\' '
        #if request.POST['MPNo'] != '':
        #    MPNo = request.POST['MPNo']
        #    consentsql = consentsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\' '
        #if request.POST['MRN'] != '':
        #    MRN = request.POST['MRN']
        #    consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%'"

        if request.POST['description'] != '':
            description = request.POST['description']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'rearrangements' ->> 'rearrangement' LIKE '%" + request.POST['description'] + "%'"
        if request.POST['targeted_gene'] != '':
            targeted_gene = request.POST['targeted_gene']
            consentsql = consentsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'rearrangements' ->> 'rearrangement' LIKE '%" + request.POST['targeted_gene'] + "%'"
        if request.POST['other_gene'] != '':
            other_gene = request.POST['other_gene']
            consentsql = consentsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'rearrangements' ->> 'rearrangement' LIKE '%" + request.POST['other_gene'] + "%'"
        
        cur.execute(consentsql)
        rows = cur.fetchall()
        '''
        datalistsql = "SELECT id, \"ReportNo\",\"MPNo\", \
            resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' as \"MRN\", \
                resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'rearrangements' ->> 'rearrangement' as \"rearrangements\" \
                    FROM public.reportxml where true "
        #if request.POST['ReportNo'] != '':
        #    datalistsql = datalistsql + ' and "ReportNo" = \'' + request.POST['ReportNo'] + '\''
        #if request.POST['MPNo'] != '':
        #    datalistsql = datalistsql + ' and "MPNo" = \'' + request.POST['MPNo'] + '\''
        #if request.POST['MRN'] != '':
        #    datalistsql = datalistsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'FinalReport' -> 'PMI' ->> 'MRN' LIKE '%" + request.POST['MRN'] + "%'"
        
        if request.POST['description'] != '':
            datalistsql = datalistsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'rearrangements' ->> 'rearrangement' LIKE '%" + request.POST['description'] + "%'"
        if request.POST['targeted_gene'] != '':
            datalistsql = datalistsql + " and resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'rearrangements' ->> 'rearrangement' LIKE '%" + request.POST['targeted_gene'] + "%'"
        if request.POST['other_gene'] != '':
            datalistsql = datalistsql + " and  resultsreport -> 'ResultsReport' -> 'ResultsPayload' -> 'variant_report' -> 'rearrangements' ->> 'rearrangement' LIKE '%" + request.POST['other_gene'] + "%'"
            
        cur.execute(datalistsql)
        datalist = cur.fetchall()
        df = pd.DataFrame(datalist)
        #print(consentsql)
        column_list = ["Id", "報告號碼", "分生號碼", "病歷號", "rearrangements"]  
        df.columns=column_list
        df.to_csv('static/doc/datalist.csv', encoding='utf-8-sig' ,index=False)        
        '''
        SELECTint=len(rows)
        conn.close()
        search={#'ReportNo' : ReportNo,
                #'MPNo' : MPNo,
                #'MRN' : MRN,
                'description':description,
                'targeted_gene':targeted_gene,
                'other_gene':other_gene,
                } 
        context = {
                'Generight' : Generight,
                'search' : search,
                'right' : right,
                'FuncResult' : SELECTint,
                'rows' : rows
                }
        return render(request, 'Rearrangement.html', context)
    except:
        context = {
                'Generight' : Generight,
                #'search' : search,
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'Rearrangement.html', context)
'''  
def GeneFinalReportDetails(request):
    try:
        user = request.user
        #print(user.username)
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        #print(Generight) 
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        #print(right)  
        rid = request.GET.get('id')  # 取得 id，如果沒有則為 None
        #print(f"GET id: {rid}")
        short_variants = request.POST.get('short_variants')  # 取得 short_variants，如果沒有則為 None
        #print(type(short_variants))
        #print(f"POST short_variants: {short_variants}")
        # 連接 PostgreSQL
        conn = psycopg2.connect(
            database="vghtpegene",
            user="postgres",
            password="1qaz@WSX3edc",
            host=genepostgresip,
            port=genepostgresport
        )
        cur = conn.cursor()
        consentsql = 'SELECT * FROM public.reportxml WHERE id = \'' + rid + '\';'
        #print(consentsql)
        cur.execute(consentsql)
        rows = cur.fetchall()
        conn.close()
        #print(cur.description)
        #name_index = cur.description.index('resultsreport')
        #print(len(rows[0][1]))
        #print(rows[0][1])
        print(short_variants)
        #dict_result = json.loads(short_variants)
        #print(dict_result)
        print(rows[0][1]['ResultsReport']['ResultsPayload']['variant_report'])
        # 提取報告資料
        #report_data = rows[0][1]


        context = {
                'right' : right,
                'Generight' : Generight,
                'FuncResult' : rid,
                'data' : rows[0]
                }             
        return render(request, 'GeneFinalReportDetails.html', context)
    except:
        context = {
                'right' : right, 
                'Generight' : Generight,
                'FuncResult' : '查無資料'
            } 
        return render(request, 'GeneFinalReportDetails.html', context)
'''    
def GeneFinalReportDetails(request):
    try:
        user = request.user
        Generight = models.Genepermission.objects.filter(user__username__startswith=user.username)
        right = models.Permission.objects.filter(user__username__startswith=user.username)
        rid = request.GET.get('id')  # Get id, None if not present
        short_variants = request.POST.get('short_variants')  # Get short_variants, None if not present

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            database="vghtpegene",
            user="postgres",
            password="1qaz@WSX3edc",
            host=genepostgresip,
            port=genepostgresport
        )
        cur = conn.cursor()
        
        # Fetch the existing record
        consentsql = 'SELECT * FROM public.reportxml WHERE id = \'' + rid + '\';'
        cur.execute(consentsql)
        rows = cur.fetchall()
        
        # Modify the data: replace variant_report with short_variants
        if short_variants:
            # Assuming short_variants is JSON string, convert it if needed
            report_data = rows[0][1]  # Get the JSON data
            report_data['ResultsReport']['ResultsPayload']['variant_report'] = json.loads(short_variants) if isinstance(short_variants, str) else short_variants
            
            # Update the database
            update_sql = """
                UPDATE public.reportxml 
                SET resultsreport = %s 
                WHERE id = %s;
            """
            cur.execute(update_sql, (json.dumps(report_data), rid))
            conn.commit()  # Commit the transaction
            
            print('UPDATE')

        conn.close()

        context = {
            'right': right,
            'Generight': Generight,
            'FuncResult': rid,
            'data': rows[0]
        }             
        return render(request, 'GeneFinalReportDetails.html', context)
    
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        context = {
            'right': right, 
            'Generight': Generight,
            'FuncResult': '查無資料'
        } 
        return render(request, 'GeneFinalReportDetails.html', context)


def GeneVariantReportDetails(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    #print(right)       
    try:
        rid=request.GET['id']
        #print(rid)
        conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
        cur = conn.cursor()
        consentsql = 'SELECT * FROM public.reportxml WHERE id = \'' + rid + '\';'
        #print(consentsql)
        cur.execute(consentsql)
        rows = cur.fetchall()
        conn.close()
        #print(rows)
        context = {
                'right' : right,
                'FuncResult' : rid,
                'data' : rows[0]
                }             
        return render(request, 'GeneVariantReportDetails.html', context)
    except:
        context = {
                'right' : right,                
                'FuncResult' : '查無資料'
            } 
        return render(request, 'GeneVariantReportDetails.html', context)
    
def ambulance(request):
    try:
        user = request.user
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'ambulance.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                }
        return render(request, 'ambulance.html', context)

def Phenopacket(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.PhenopacketCURD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data,
                'phenotypic_features_count' : len(data['phenotypic_features']),
                'measurements_count' : len(data['measurements']),
                'biosamples_count' : len(data['biosamples']),
                'genomic_interpretations_count' : len(data['interpretations'][0]['diagnosis']['genomic_interpretations'])
                }             
        return render(request, 'Phenopacket.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Phenopacket.html', context)

def Biosample(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)

    try:
        
        Result,data = Function.BiosampleCURD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Biosample.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Biosample.html', context)
    
def Individual(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.IndividualCURD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Individual.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Individual.html', context)

def Interpretation(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        
        Result,data = Function.InterpretationCURD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Interpretation.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Interpretation.html', context)

def ClinvarVariant(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        
        Result,data = Function.ClinvarVariantCURD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'ClinvarVariant.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'ClinvarVariant.html', context)

def Patient(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        fhirip=models.fhirip.objects.all()
        #print(fhirip)            
        Result,data = Function.PatientCURD(request)
        context = {
                'right' : right,
                'fhirip' : fhirip,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Patient.html', context)
    except:
        context = {
                'right' : right,
                'fhirip' : fhirip,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Patient.html', context)

def Organization(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.OrganizationCURD(request)

        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Organization.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Organization.html', context)

def Practitioner(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.PractitionerCURD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Practitioner.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Practitioner.html', context)
        
def PatientUpload(request):
    try:
        user = request.user
        #print(user.username)
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Genedataall=models.Genedata.objects.all().order_by('-id')
        #df = pd.read_excel(uploadedFile)
        try:
            inlineRadioOptions = request.POST["inlineRadioOptions"]
        except:
            inlineRadioOptions = ''
        
        if request.POST["fileTitle"] !='':
            fileTitle = request.POST["fileTitle"]
        else:
            fileTitle = '' 
        try:
            uploadedFile = request.FILES["uploadedFile"]
        except:
            uploadedFile = ''
        
        Genedata = models.Genedata(
            inlineRadioOptions=inlineRadioOptions,
            fileTitle = fileTitle,
            uploadedFile = uploadedFile
        )
        Genedata.save() 

        #print(os.getcwd())
        
        context = {
                'Generight' : Generight,
                'right' : right,
                'Genedata' : Genedataall,
                'FuncResult' : 'Up finsh'
                }
        return render(request, 'PatientUpload.html', context)
  
    except:
        context = {
                'Generight' : Generight,
                'right' : right,
                'Genedata' : Genedataall,
                'FuncResult' : 'Up Fail'
                }
        return render(request, 'PatientUpload.html' , context)

def Userright(request):
    try:
        user = request.user
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Userrightall=models.Userright.objects.all().order_by('-id')
        #conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
        #cur = conn.cursor()
        #print('Opened database successfully')
    
        if request.POST["fileTitle"] !='':
            fileTitle = request.POST["fileTitle"]
        else:
            fileTitle = '' 
        try:
            uploadedFile = request.FILES["uploadedFile"]
        except:
            uploadedFile = ''
        # Saving the information in the database
        Userright = models.Userright(
            fileTitle = fileTitle,
            uploadedFile = uploadedFile,
        )
        Userright.save()        
        #print(uploadedFile)
        #documents = models.Document.objects.all()        
        context = {
                'Generight' : Generight,
                'right' : right,
                'Userright' : Userrightall,
                'FuncResult' : 'Up finsh'
                }
        return render(request, 'UsrUpload.html', context)
    except:
        context = {
                'Generight' : Generight,
                'right' : right,
                'Userright' : Userrightall,
                'FuncResult' : 'Up Fail'
                }
        return render(request, 'UsrUpload.html' , context)

def UpGeneZip(request):
    try:
        user = request.user
        Generight = models.Genepermission.objects.filter(user__username__startswith=user.username)
        right = models.Permission.objects.filter(user__username__startswith=user.username)
        Genezipall = models.Genezip.objects.all().order_by('-id')
        root = os.getcwd()
        if request.POST["fileTitle"] != '' and request.FILES["uploadedFile"] != '':
            fileTitle = request.POST["fileTitle"]
            uploadedFile = request.FILES["uploadedFile"]


            # 保存上传文件信息到数据库
            Genezip = models.Genezip(
                fileTitle=fileTitle,
                uploadedFile=uploadedFile,
            )
            Genezip.save()
            #print(Genezippk.pk)
            # 数据库连接信息
            conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
            cur = conn.cursor()

            # 獲取當前根目錄
            root = os.getcwd()

            # 確保 media/Genezip 目錄存在
            media_genezip_dir = os.path.join(root, 'media', 'Genezip')
            os.makedirs(media_genezip_dir, exist_ok=True)

            # 清理文件名，確保不含特殊字符
            uploaded_filename = uploadedFile.name.replace('(', '').replace(')', '')

            # 定義原始文件存放路徑
            source_path = os.path.join(media_genezip_dir, uploaded_filename)

            # 先將上傳的檔案寫入磁碟
            with open(source_path, 'wb+') as destination_file:
                for chunk in uploadedFile.chunks():
                    destination_file.write(chunk)

            # 確保 static/doc 目錄存在
            static_doc_dir = os.path.join(root, 'static', 'doc')
            os.makedirs(static_doc_dir, exist_ok=True)

            # 定義最終的目的路徑
            destination_path = os.path.join(static_doc_dir, uploaded_filename)

            # 刪除舊檔案（如果存在）
            if os.path.exists(destination_path):
                os.remove(destination_path)


            # 複製文件到最終目的地
            dest = shutil.copyfile(source_path, destination_path)
            #shutil.copyfile(source_path, destination_path)
            '''
            filename = os.path.join(root, 'media', 'Genezip', str(uploadedFile).replace('(', '').replace(')', ''))
            source = filename
            destination = os.path.join(root, 'static', 'doc', str(uploadedFile))

            # 删除已有的目标文件
            try:
                os.remove(destination)
                #print("文件删除成功")
            except FileNotFoundError:
                print("文件不存在")
            except PermissionError:
                print("没有权限删除文件")
            except Exception as e:
                print("发生错误:", e)

            # 复制文件到目标位置
            dest = shutil.copyfile(source, destination)
            '''

            # 解压缩文件
            try:
                destination_dir = os.path.join(root, 'static', 'doc', str(uploadedFile).replace('.zip', ''))
                with zipfile.ZipFile(dest, "r") as zip_ref:
                    zip_ref.extractall(destination_dir)
            except zipfile.BadZipFile as e:
                print("错误: ZIP 文件无效 -", e)
            except FileNotFoundError as e:
                print("错误: 文件未找到 -", e)
            except Exception as e:
                print("错误:", e)

            #print(os.listdir(destination_dir))
            #print(os.getcwd())

            # 处理解压后的文件目录
            dirpath = 'ACTOnco V1'
            if os.path.isdir(dirpath):
                print("目录存在。")
            else:
                #print("目录不存在。")
                os.chdir(os.path.join(destination_dir, str(uploadedFile).replace('.zip', '')))
                #print(os.getcwd())

            genepath = os.path.join(root, 'static', 'doc')
            process_gene_files(dirpath, conn, cur, genepath)

            context = {
                'Generight': Generight,
                'right': right,
                'Genezip': Genezipall,
                'FuncResult': 'Upload finish'
            }
            return render(request, 'Geneload.html', context)
        else:
            context = {
                'Generight': Generight,
                'right': right,
                'Genezip': Genezipall,
                'FuncResult': 'No file upload'
            }
            return render(request, 'Geneload.html', context)
    except Exception as e:
        print("发生错误:", e)
        context = {
            'Generight': Generight,
            'right': right,
            'Genezip': Genezipall,
            'FuncResult': 'No file upload'
        }
        return render(request, 'Geneload.html', context)


def process_gene_files(dirpath, conn, cur, genepath):
    dirpath = 'ACTOnco V1'
    gene2cbio.ACTGV12xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    #print('ACTOnco V1')

    dirpath = 'ACTOnco V2'
    gene2cbio.ACTGV22xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    #print('ACTOnco V2')

    dirpath = 'Guardant360'
    gene2cbio.Guardant3602xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    #print('Guardant360')

    dirpath = 'Foundation One'
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    #print('Foundation One')

    dirpath = 'Archer Lung'
    gene2cbio.pdf2floder(dirpath)
    gene2cbio.Archer2xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    #print('Archer Lung')

    dirpath = 'Archer Sarcoma'
    gene2cbio.pdf2floder(dirpath)
    gene2cbio.Archer2xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    #print('Archer')

    dirpath = 'BRCA Assay'
    gene2cbio.pdf2floder(dirpath)
    gene2cbio.BRCAAssay2xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    #print('BRCA')

    dirpath = 'Focus Assay'
    gene2cbio.pdf2floder(dirpath)
    gene2cbio.FocusAssay2xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    print('Focus')

    dirpath = 'Myeloid Assay'
    gene2cbio.pdf2floder(dirpath)
    gene2cbio.MyeloidAssay2xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    #print('Myeloid')

    dirpath = 'Tumor Mutation Load Assay'
    gene2cbio.pdf2floder(dirpath)
    gene2cbio.MutationLoadAssay2xml(dirpath)
    gene2cbio.xmlisql(dirpath, conn, cur)
    gene2cbio.pdf2dir(dirpath, genepath)
    gene2cbio.sqldelduplicate(conn, cur)
    #print('Tumor')
    
def UpdateMeta(request):
    try:
        user = request.user
        #print(user.username)
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Metaxlsxall=models.Metaxlsx.objects.all().order_by('-id')
        #df = pd.read_excel(uploadedFile)
        #print(method)
        if request.POST["fileTitle"] !='' and request.FILES["uploadedFile"]!='':
            if request.POST["fileTitle"] !='':
                fileTitle = request.POST["fileTitle"]
            else:
                fileTitle = '' 
            try:
                uploadedFile = request.FILES["uploadedFile"]
            except:
                uploadedFile = ''
            # Saving the information in the database
            Metaxlsx = models.Metaxlsx(
                fileTitle = fileTitle,
                uploadedFile = uploadedFile,
            )            
            Metaxlsx.save()        
            #documents = models.Document.objects.all()        
        context = {
                'Generight' : Generight,
                'right' : right,
                'Metaxlsx' : Metaxlsxall,
                'FuncResult' : 'Upload finsh'
                }
        return render(request, 'MetaUpload.html', context)
    except Exception as e:
        print("发生错误:", e)
        context = {
                'Generight' : Generight,
                'right' : right,
                'Metaxlsx' : Metaxlsxall,
                'FuncResult' : e
                }
        return render(request, 'MetaUpload.html' , context)
    


def Metaxlsx(request):    
    try:
        user = request.user
        #print(user.username)
        Generight=models.Genepermission.objects.filter(user__username__startswith=user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        rid=request.GET["id"]
        #print(rid)
        Metaxlsx=models.Metaxlsx.objects.filter(id=rid)
        for meta in Metaxlsx:
            print(meta.uploadedFile)
            #for dirname in os.listdir(os.getcwd()+'/media/'):
                #print(dirname)\media\Metaxlsx
            dfpath=os.getcwd().replace('\\','/')+'/media/'+str(meta.uploadedFile)
            #dfpath='/server/media/'+str(meta.uploadedFile)#VM用
            #print(dfpath)

            conn = psycopg2.connect(database="vghtpegene", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
            #print('Opened database successfully')
            cur = conn.cursor()
            
            df = pd.read_excel(dfpath)
            #print(df)
            df = df.assign(update='')
            #print("Columns")
            #print(df.columns)
            for i in range(len(df)):
                #if i % 10 ==0:11111
                    #print(i)
                #print(df['分生號碼'][i] + ' ' + df['報告號碼'][i])
                try:
                    ReportNo=df['報告號碼'][i]
                    MPNo=df['分生號碼'][i]
                    query= "SELECT id, resultsreport, \"ReportNo\", \"MPNo\" FROM public.reportxml where \"ReportNo\" = '"+df['報告號碼'][i]+"' and \"MPNo\" = '"+df['分生號碼'][i]+"';"
                    #print(query)
                    df1 = pd.read_sql(query, conn)
                    #print(df1)
                    for j in range(len(df1)):
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['PMI']['ReportId']=str(df['報告號碼'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['PMI']['MRN']=str(df['病歷號'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['PMI']['FullName']=str(df['病患姓名'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis']=str(df['Diagnosis'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['PMI']['OrderingMD']=str(df['臨床主治醫師'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['PMI']['Pathologist']=str(df['病理醫師'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['PMI']['ReceivedDate']=str(df['報告日期'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['PMI']['TumorType']=str(df['Tumor type'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample']['BlockId']=str(df['蠟塊號'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample']['TestType']=str(df['檢測項目'][i])
                            df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample']['SpecFormat']=str(df['檢體別'][i])
                            #print(df.columns)
                           
                            try:
                                #print(int(str(df['Tumor purity %'][i]).replace('%','')))
                                df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample']['TumorPurity']=str(df['Tumor purity %'][i]).replace('%','')
                            except:
                                df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample']['TumorPurity']='NA'
                            
                            try:
                                df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample']['SpecimenLocation']=str(df['標本組織部位來源'][i])
                            except:
                                df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample']['SpecimenLocation']='NA'
                            #print(df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample'])
                            sql='UPDATE public.reportxml SET resultsreport = \'' + json.dumps(df1['resultsreport'][j], cls=NpEncoder) + '\' WHERE id = ' + str(df1['id'][j]) +';'
                            #if i ==1:
                            #print(df1['resultsreport'][j]['ResultsReport']['ResultsPayload']['FinalReport']['Sample']['TumorPurity'])
                            datajson=json.dumps(df1['resultsreport'][j], cls=NpEncoder)
                            #print(type(datajson))
                            with open('media/json/'+ReportNo+'_('+MPNo+').json', 'w') as f:
                                f.write(
                                    )
                            #print(sql)
                            cur.execute(sql)
                            #print(cur.rowcount)
                            if cur.rowcount > -1:
                                df['update'][i]='OK'
                            conn.commit()
                #except:
                except Exception as e:
                    df['update'][i]=e
            df.to_excel(dfpath,index=False)
        context = {
                'Generight' : Generight,
                'right' : right,
                'Metaxlsx' : Metaxlsx,
                'FuncResult' : 'Updata finsh'
                }
        return render(request, 'Update.html', context)
    except Exception as e:
        print("发生错误:", e)
        context = {
                'Generight' : Generight,
                'right' : right,
                'Metaxlsx' : '',
                'FuncResult' :  e
                }
        return render(request, 'Update.html' , context)

def DataUpload(request):
    try:
        if request.method == "POST":
            method=request.POST['method']
            fileTitle = request.POST["fileTitle"]
            uploadedFile = request.FILES["uploadedFile"]
            df = pd.read_excel(uploadedFile)
            document = models.Document(
                title = fileTitle,
                uploadedFile = uploadedFile
            )
            document.save()
        status_codelist=[]
        diagnosticslist=[]
        for i in range(len(df)):
            try:
                Result,data,status_code,diagnostics = Function.PatientUpload(df.iloc[i],method)
                status_codelist.append(status_code)
                diagnosticslist.append(diagnostics)
                context = {
                        'FuncResult' : Result,
                        'data' : data,
                        }
            except:
                context = {
                        'FuncResult' : 'Function'
                        } 
        errordict = {
            "status_code": status_codelist,
            "diagnosticslist": diagnosticslist
            }
        errordf = pd.DataFrame(errordict)
        data=df.merge(errordf, how='outer', left_index=True, right_index=True)
        context = {
                'FuncResult' : Result,
                'data' : data,
                }
        return render(request, 'DataUpload.html', context)
    except:
        context = {
                'FuncResult' : 'FuncResult'
                }
        return render(request, 'DataUpload.html', context )

def AllergyIntolerance(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.AllergyIntoleranceCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'AllergyIntolerance.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'AllergyIntolerance.html', context)

def FamilyMemberHistory(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.FamilyMemberHistoryCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'FamilyMemberHistory.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'FamilyMemberHistory.html', context)

def Encounter(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.EncounterCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Encounter.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Encounter.html', context)
    
def CarePlan(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.CarePlanCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'CarePlan.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'CarePlan.html', context)

def DiagnosticReportNursing(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.DiagnosticReportNursingCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'DiagnosticReportNursing.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'DiagnosticReportNursing.html', context)

def DiagnosticReportRadiationTreatment(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.DiagnosticReportRadiationTreatmentCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'DiagnosticReportRadiationTreatment.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'DiagnosticReportRadiationTreatment.html', context)
    
def DiagnosticReportPathologyReport(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.DiagnosticReportPathologyReportCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'DiagnosticReportPathologyReport.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'DiagnosticReportPathologyReport.html', context)

def Procedure(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.ProcedureCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Procedure.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Procedure.html', context)
    
def ServiceRequest(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.ServiceRequestCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'ServiceRequest.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'ServiceRequest.html', context)
    
def ConditionStage(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.ConditionStageCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'ConditionStage.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'ConditionStage.html', context)

def ImagingStudy(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.ImagingStudyCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'ImagingStudy.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'ImagingStudy.html', context)

def Endpoint(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.EndpointCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Endpoint.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Endpoint.html', context)

def Medication(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.MedicationCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Medication.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Medication.html', context)

def MedicationRequest(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.MedicationRequestCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'MedicationRequest.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'MedicationRequest.html', context)    

def MedicationAdministration(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.MedicationAdministrationCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'MedicationAdministration.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'MedicationAdministration.html', context)

def Immunization(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.ImmunizationCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Immunization.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
                } 
        return render(request, 'Immunization.html', context)
    
def dbSNP(request):
    try:
        if 'Alleles' in request.POST:
            Alleles = request.POST['Alleles']
            dbSNP = request.POST['dbSNP']
            #print(Alleles)
            context=Function.post_dbSNP(Alleles,dbSNP)
            #print(context)
        elif 'Alleles' in request.GET:
            Alleles = request.GET['Alleles']
            dbSNP = request.GET['dbSNP']
            #print(Alleles)
            context=Function.post_dbSNP(Alleles,dbSNP)
        else:
            context=None
        return render(request, 'geneticsdbSNP.html', context)
    except:
        return render(request, 'geneticsdbSNP.html', context)

def getRisk(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)    
        riskrlue = request.GET['risk']
        #riskrlue='Alc_risk'
        #print(riskrlue)

        risksdf=riskdf[riskdf['risk']==riskrlue]
        #print(risksdf)
        #risksdict = risksdf.to_dict()
        risksdict = risksdf.to_dict('records')
        context = {
                'right' : right,
                'riskrlue' : riskrlue,
                'risks' : risksdict
                }
        return render(request,'geneticsRisk.html', context)
    except:
        return render(request,'geneticsRisk.html', context)

def Gene(request):
    try:
        user = request.user
        #print(user.username)
        right=models.Permission.objects.filter(user__username__startswith=user.username)
        Result,data = Function.GeneCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'geneticsVghtc.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
            } 
        return render(request, 'geneticsVghtc.html', context)

def MolecularSequence(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.MolecularSequenceCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'MolecularSequence.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
            } 
        return render(request, 'MolecularSequence.html', context)

def ObservationGenetics(request):
    user = request.user
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.ObservationGeneticsCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'ObservationGenetics.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
            } 
        return render(request, 'ObservationGenetics.html', context)

def ObservationImaging(request):
    user = request.user
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data = Function.ObservationImagingCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'ObservationImaging.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
            } 
        return render(request, 'ObservationImaging.html', context)

def Referral(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    try:
        Result,data,prtj,ohrtj,ihrtj,crtj,odrtj,idrtj = Function.ReferralCRUD(request)
        context = {
                'right' : right,
                'FuncResult' : Result,
                'data' : data,
                'prtj' : prtj,
                'ohrtj' : ohrtj,
                'ihrtj' : ihrtj,
                'crtj' : crtj,
                'odrtj' : odrtj,
                'idrtj' : idrtj
                }             
        return render(request, 'Referral.html', context)
    except:
        context = {
                'right' : right,
                'FuncResult' : 'Function'
            } 
        return render(request, 'Referral.html', context)

def patient_medical_records(request):
    
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    #print(right)   
    fhirip=models.fhirip.objects.all()
    try:
        Result,data = Function.patient_medical_recordsCRUD(request)
        context = {
                'fhirip' : fhirip,
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'patient_medical_records.html', context)
    except:
        context = {
                'right' : right,
                'fhirip' : fhirip,
                'FuncResult' : '查無資料'
            } 
        return render(request, 'patient_medical_records.html', context)
@csrf_exempt    
def DischargeSummaryDetails(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    #print(right)
    fhirip=models.fhirip.objects.all()
    try:
        fhiripSelect=request.GET['fhir']
    except:
        fhiripSelect=''
    try:
        DischargeSummaryId=request.GET['id']
    except:
        DischargeSummaryId=''
    #print(fhiripSelect)
    #print(DischargeSummaryId)
    #print(fhiripSelect+'Composition/'+DischargeSummaryId)
        
    try:
        url = fhiripSelect+'Composition/'+DischargeSummaryId
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        resultjson=json.loads(response.text)
        #print(resultjson)
        context = {
                'fhiripSelect' : fhiripSelect,
                'fhirip' : fhirip,
                'right' : right,
                'FuncResult' : DischargeSummaryId,
                'data' : resultjson
                }             
        return render(request, 'DischargeSummaryDetails.html', context)
    except:
        context = {
                'fhiripSelect' : fhiripSelect,
                'fhirip' : fhirip,
                'right' : right,                
                'FuncResult' : '查無資料'
            } 
        return render(request, 'DischargeSummaryDetails.html', context)

@csrf_exempt    
def tpoorf(request):
    Verificationurl='https://tproof-dev.twcc.ai/api/v1/tproof/forensics'
    Verification={
      "apikey": "",
      "tokenId": ""
    }    
    headers = {'Content-Type': 'application/json'}
    try:
        tpoorf=request.GET['chain']
        tpoorflist=tpoorf.split(",")
        apikey=tpoorflist[0]
        tokenId=tpoorflist[1]
        Verification['apikey']=apikey
        Verification['tokenId']=tokenId
        payload = json.dumps(Verification)
        #print(payload)
        response = requests.request("POST", Verificationurl, headers=headers, data=payload)
        resultjson=json.loads(response.text)
        #print(response.text)
        context = {
            'data' : resultjson,
            }
        return render(request, 'tpoorf.html', context)
    except:
        context = {} 
        return render(request, 'tpoorf.html', context)

def working(request):
    html = '<h1> working </h1>'
    return HttpResponse(html, status=200)

@csrf_exempt    
def logging(request):
    user = request.user
    right=models.Permission.objects.filter(user__username__startswith=user.username)
  
    try:
        method=request.POST['method']
    except:
        method=''
    try:
        formip=request.POST['formip']
    except:
        formip=''
    try:
        operationdate=request.POST['operationdate']
    except:
        operationdate=''    
    #print(formip,method,operationdate)
    
    conn = psycopg2.connect(database="consent", user="postgres", password="1qaz@WSX3edc", host=genepostgresip, port=genepostgresport)
    cur = conn.cursor()  
    sqlstring =  "SELECT * FROM public.log WHERE method = '" + method + "'"
    if formip != '':
        sqlstring = sqlstring + " AND ip_addr = '" + formip + "'"
    if operationdate != '':
        sqlstring = sqlstring + " AND datetime::date = '" + operationdate + "'"
    sqlstring=sqlstring + " ORDER BY datetime DESC limit 2000;"
    cur.execute(sqlstring)
    rows = cur.fetchall()
    #for row in rows:
        #print(row)
    conn.close()
    context = {
        'right' : right,
        'data' : rows,
        'method' : method,
        'formip' : formip,
        'operationdate' : operationdate
        }                 
    return render(request, 'logging.html', context)

@csrf_exempt    
def DischargeSummary(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    #print(right)
    fhirip=models.fhirip.objects.all()
    try:
        fhiripSelect=request.POST['fhirip']
    except:
        fhiripSelect=''
    try:
        Result,data = Function.DischargeSummaryCRUD(request)
        context = {
                'fhiripSelect' : fhiripSelect,
                'fhirip' : fhirip,
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'DischargeSummary.html', context)
    except:
        context = {
                'fhiripSelect' : fhiripSelect,
                'fhirip' : fhirip,
                'right' : right,                
                'FuncResult' : '查無資料'
            } 
        return render(request, 'DischargeSummary.html', context)
    
@csrf_exempt
def VisitNote(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    #print(right)
    fhirip=models.fhirip.objects.all()
    try:
        fhiripSelect=request.POST['fhirip']
    except:
        fhiripSelect=''
    try:
        Result,data = Function.VisitNoteCRUD(request)
        context = {
                'fhiripSelect' : fhiripSelect,
                'fhirip' : fhirip,
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'VisitNote.html', context)
    except:
        context = {
                'fhiripSelect' : fhiripSelect,
                'fhirip' : fhirip,
                'right' : right,                
                'FuncResult' : '查無資料'
            } 
        return render(request, 'VisitNote.html', context)

@csrf_exempt
def Consent(request):
    user = request.user
    #print(user.username)
    right=models.Permission.objects.filter(user__username__startswith=user.username)
    #print(right)
    fhirip=models.fhirip.objects.all()
    try:
        fhiripSelect=request.POST['fhirip']
    except:
        fhiripSelect=''
    try:
        Result,data = Function.ConsentCRUD(request)
        context = {
                'fhiripSelect' : fhiripSelect,
                'fhirip' : fhirip,
                'right' : right,
                'FuncResult' : Result,
                'data' : data
                }             
        return render(request, 'Consent.html', context)
    except:
        context = {
                'fhiripSelect' : fhiripSelect,
                'fhirip' : fhirip,
                'right' : right,                
                'FuncResult' : '查無資料'
            } 
        return render(request, 'Consent.html', context)