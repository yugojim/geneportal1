# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:33:36 2022

@author: yugojim
"""
from django.db import models
from django.contrib.auth.models import User

class Metaxlsx(models.Model):
    fileTitle = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to="Metaxlsx/")
    status = models.CharField(max_length=200)
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    
class Resourcejson(models.Model):
    uploadedFile = models.FileField(upload_to="Resourcejson/")
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    
class Genezip(models.Model):
    fileTitle = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to="Genezip/")
    status = models.CharField(max_length=200)
    dateTimeOfUpload = models.DateTimeField(auto_now=True)

class Userright(models.Model):
    fileTitle = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to="Userright/")
    status = models.CharField(max_length=200)
    dateTimeOfUpload = models.DateTimeField(auto_now=True)

class Genedata(models.Model):
    inlineRadioOptions= models.CharField(max_length=200)
    fileTitle = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to="UploadedFiles/")
    status = models.CharField(max_length=200)
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    '''
    def __str__(self):
        #return self.user 
        return f'{self.id} {self.fileTitle} {self.uploadedFile} \
             {self.dateTimeOfUpload}'
    '''         
class Genepermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 20)
    OrderingMD=models.TextField()
    MRN=models.TextField()
    pmi=models.BooleanField()
    specimen=models.BooleanField()
    biomarker=models.BooleanField()
    rearrangements=models.BooleanField()
    GenomicFindings=models.BooleanField()
    VariantProperties=models.BooleanField()
    Trials=models.BooleanField()
    reportProperties=models.BooleanField()
    copy_number_alterations=models.BooleanField()
    short_variants=models.BooleanField()
    cbioportal=models.BooleanField()
    cbioportal1=models.BooleanField()
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
    #def __str__(self):
        #return self.User
    '''
        return f'{self.User} OrderingMD {self.OrderingMD}\
            MRN {self.MRN}  pmi {self.pmi} specimen{self.specimen}\
                biomarker{self.biomarker} rearrangements{self.rearrangements} GenomicFindings {self.GenomicFindings}\
                    VariantProperties {self.VariantProperties} Trials {self.Trials} reportProperties {self.reportProperties}\
                        copy_number_alterations {self.copy_number_alterations} short_variants {self.short_variants}'
                        #修改時間{self.dateTimeOfUpload} {self.title} '
                        '''
class Permission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 20)
    gene=models.BooleanField()
    patient=models.BooleanField()
    emergency=models.BooleanField()
    outpatient=models.BooleanField()
    inpatient=models.BooleanField()
    medication=models.BooleanField()
    report=models.BooleanField()
    administrative=models.BooleanField()
    up=models.BooleanField()
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
    '''
    def __str__(self):
        #return self.user 
        return f'{self.id} {self.user} {self.title} 基因資料{self.gene}\
            病人資料{self.patient} 急診{self.emergency} 門診{self.outpatient} 住診{self.inpatient}\
                用藥{self.medication} 報告{self.report} 行政{self.administrative} 上傳{self.up}\
                    修改時間{self.dateTimeOfUpload}'
                    '''
                    
class fhirip(models.Model):
    location = models.CharField(max_length = 50)
    ip = models.CharField(max_length = 50)
    token = models.CharField(max_length = 200)
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
    '''
    def __str__(self):
        #return self.user 
        return f'{self.id} {self.location} {self.ip} \
             {self.token} 修改時間{self.dateTimeOfUpload}'
             '''