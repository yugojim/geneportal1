from django.contrib import admin
from django.urls import include, path ,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve 
app_name = 'sdlc'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('Patient/', views.Patient, name='Patient'),
    path('Practitioner/', views.Practitioner, name='Practitioner'),
    path('Organization/', views.Organization, name='Organization'),
    path('AllergyIntolerance/', views.AllergyIntolerance, name='AllergyIntolerance'),
    path('FamilyMemberHistory/', views.FamilyMemberHistory, name='FamilyMemberHistory'),
    path('Immunization/', views.Immunization, name='Immunization'),
    path('Encounter/', views.Encounter, name='Encounter'),
    path('CarePlan/', views.CarePlan, name='CarePlan'),
    path('DiagnosticReportNursing/', views.DiagnosticReportNursing, name='DiagnosticReportNursing'),
    path('Referral/', views.Referral, name='Referral'),
    path('ConditionStage/', views.ConditionStage, name='ConditionStage'),
    path('Consent/', views.Consent, name='Consent'),
    path('DiagnosticReportRadiationTreatment/', views.DiagnosticReportRadiationTreatment, name='DiagnosticReportRadiationTreatment'),
    path('DiagnosticReportPathologyReport/', views.DiagnosticReportPathologyReport, name='DiagnosticReportPathologyReport'),
    path('Procedure/', views.Procedure, name='Procedure'),
    path('ServiceRequest/', views.ServiceRequest, name='ServiceRequest'),
    path('MolecularSequence/', views.MolecularSequence, name='MolecularSequence'),
    path('ObservationGenetics/', views.ObservationGenetics, name='ObservationGenetics'),
    path('Gene/', views.Gene, name='Gene'),
    path('dbSNP/', views.dbSNP, name='dbSNP'),
    path('risk/', views.getRisk, name='getRisk'),
    path('ImagingStudy/', views.ImagingStudy, name='ImagingStudy'),
    path('Endpoint/', views.Endpoint, name='Endpoint'),
    path('Medication/', views.Medication, name='Medication'),
    path('MedicationRequest/', views.MedicationRequest, name='MedicationRequest'),
    path('MedicationAdministration/', views.MedicationAdministration, name='MedicationAdministration'),
    path('ambulance/', views.ambulance, name='ambulance'),
    path('Phenopacket/', views.Phenopacket, name='Phenopacket'),
    path('Individual/', views.Individual, name='Individual'),
    path('Biosample/', views.Biosample, name='Biosample'),
    path('Interpretation/', views.Interpretation, name='Interpretation'),
    path('ClinvarVariant/', views.ClinvarVariant, name='ClinvarVariant'),
    path('ObservationImaging/', views.ObservationImaging, name='ObservationImaging'),
    #path('linebot', views.linebot, name='linebot'),
    
    path('GeneReport/', views.GeneReport, name='GeneReport'),
    path('PMI/', views.PMI, name='PMI'),
    path('Biomarker/', views.Biomarker, name='Biomarker'),
    path('ShortVariants/', views.ShortVariants, name='ShortVariants'),
    path('CopyNumberAlterations/', views.CopyNumberAlterations, name='CopyNumberAlterations'),
    path('Rearrangement/', views.Rearrangement, name='Rearrangement'),
    
    path('GeneFinalReportDetails/', views.GeneFinalReportDetails, name='GeneFinalReportDetails'),
    path('GeneVariantReportDetails/', views.GeneVariantReportDetails, name='GeneVariantReportDetails'),
    path('convert/', views.convert, name='convert'),
    
    path('working', views.working, name='working'),
    path('DischargeSummary', views.DischargeSummary, name='DischargeSummary'),
    path('VisitNote', views.VisitNote, name='VisitNote'),
    path('DischargeSummaryDetails', views.DischargeSummaryDetails, name='DischargeSummaryDetails'),
    path('tpoorf', views.tpoorf, name='tpoorf'),
    path('logging', views.logging, name='logging'),
    path('patient_medical_records', views.patient_medical_records, name='patient_medical_records'),
    
    path('PatientUpload/', views.PatientUpload, name='PatientUpload'),
    path('Metaxlsx/', views.Metaxlsx, name='Metaxlsx'),
    path('UpGeneZip/', views.UpGeneZip, name='UpGeneZip'),
    path('UpdateMeta/', views.UpdateMeta, name='UpdateMeta'),
    path('Userright/', views.Userright, name='Userright'),
    path('DataUpload/', views.DataUpload, name='DataUpload'),
        
    path('admin/',admin.site.urls),
    path('auth/', views.auth, name='auth'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)