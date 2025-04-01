# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 10:27:46 2023

@author: 11107045
"""
import os
import glob
import zipfile
import PyPDF2

def FocusAssay(pdfpath):
    ### creating a pdf reader object Focus Assay ###
    #dirlist=glob.glob('F22100_S111-97911*')
    dirlist=glob.glob(pdfpath)
    for dirpath in dirlist:
        try:    
            ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
            #filepathlist =glob.glob(os.path.join(dirpath, "*.xml"))
            filepathlist =glob.glob(os.path.join(dirpath, "S*).pdf"))
            #print(filepathlist)        
            for filename in filepathlist:
                print(filename)
                reader = PyPDF2.PdfReader(filename)
                #text_file = open("Output.txt", "w", encoding="utf-8")
                text=[]
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                    #text_file.write(reader.pages[i].extract_text())
                #text_file.close()
                #OTHER DETECTED VARIANTS
                short_variants = []            
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = []
                
                for i in range(len(text)):
                    
                    #short variants                
                    if text[i].find('OTHER DETECTED VARIANTS') > -1:
                        print('\nDETECTED VARIANTS')
                        start = text[i].find('Frequency  Coverage')
                        end = text[i].find('Note:')
                        short_variants.extend(text[i][start+22:end-5].split(' \n'))
                        #print(len(text[i][start+22:end-5].split(' \n')))
                        print(text[i][start+22:end-5].split(' \n'))
                        
                    #rearrangement
                    if text[i].find('Gene Fusions (RNA)') > -1: 
                        print('\nFusions')
                        print(text[i])
                        #start = text[i].find('Transcript ID ')
                        #end = text[i].find('- Immune')
                        #print(text[i][start+16:end-5].split(' \n'))
                        #rearrangement.extend(text[i][start+16:end-5].split(' \n'))
                        #print(len(text[i][start+16:end-5].split(' \n')))
                        
                      
                    #copy_number_alterations
                    if text[i].find('Copy Number Variations') > -1: 
                        print('\ncopy_number_alterations')
                        print(text[i])
                        #start = text[i].find('Chromosome  Gene  Variation  Copy Number')
                        #end = text[i].find('- Fusions')
                        #print(text[i][start+43:end-4].split(' \n'))
                        #copy_number_alterations.extend(text[i][start+43:end-4].split(' \n'))
                        #print(len(text[i][start+43:end-4].split(' \n')))
               
                    #pmi
                    if text[i].find('Sample Information') > -1: 
                        print('\nPMI')
                        #print(text[0])
                        start = text[0].find('Sample Information\n')
                        end = text[0].find('\nTable of')
                        print(text[0][start:end])
                        #start = text[0].find('ORDERING PHYSICIAN')
                        #end = text[0].find('SPECIMEN')
                        #print(text[0][start+18:end-1])
                        #start = text[0].find('SPECIMEN')
                        #end = text[0].find('ABOUT')
                        #print(text[0][start+10:end-1])
                        
                        #copy_number_alterations.extend(text[i][start+43:end-4].split(' \n'))
                        #print(len(text[i][start+43:end-4].split(' \n')))
                    
                        
                print(dirpath + ' OK')
        except:
            print(dirpath + ' NG')
#print(os.getcwd())   # /content
#print(os.listdir('../media/UploadedFiles'))# ..上層目錄
listfloder=['ACTOnco V1','ACTOnco V2','Archer Lung','Archer Sarcoma','BRCA Assay','Focus Assay',\
            'Foundation One','Guardant 360','Myeloid Assay','Tumor Mutation Load Assay']   
listzip=glob.glob('../media/UploadedFiles/*.zip')
1
for i in range (len(listzip)):
    #print(time.ctime(os.path.getctime(glob.glob('../media/UploadedFiles/*.zip')[0])))
    #print(listzip[i])
    with zipfile.ZipFile(listzip[i],"r") as zip_ref:
        zip_ref.extractall('../media/unzip')
    #print(os.listdir('../media/unzip/'))
    strtpath=listzip[i].replace('UploadedFiles', 'unzip').replace('.zip', '')
    for j in listfloder:
        if j == 'Focus Assay':
            strfloader = strtpath + '/' + j
            for k in os.listdir(strfloader):
                print(strfloader + '/' + k)
                FocusAssay(strfloader)
                
                
def FocusAssay(pdfpath):
    ### creating a pdf reader object Focus Assay ###
    #dirlist=glob.glob('F22100_S111-97911*')
    dirlist=glob.glob(pdfpath)
    for dirpath in dirlist:
        try:    
            ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
            #filepathlist =glob.glob(os.path.join(dirpath, "*.xml"))
            filepathlist =glob.glob(os.path.join(dirpath, "S*).pdf"))
            #print(filepathlist)        
            for filename in filepathlist:
                print(filename)
                reader = PyPDF2.PdfReader(filename)
                #text_file = open("Output.txt", "w", encoding="utf-8")
                text=[]
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                    #text_file.write(reader.pages[i].extract_text())
                #text_file.close()
                #OTHER DETECTED VARIANTS
                short_variants = []            
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = []
                
                for i in range(len(text)):
                    
                    #short variants                
                    if text[i].find('OTHER DETECTED VARIANTS') > -1:
                        print('\nDETECTED VARIANTS')
                        start = text[i].find('Frequency  Coverage')
                        end = text[i].find('Note:')
                        short_variants.extend(text[i][start+22:end-5].split(' \n'))
                        #print(len(text[i][start+22:end-5].split(' \n')))
                        print(text[i][start+22:end-5].split(' \n'))
                        
                    #rearrangement
                    if text[i].find('Gene Fusions (RNA)') > -1: 
                        print('\nFusions')
                        print(text[i])
                        #start = text[i].find('Transcript ID ')
                        #end = text[i].find('- Immune')
                        #print(text[i][start+16:end-5].split(' \n'))
                        #rearrangement.extend(text[i][start+16:end-5].split(' \n'))
                        #print(len(text[i][start+16:end-5].split(' \n')))
                        
                      
                    #copy_number_alterations
                    if text[i].find('Copy Number Variations') > -1: 
                        print('\ncopy_number_alterations')
                        print(text[i])
                        #start = text[i].find('Chromosome  Gene  Variation  Copy Number')
                        #end = text[i].find('- Fusions')
                        #print(text[i][start+43:end-4].split(' \n'))
                        #copy_number_alterations.extend(text[i][start+43:end-4].split(' \n'))
                        #print(len(text[i][start+43:end-4].split(' \n')))
               
                    #pmi
                    if text[i].find('Sample Information') > -1: 
                        print('\nPMI')
                        #print(text[0])
                        start = text[0].find('Sample Information\n')
                        end = text[0].find('\nTable of')
                        print(text[0][start:end])
                        #start = text[0].find('ORDERING PHYSICIAN')
                        #end = text[0].find('SPECIMEN')
                        #print(text[0][start+18:end-1])
                        #start = text[0].find('SPECIMEN')
                        #end = text[0].find('ABOUT')
                        #print(text[0][start+10:end-1])
                        
                        #copy_number_alterations.extend(text[i][start+43:end-4].split(' \n'))
                        #print(len(text[i][start+43:end-4].split(' \n')))
                    
                        
                print(dirpath + ' OK')
        except:
            print(dirpath + ' NG')