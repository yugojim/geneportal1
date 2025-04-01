import PyPDF2
import os
import glob
import xmltodict
import json
import shutil
import re
import warnings
warnings.filterwarnings('ignore')

### 移动PDF 至目錄 ###
def pdf2floder(PdfPath):
    os.chdir(PdfPath)
    dirlist=glob.glob('*_*')
    for dirpath in dirlist:
        #print(dirpath.replace('.pdf', ''))
        source_dir = dirpath
        destination_dir = dirpath.replace('.pdf', '')
                
        # 确保目标目录存在
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        try:
            shutil.move(source_dir, destination_dir)
            #print(f"移动文件 {source_dir} 到 {destination_dir}")
        except Exception as e:
            print(f"移动文件 {source_dir} 失败：{e}")
    os.chdir('..')
    return 'xml2sql done'

### 新增XML 至SQL ###
def xmlisql(PdfPath,conn,cur):
    os.chdir(PdfPath)
    dirlist=glob.glob('*_*')
    for dirpath in dirlist:
        try:    
            ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
            filepathlist =glob.glob(os.path.join(dirpath, "*.xml"))
            #print(filepathlist)        
            for filename in filepathlist:
                #print(filename)
                #print(filename.split('\\')[1])
                #os.remove(filename)
                #try:
                with open(filename, encoding="utf-8") as fd:
                    exDict = xmltodict.parse(fd.read())            
                    sql='INSERT INTO public.reportxml(resultsreport,"ReportNo", "MPNo") VALUES (\'' + json.dumps(exDict).replace("'", " ").replace("rr:", "").replace(":rr", "").replace("@", "").replace(":xsi", "xsi").replace("xsi:", "xsi").replace(":xsd", "xsd").replace("xsd:", "xsd").replace("-", "_") + '\'' + ',\'' + ReportNo + '\'' + ',\'' + MPNo + '\'' + ');'
                    #print(sql)
                    cur.execute(sql)            
                    conn.commit()
                    #print(dirpath + ' INSERT')
                #except:
                    #print('no xml')
            #print(dirpath + ' OK')
        except:
            None
            #print(dirpath + ' NG')
    os.chdir('..')
    return 'xml2sql done'
### 新增XML 至SQL ###
def sqldelduplicate(conn,cur):
    try:
        sql='WITH duplicates AS ( SELECT *, ROW_NUMBER() OVER (PARTITION BY "ReportNo", "MPNo" ORDER BY id DESC) AS row_num FROM public.reportxml) DELETE FROM public.reportxml WHERE id IN (SELECT id FROM duplicates WHERE row_num > 1);'
        #print(sql)
        cur.execute(sql)            
        conn.commit()
        print('duplicate')
    except:            
        print('NG')
    return 'sqldelduplicate done'


### 更新XML 至SQL ###
def xml2sql(PdfPath,conn,cur):
    os.chdir(PdfPath)
    dirlist=glob.glob('*_*')
    for dirpath in dirlist:
        try:    
            ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
            filepathlist =glob.glob(os.path.join(dirpath, "*.xml"))
            #print(filepathlist)        
            for filename in filepathlist:
                #print(filename)
                #print(filename.split('\\')[1])
                #os.remove(filename)

                with open(filename, encoding="utf-8") as fd:
                    exDict = xmltodict.parse(fd.read()) 
                sql='UPDATE public.reportxml SET resultsreport = \'' + json.dumps(exDict).replace("'", " ").replace("rr:", "").replace(":rr", "").replace("@", "").replace(":xsi", "xsi").replace("xsi:", "xsi").replace(":xsd", "xsd").replace("xsd:", "xsd").replace("-", "_") + '\' \
                    where "ReportNo"= \'' + ReportNo + '\' and ' + '"MPNo"=\'' + MPNo + '\'' + ';'
                #print(sql)
                cur.execute(sql)  
                conn.commit()
                #print(cur.rowcount)
                print(dirpath + ' UPDATE')

            #print(dirpath + ' OK')
        except:
            print(dirpath + ' NG')
    os.chdir('..')
    return 'xml2sql done'

### Guardant360 ###
def Guardant3602xml(PdfPath):
    os.chdir(PdfPath)
    dirlist=glob.glob('*')
    #print(len(dirlist))
    for dirpath in dirlist:
        try: 
            basedict={
                "rr:ResultsReport": {
                    "rr:ResultsPayload": {
                        "FinalReport":{
                            "Sample": {
                                "FM_Id": "",
                                "SampleId": "",
                                "BlockId": "",
                                "TRFNumber": "",
                                "TestType": "",
                                "SpecFormat": "",
                                "ReceivedDate": "",
                                },
                            "PMI" : {
                                "ReportId": "",
                                "MRN": "",
                                "FullName": "",
                                "FirstName": "",
                                "LastName": "",
                                "SubmittedDiagnosis": "",
                                "Gender": "",
                                "DOB": "",
                                "OrderingMD": "",
                                "OrderingMDId": "",
                                "Pathologist": "",
                                "CopiedPhysician1": "",
                                "MedFacilName": "",
                                "MedFacilID": "",
                                "SpecSite": "",
                                "CollDate": "",
                                "ReceivedDate": "",
                                "CountryOfOrigin": ""
                               }
                            },
                        "variant-report": {
                            "short_variants": {
                                "short_variant":[]
                                },
                            "copy_number_alterations": {
                                "copy_number_alteration": []
                                },
                            "rearrangements": {
                            	"rearrangement": []
                            },
                            "biomarkers": {
                                "microsatellite_instability": {
                                    "status": ""
                                },
                                "tumor_mutation_burden": {
                                    "score": ""
                                }
                            }                
                        }
                        }
                    }
            }
            ReportNo, MPNo  = dirpath.replace('(', '').replace(')', '').split('_')
            filepathlist =glob.glob(os.path.join(dirpath, "*).pdf"))
            #filepath="D:/2024/3/geneportal/FhirPotal/static/doc/gene/M112-00052_(AL23002).pdf"
            #print(filepathlist)        
            for filename in filepathlist:
                #print(filename)
                reader = PyPDF2.PdfReader(filename)
                #text_file = open("Output.txt", "w", encoding="utf-8")
                text=[]
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                    #text_file.write(reader.pages[i].extract_text())
                #text_file.close()
                short_variants = []            
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = []           
                
                for i in range(len(text)):
                    #print(text[i])
                    #print(i)
                       
                    try:                    
                        #biomarkers
                        if text[i].find('Additional Biomarker') > -1: 
                            #print('biomarkers '+str(i))
                            #print(text[i])
                            start = text[i].find('Additional Details')
                            end = text[i].find('Alterations or')
                            biomarkers = []
                            biomarkers.extend(text[i][start + 19:end-1].split('\n'))
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['biomarkers']['microsatellite_instability']['status']=biomarkers[0].split(' ')[0]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['biomarkers']['tumor_mutation_burden']['score']=biomarkers[0].split(' ')[1]
                    except:
                        None
                    
                    try:
                    #copy_number_alterations
                        if text[i].find('Guardant360 Tumor Response Map') > -1: 
                            #print('copy_number_alterations' + str(i))
                            start = text[i].find('\xa0\n')
                            end = text[i].find('\xa0\nThe')
                            #print(text[i][start+43:end-4].split(' \n'))
                            copy_number_alterations.extend(text[i][start+3:end-1].replace('Variants of Uncertain Clinical Significance §', '').replace('Synonymous Alteration §', '').strip().split('\n'))
                            copy_number_alterationlist=[]
                            short_variantllist=[]
                            rearrangementlist=[]
                            for copy_number_alteration in copy_number_alterations:
                                if copy_number_alteration != '':
                                    if len(copy_number_alteration.strip().split(' '))==2:
                                        short_variantllist.append({
                                            "gene": copy_number_alteration.strip().split(' ')[0],
                                            "allele_fraction": copy_number_alteration.strip().split(' ')[1]}) 
                                        basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variantllist
                                    else:
                                        #print(copy_number_alteration)
                                        try:
                                            if 'Amplification' in copy_number_alteration:
                                                #print(copy_number_alteration.strip())
                                                if copy_number_alteration.strip().replace('Amplification','').split(' ')[0] > 2:
                                                    copy_number_alterationlist.append({
                                                        "gene": copy_number_alteration.strip().replace('Amplification','').split(' ')[0],
                                                        "type": 'Amplification'
                                                        })
                                                
                                            if 'SNV' in copy_number_alteration:
                                                #print(copy_number_alteration.strip())
                                                copy_number_alterationlist.append({
                                                    "gene": copy_number_alteration.strip().replace('SNV','').split(' ')[1],
                                                    "type": 'SNV'
                                                    })
                                            
                                            if 'deletion' in copy_number_alteration:
                                                #print(copy_number_alteration.strip())
                                                copy_number_alterationlist.append({
                                                    "gene": copy_number_alteration.strip().split(' ')[1],
                                                    "type": 'deletion'
                                                    })
                                                
                                            if 'insertion' in copy_number_alteration:
                                                #print(copy_number_alteration.strip())
                                                copy_number_alterationlist.append({
                                                    "gene": copy_number_alteration.strip().split(' ')[1],
                                                    "type": 'insertion'
                                                    })
                                                
                                            if 'Fusion' in copy_number_alteration:
                                                Fusion=copy_number_alteration
                                                rearrangementlist.append({
                                                    "description":copy_number_alteration.strip().split(' ')[1],
                                                    "other_gene": copy_number_alteration.strip().split(' ')[1].split('-')[0],
                                                    "targeted_gene": copy_number_alteration.strip().split(' ')[1].split('-')[1]
                                                    })
                                            
                                            if '%' in copy_number_alteration.strip().split(' ')[3]:
                                                #print('%')
                                                copy_number_alterationlist.append({
                                                    "gene": copy_number_alteration.strip().split(' ')[2],
                                                    "ratio": copy_number_alteration.strip().split(' ')[3]
                                                    })
                                        except:
                                            None
                                        #print(copy_number_alterationlist)
                                        #print(rearrangementlist)
                                        basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['copy_number_alterations']['copy_number_alteration'] = copy_number_alterationlist
                                        basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement']=rearrangementlist
                            #print(len(text[i][start+43:end-4].split(' \n')))
                        #print(copy_number_alterations)
                    except:
                        None
                        
                    try:
                        #pmi
                        if text[i].find('PATIENT AND SAMPLE INFORMATION') > -1: 
                            #print('PMI')
                            start = text[i].find('ORDERING PHYSICIAN')
                            end = text[i].find('ID: NA')
                            PATIENT = text[i][start+21:end]
                            #print(PATIENT)
                            #print(PATIENT.split(' \n'))
                            ['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split(' \n')[0].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split(' \n')[3].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SpecSite'] = PATIENT.split(' \n')[2].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['DOB'] = PATIENT.split(' \n')[2].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split(' \n')[1].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = PATIENT.split(' \n')[4].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PATIENT.split(' \n')[0].split('  ')[2].split(': ')[1]
                            
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = PATIENT.split(' \n')[0].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = PATIENT.split(' \n')[3].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['ReceivedDate'] = PATIENT.split(' \n')[1].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TestType'] = 'ACTOnco'
                    except:
                        None 

                with open(os.path.join(dirpath,ReportNo+'_('+MPNo+').xml'), 'w', encoding="utf-8") as output:
                    output.write(xmltodict.unparse(basedict, pretty=True))            
                #print(dirpath + ' OK')
        except:
            None
            #print(dirpath + ' NG')   
    os.chdir('..')
    return 'Guardant3602xml done'

### ACTOnco V2 ###
def ACTGV22xml(PdfPath):
    print(PdfPath)
    os.chdir(PdfPath)
    dirlist=glob.glob('*')
    print(dirlist)
    for dirpath in dirlist:
        basedict={
            "rr:ResultsReport": {
                "rr:ResultsPayload": {
                    "FinalReport":{
                        "Sample": {
                            "FM_Id": "",
                            "SampleId": "",
                            "BlockId": "",
                            "TRFNumber": "",
                            "TestType": "",
                            "SpecFormat": "",
                            "ReceivedDate": "",
                            },
                        "PMI" : {
                            "ReportId": "",
                            "MRN": "",
                            "FullName": "",
                            "FirstName": "",
                            "LastName": "",
                            "SubmittedDiagnosis": "",
                            "Gender": "",
                            "DOB": "",
                            "OrderingMD": "",
                            "OrderingMDId": "",
                            "Pathologist": "",
                            "CopiedPhysician1": "",
                            "MedFacilName": "",
                            "MedFacilID": "",
                            "SpecSite": "",
                            "CollDate": "",
                            "ReceivedDate": "",
                            "CountryOfOrigin": ""
                           }
                        },
                    "variant-report": {
                        "short_variants": {
                            "short_variant":[]
                            },
                        "copy_number_alterations": {
                            "copy_number_alteration": []
                            },
                        "rearrangements": {
                        	"rearrangement": []
                        },
                        "biomarkers": {
                            "microsatellite_instability": {
                                "status": ""
                            },
                            "tumor_mutation_burden": {
                                "score": ""
                            }
                        }                
                    }
                    }
                }
        }
        try:    
            ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
            filepathlist =glob.glob(os.path.join(dirpath, "*).pdf"))
            #print(filepathlist)        
            for filename in filepathlist:
                #print(filename)
                reader = PyPDF2.PdfReader(filename)
                #text_file = open("Output.txt", "w", encoding="utf-8")
                text=[]
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                    #text_file.write(reader.pages[i].extract_text())
                #text_file.close()
                short_variants = []            
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = []           
                
                for i in range(len(text)):
                    #print(text[i])
                    #short variants
                    try:
                        '''
                        if text[i].find('Single Nucleotide and Small InDel Variants') > -1:
                            Variants_start = text.find('COSMIC ID  Allele \nFrequency  Coverage')
                            Variants_end = text.find('\n \n- Copy Number Alterations  \nObserved copy number')
                            short_variants.extend(text[Variants_start+39:Variants_end].strip().replace('  \n(','(').replace('Exon ','Exon').replace(' deletion','deletion').split(' \n'))
                        
                        if text[i].find('\nOTHER DETECTED VARIANTS') > -1:
                            Variants1_start = text[i].find('COSMIC ID  Allele \nFrequency  Coverage')
                            Variants1_end = text[i].find('\n \nNote:  \n- This table enlists')
                            short_variants.extend(text[Variants1_start+39:Variants1_end].strip().replace('  \n(','(').replace('Exon ','Exon').replace(' deletion','deletion').split(' \n'))
                            #print(text[Variants_start+39:Variants_end].strip().replace('  \n(','('))    
                        #print(short_variants)
                        '''
                        if text[i].find('OTHER DETECTED VARIANTS') > -1:
                            #print('\nDETECTED VARIANTS')
                            start = text[i].find('Frequency  Coverag')
                            end = text[i].find('Note:')
                            short_variants.extend(text[i][start+21:end-5].split(' \n'))
                            #print(len(text[i][start+22:end-5].split(' \n')))
                            #print(text[i][start+22:end-5].split(' \n'))
                        
                        if text[i].find('VARIANTS WITH CLINICAL RELEVANCE') > -1: 
                            #print('\nCLINICAL RELEVANCE')
                            #print(text[i])
                            start = text[i].find('Frequency  Coverag')
                            end = text[i].find('- Copy')
                            short_variants.extend(text[i][start+21:end-5].replace('  \n(','(').replace('Exon ','Exon').replace(' deletion','deletion').split(' \n'))
                            #print(len(text[i][start+22:end-5].split(' \n')))
                            #print(text[i][start+22:end-5].split(' \n'))
                            
                        if len(short_variants) > 0:
                            #print(short_variants)
                            short_variantllist=[]
                            for j in range(len(short_variants)):
                                short_variants[j] = short_variants[j].strip().replace('  ', ' ').replace(' ', ',').replace(',,', ',')
                                if len(short_variants[j].split(',')) > 3:                            
                                    short_variantllist.append({
                                        "cds_effect": short_variants[j].split(',')[3],
                                        "depth": short_variants[j].split(',')[7],
                                        "gene": short_variants[j].split(',')[0],
                                        "percent_reads": short_variants[j].split(',')[6],
                                        "protein_effect": short_variants[j].split(',')[1],
                                        "transcript": short_variants[j].split(',')[4],
                                        }) 
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variantllist
                        #print(short_variantllist)   
                    except:
                        None
                        
                    try:    
                        #rearrangement
                        if text[i].find('- Fusions') > -1: 
                            #print(text[i])
                            start = text[i].find('Transcript ID ')
                            end = text[i].find('- Immune')
                            #print(text[i][start+16:end-5].split(' \n'))
                            rearrangement.extend(text[i][start+16:end-5].split(' \n'))
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement'][0]['description'] = rearrangement[0]
                            if len(rearrangement[0].split('  ')) > 1:
                                print('\nFusions')
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement'][0]['other_gene'] = rearrangement[0].split('  ')[0].split(' ')[0]
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement'][0]['targeted_gene'] = rearrangement[0].split('  ')[0].split(' ')[1]
                            #print(rearrangement)    
                            #print(len(text[i][start+16:end-5].split(' \n')))
                    except:
                        None
                        
                    try:                    
                        #biomarkers
                        if text[i].find('Checkpoint') > -1: 
                            #print('\nbiomarkers')
                            #print(text[i])
                            tmb_index = text[i].find('Tumor Mutational Burden (TMB)')
                            msi_index = text[i].find('Microsatellite Instability (MSI)')
                            
                            # 提取TMB和MSI信息
                            tmb_info = text[i][tmb_index+29:tmb_index+79].split('\n')[0].strip()
                            tmb_value = re.findall(r'\d+\.\d+', tmb_info)[0]
                            tmb_value = float(tmb_value)
                            msi_info = text[i][msi_index+32:msi_index+82].split('\n')[0].strip()
                            
                            # 打印提取的信息
                            #print("TMB Information: ", tmb_value)
                            #print("MSI Information: ", msi_info)
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['biomarkers']['microsatellite_instability']['status']=msi_info
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['biomarkers']['tumor_mutation_burden']['score']=tmb_value
                            #print(len(text[i][start + 21:end - 5].split('\n')))
                            #print(biomarkers)
                    except:
                        None
                    
                    try:
                        #copy_number_alterations
                        #print(i)
                        if text[i].find('Chromosome  Gene  Variation  Copy Number') > -1: 
                            #print('\ncopy_number_alterations')
                            #print(text[i])
                            start = text[i].find('Chromosome  Gene  Variation  Copy Number')
                            end = text[i].find('- Fusions')
                            #print(text[i][start+43:end-4].split(' \n'))
                            copy_number_alterations.extend(text[i][start+43:end-4].split(' \n'))
                            copy_number_alterationlist=[]
                            for copy_number_alteration in copy_number_alterations:
                                try:
                                    alterationlist = copy_number_alteration.split('  ')
                                    copy_number_alterationlist.append({"copy_number": alterationlist[3],
                                                              "gene": alterationlist[1],
                                                              "position": alterationlist[0],
                                                              "type": alterationlist[2]})
                                except:
                                    None
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['copy_number_alterations']['copy_number_alteration'] = copy_number_alterationlist
                            #print(len(text[i][start+43:end-4].split(' \n')))
                        #print(copy_number_alterations)
                    except:
                        None
                    try:
                        #pmi
                        if text[i].find('PATIEN') > -1: 
                            #print('\nPMI')
                            #print(text[0])
                            start = text[0].find('PATIEN')
                            end = text[0].find('ORDERING PHYSICIAN')
                            #print(text[0][start+10:end-1])
                            PATIENT = text[0][start+10:end-1]
                            #print(PATIENT)
                            #print(PATIENT.split(' \n'))
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split(' \n')[0].split(':')[1].split(' ')[1] #name
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split(' \n')[0].split(':')[2].strip()    
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['DOB'] = PATIENT.split(' \n')[1].split(':')[1].replace('Gender', '').strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split(' \n')[1].split(':')[2].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = PATIENT.split(' \n')[2].split(':')[1].strip()
                            
                            start = text[0].find('ORDERING PHYSICIAN')
                            end = text[0].find('SPECIMEN')
                            #print(text[0][start+21:end-1]) 
                            PHYSICIAN = text[0][start+21:end-1]
                            #print(PHYSICIAN)
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PHYSICIAN.split('\n')[0].split(':')[1].replace('Tel', '').strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MedFacilName'] = PHYSICIAN.split('\n')[1].split(':')[1].strip()
                            
                            start = text[0].find('SPECIMEN')
                            end = text[0].find('ABOUT')
                            #print(text[0][start+11:end-1])
                            SPECIMEN = text[0][start+11:end-4]
                            #print(SPECIMEN)
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = SPECIMEN.split('\n')[0].split(':')[2].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = dirpath
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['FM_Id'] = SPECIMEN.split('\n')[1].split(':')[2].replace('D/ID', '').strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['ReceivedDate'] = SPECIMEN.split('\n')[1].split(':')[1].replace('Lab ID', '').strip()
                    except:
                        None
                with open(os.path.join(dirpath,ReportNo+'_('+MPNo+').xml'), 'w', encoding="utf-8") as output:
                    output.write(xmltodict.unparse(basedict, pretty=True))            
                #print(dirpath + ' OK')
        except:
            None
            #print(dirpath + ' NG')
    os.chdir('..')
    return 'ACTGV22xml done'
### ACTOnco V1 ###
def ACTGV12xml(PdfPath):
    os.chdir(PdfPath)
    dirlist=glob.glob('*')    
    for dirpath in dirlist:
        try: 
            basedict={
                "rr:ResultsReport": {
                    "rr:ResultsPayload": {
                        "FinalReport":{
                            "Sample": {
                                "FM_Id": "",
                                "SampleId": "",
                                "BlockId": "",
                                "TRFNumber": "",
                                "TestType": "",
                                "SpecFormat": "",
                                "ReceivedDate": "",
                                },
                            "PMI" : {
                                "ReportId": "",
                                "MRN": "",
                                "FullName": "",
                                "FirstName": "",
                                "LastName": "",
                                "SubmittedDiagnosis": "",
                                "Gender": "",
                                "DOB": "",
                                "OrderingMD": "",
                                "OrderingMDId": "",
                                "Pathologist": "",
                                "CopiedPhysician1": "",
                                "MedFacilName": "",
                                "MedFacilID": "",
                                "SpecSite": "",
                                "CollDate": "",
                                "ReceivedDate": "",
                                "CountryOfOrigin": ""
                               }
                            },
                        "variant-report": {
                            "short_variants": {
                                "short_variant":[]
                                },
                            "copy_number_alterations": {
                                "copy_number_alteration": []
                                },
                            "rearrangements": {
                            	"rearrangement": []
                            },
                            "biomarkers": {
                                "microsatellite_instability": {
                                    "status": ""
                                },
                                "tumor_mutation_burden": {
                                    "score": ""
                                }
                            }                
                        }
                        }
                    }
            }
            ReportNo, MPNo  = dirpath.replace('(', '').replace(')', '').split('_')
            filepathlist =glob.glob(os.path.join(dirpath, "*).pdf"))
            #print(filepathlist)        
            for filename in filepathlist:
                #print(filename)
                reader = PyPDF2.PdfReader(filename)
                #text_file = open("Output.txt", "w", encoding="utf-8")
                text=[]
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                    #text_file.write(reader.pages[i].extract_text())
                #text_file.close()
                short_variants = []            
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = []           
                
                for i in range(len(text)):
                    #print(text[i])
                    #print(i)
                    try:
                        if i==1: 
                            print('PMI')
                            start = text[i].find('ORDERING PHYSICIAN')
                            end = text[i].find('ID: NA')
                            PATIENT = text[i][start+21:end]
                            #print(PATIENT)
                            #print(PATIENT.split(' \n'))
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split(' \n')[0].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split(' \n')[3].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SpecSite'] = PATIENT.split(' \n')[2].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['DOB'] = PATIENT.split(' \n')[2].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split(' \n')[1].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = PATIENT.split(' \n')[4].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PATIENT.split(' \n')[0].split('  ')[2].split(': ')[1]
                            
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = PATIENT.split(' \n')[0].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = PATIENT.split(' \n')[3].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['ReceivedDate'] = PATIENT.split(' \n')[1].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TestType'] = 'ACTOnco'
                        
                        
                            #print(text[i])
                        
                            if text[i].find('INSTA BILITY (MSI)') >-1:
                                start = text[i].find('INSTA BILITY (MSI)')
                            else:
                                start = text[i].find('INSTABILITY (MSI)')
                            
                            end = text[i].find('Note:')
                            biomarkers = []
                            biomarkers.extend(text[i][start + 21:end - 5].split('\n'))
                            if biomarkers[0].split('  ')[2] == '':
                                status=biomarkers[0].split('  ')[1]
                            else:
                                status=biomarkers[0].split('  ')[2]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['biomarkers']['microsatellite_instability']['status']=status
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['biomarkers']['tumor_mutation_burden']['score']=biomarkers[0].split('  ')[0].split(' ')[0]
                    except:
                        None
                            
                    try:                    
                        #biomarkers
                        if text[i].find('TUMOR MUTATIONAL') > -1: 
                            #print('\nbiomarkers')
                            #print(text[i])
                            tmb_index = text[i].find('Tumor Mutational Burden (TMB)')
                            msi_index = text[i].find('Microsatellite Instability (MSI)')
                            
                            # 提取TMB和MSI信息
                            tmb_info = text[i][tmb_index+29:tmb_index+79].split('\n')[0].strip()
                            tmb_value = re.findall(r'\d+\.\d+', tmb_info)[0]
                            tmb_value = float(tmb_value)
                            msi_info = text[i][msi_index+32:msi_index+82].split('\n')[0].strip()
                            
                            # 打印提取的信息
                            #print("TMB Information: ", tmb_value)
                            #print("MSI Information: ", msi_info)
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['biomarkers']['microsatellite_instability']['status']=msi_info
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['biomarkers']['tumor_mutation_burden']['score']=tmb_value
                            #print(len(text[i][start + 21:end - 5].split('\n')))
                            #print(biomarkers)
                    except:
                        None
                    
                    try:
                    #copy_number_alterations
                        if text[i].find('(CNVS)') > -1 or text[i].find('(CNV S)') > -1: 
                            print('copy_number_alterations' + str(i))
                            #print(text[i])
                            start = text[i].find('Amplification')
                            if text[i].find('TUMOR') > -1:
                                end = text[i].find('TUMOR')
                            else:
                                end = text[i].find('ND, Not Detected')
                            #print(text[i][start+43:end-4].split(' \n'))
                            copy_number_alterations.extend(text[i][start:end].replace(' Copy Number', '').replace('Chr Gene ', '').replace('  ', ' ').replace(', ', ',').strip().split(' \n'))
                            copy_number_alterationlist=[]
                            for copy_number_alteration in copy_number_alterations:
                                if copy_number_alteration != '':
                                    if 'Copy number' in copy_number_alteration:
                                        #print(copy_number_alteration.split(' (Copy number'))
                                        altertype=copy_number_alteration.split(' (Copy number')[0]
                                        copy_number=re.findall(r"-?\d+\.?\d*", copy_number_alteration.split(' (Copy number')[1])
                                    else:
                                        try:
                                            list_copy_number=copy_number_alteration.split(' ')[2]
                                        except:
                                            list_copy_number=copy_number
                                        copy_number_alterationlist.append({"copy_number": list_copy_number,            
                                                      "gene": copy_number_alteration.split(' ')[1],
                                                      "position": copy_number_alteration.split(' ')[0],
                                                      "type": altertype})
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['copy_number_alterations']['copy_number_alteration'] = copy_number_alterationlist
                    
                            #print(len(text[i][start+43:end-4].split(' \n')))
                        #print(copy_number_alterations)
                    except:
                        None
                        
                    try:
                        #short variants
                        if text[i].find('Gene  Amino Acid Change') > -1:
                            print('short variants' + str(i))
                            start = text[i].find('Frequency  COSMIC ID')
                            end = text[i].find('COPY NUMBER')
                            short_variants.extend(text[i][start+23:end-3].split(' \n'))
                            #print(len(text[i][start+22:end-5].split(' \n')))
                            #print(text[i][start+22:end-5].split(' \n'))
                            
                        if len(short_variants) > 0:
                            short_variantllist=[]
                            for j in range(len(short_variants)):
                                
                                if len(short_variants[j].split('  ')) >= 3:                            
                                    short_variantllist.append({
                                        "depth": short_variants[j].replace('  ', ' ').split(' ')[2],
                                        "gene": short_variants[j].replace('  ', ' ').split(' ')[0],
                                        "percent_reads": short_variants[j].replace('  ', ' ').split(' ')[3],
                                        "protein_effect": short_variants[j].replace('  ', ' ').split(' ')[1],
                                         }) 
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variantllist
                        #print(short_variantllist)   
                    except:
                        None
                       
                    try:
                        #pmi
                        if text[i].find('PATIENT AND SAMPLE INFORMATION') > -1: 
                            #print('PMI')
                            start = text[i].find('ORDERING PHYSICIAN')
                            end = text[i].find('ID: NA')
                            PATIENT = text[i][start+21:end]
                            #print(PATIENT)
                            #print(PATIENT.split(' \n'))
                            ['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split(' \n')[0].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split(' \n')[3].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SpecSite'] = PATIENT.split(' \n')[2].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['DOB'] = PATIENT.split(' \n')[2].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split(' \n')[1].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = PATIENT.split(' \n')[4].split('  ')[0].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PATIENT.split(' \n')[0].split('  ')[2].split(': ')[1]
                            
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = PATIENT.split(' \n')[0].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = PATIENT.split(' \n')[3].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['ReceivedDate'] = PATIENT.split(' \n')[1].split('  ')[1].split(': ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TestType'] = 'ACTOnco'
                    except:
                        None 
                        
                    try:    
                        #rearrangement
                        if text[i].find('- Fusions') > -1: 
                            #print(text[i])
                            print('rearrangement ' + str(i))
                            start = text[i].find('Transcript ID ')
                            end = text[i].find('- Immune')
                            #print(text[i][start+16:end-5].split(' \n'))
                            rearrangement.extend(text[i][start+16:end-5].split(' \n'))
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement'][0]['description'] = rearrangement[0]
                            if len(rearrangement[0].split('  ')) > 1:
                                #print('\nFusions')
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement'][0]['other_gene'] = rearrangement[0].split('  ')[0].split(' ')[0]
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement'][0]['targeted_gene'] = rearrangement[0].split('  ')[0].split(' ')[1]
                            #print(rearrangement)    
                            #print(len(text[i][start+16:end-5].split(' \n')))
                    except:
                        None
    
                with open(os.path.join(dirpath,ReportNo+'_('+MPNo+').xml'), 'w', encoding="utf-8") as output:
                    output.write(xmltodict.unparse(basedict, pretty=True))            
                #print(dirpath + ' OK')
        except:
            None
            #print(dirpath + ' NG')
    os.chdir('..')
    return 'ACTGV12xml done'
### Archer ###
def Archer2xml(PdfPath):
    os.chdir(PdfPath)
    dirlist=glob.glob('*_*')
    #print(len(dirlist))
    for dirpath in dirlist:
        try: 
            basedict={
                "rr:ResultsReport": {
                    "rr:ResultsPayload": {
                        "FinalReport":{
                            "Sample": {
                                "FM_Id": "",
                                "SampleId": "",
                                "BlockId": "",
                                "TRFNumber": "",
                                "TestType": "",
                                "SpecFormat": "",
                                "ReceivedDate": "",
                                },
                            "PMI" : {
                                "ReportId": "",
                                "MRN": "",
                                "FullName": "",
                                "FirstName": "",
                                "LastName": "",
                                "SubmittedDiagnosis": "",
                                "Gender": "",
                                "DOB": "",
                                "OrderingMD": "",
                                "OrderingMDId": "",
                                "Pathologist": "",
                                "CopiedPhysician1": "",
                                "MedFacilName": "",
                                "MedFacilID": "",
                                "SpecSite": "",
                                "CollDate": "",
                                "ReceivedDate": "",
                                "CountryOfOrigin": ""
                               }
                            },
                        "variant-report": {
                            "short_variants": {
                                "short_variant":[]
                                },
                            "copy_number_alterations": {
                                "copy_number_alteration": []
                                },
                            "rearrangements": {
                            	"rearrangement": []
                            },
                            "biomarkers": {
                                "microsatellite_instability": {
                                    "status": ""
                                },
                                "tumor_mutation_burden": {
                                    "score": ""
                                }
                            }                
                        }
                        }
                    }
            }
            ReportNo, MPNo  = dirpath.replace('(', '').replace(')', '').split('_')
            filepathlist =glob.glob(os.path.join(dirpath, "*).pdf"))
            #print(filepathlist)        
            for filename in filepathlist:
                #print(filename)
                reader = PyPDF2.PdfReader(filename)
                #text_file = open("Output.txt", "w", encoding="utf-8")
                text=[]
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                    #text_file.write(reader.pages[i].extract_text())
                #text_file.close()
                short_variants = []            
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = []           
                rearrangementlist=[]
                for i in range(len(text)):
                       
                    try:    
                        #rearrangement
                        if text[i].find('Reportable Isoforms') > -1: 
                            #print(text[i])
                            #print('rearrangement ' + str(i))
                            test_string = text[i]
                            ans=re.findall('Fusion:.+\n',test_string)
                            exon=re.findall('on:.\n',test_string)
                            for a in range(len(ans)):
                                try:
                                    description= ans[a][8:].replace(' ','').replace('\n','').replace('®','_')+'.E'+exon[a*2-1].replace('on:','').replace('\n','')+'E'+exon[a*2].replace('on:','').replace('\n','')
                                except:
                                    description= ans[a][8:].replace(' ','').replace('\n','').replace('®','_')                          
                                rearrangementlist.append({                                
                                    "description":description,
                                    "other_gene": ans[a][8:].replace(' ','').replace('\n','').split('®')[0],
                                    "targeted_gene": ans[a][8:].replace(' ','').replace('\n','').split('®')[1]
                                    })
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement'] = rearrangementlist
                            #print(rearrangementlist)
                    except:
                        None
                with open(os.path.join(dirpath,ReportNo+'_('+MPNo+').xml'), 'w', encoding="utf-8") as output:
                    output.write(xmltodict.unparse(basedict, pretty=True))            
                #print(dirpath + ' OK')
        except:
            None#print(dirpath + ' NG')
   
    os.chdir('..')
    return 'Archer2xml done'

'''
def BRCAAssay2xml(PdfPath):
    os.chdir(PdfPath)
    dirlist = glob.glob('*_*')
    for dirpath in dirlist:
        basedict = {
            "rr:ResultsReport": {
                "rr:ResultsPayload": {
                    "FinalReport": {
                        "Sample": {
                            "FM_Id": "",
                            "SampleId": "",
                            "BlockId": "",
                            "TRFNumber": "",
                            "TestType": "",
                            "SpecFormat": "",
                            "ReceivedDate": "",
                        },
                        "PMI": {
                            "ReportId": "",
                            "MRN": "",
                            "FullName": "",
                            "FirstName": "",
                            "LastName": "",
                            "SubmittedDiagnosis": "",
                            "Gender": "",
                            "DOB": "",
                            "OrderingMD": "",
                            "OrderingMDId": "",
                            "Pathologist": "",
                            "CopiedPhysician1": "",
                            "MedFacilName": "",
                            "MedFacilID": "",
                            "SpecSite": "",
                            "CollDate": "",
                            "ReceivedDate": "",
                            "CountryOfOrigin": ""
                        }
                    },
                    "variant-report": {
                        "short_variants": {
                            "short_variant": []
                        },
                        "copy_number_alterations": {
                            "copy_number_alteration": []
                        },
                        "rearrangements": {
                            "rearrangement": []
                        },
                        "biomarkers": {
                            "microsatellite_instability": {
                                "status": ""
                            },
                            "tumor_mutation_burden": {
                                "score": ""
                            }
                        }
                    }
                }
            }
        }
        ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
        filepathlist = glob.glob(os.path.join(dirpath, "*.pdf"))
        
        try:
            for filename in filepathlist:
                reader = PyPDF2.PdfReader(filename)
                text = []
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                
                short_variants = []
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = []

                for i in range(len(text)):
                    try:
                        # Copy Number Alterations
                        if text[i].find('Copy Number') > -1:
                            start = text[i].find('Locus Copy Number')
                            end = text[i].find('Copy Number Variation')
                            copy_number_alterations.extend(text[i][start+28:end].strip().split('\n'))
                            copy_number_alterationlist = []
                            for copy_number_alteration in copy_number_alterations:
                                alterationlist = copy_number_alteration.split(' ')
                                copy_number_alterationlist.append({
                                    "copy_number": alterationlist[2],
                                    "gene": alterationlist[0],
                                    "position": alterationlist[1]
                                })
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['copy_number_alterations']['copy_number_alteration'] = copy_number_alterationlist
                    except:
                        pass

                    # PMI and Sample Information
                    if text[i].find('Sample Information') > -1:
                        start = text[i].find('Sample Information')
                        end = text[i].find('Note:')
                        PATIENT = text[i][start+18:end].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split('\n')[0].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split('\n')[1].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split('\n')[3].split(':')[1].strip()
                        try:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[0]
                        except:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['ReportId'] = PATIENT.split('\n')[7].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TestType'] = PATIENT.split('\n')[12].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = PATIENT.split('\n')[13].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = PATIENT.split('\n')[14].split(':')[1].strip()
                        try:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TumorPurity'] = PATIENT.split('\n')[15].split(':')[1].strip()
                        except:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = ''
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['ReceivedDate'] = PATIENT.split('\n')[14].split(':')[1].strip()

                        start = text[i].find('Cancer Type:')
                        end = text[i].find('Table of Contents')
                        CancerType = text[i][start+12:end].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = CancerType

                    # Short Variants (修正跨行問題)
                    if text[i].find('DNA Sequence') > -1:
                        start = text[i].find('ClinVar 1 Coverage')
                        end = text[i].find('DNA Sequence')
                        raw_lines = text[i][start+18:end].strip().split('\n')
                        short_variants = []
                        temp_line = ""
                        
                        # 合併跨行資料
                        for line in raw_lines:
                            line = line.strip()
                            if not line:  # 跳過空行
                                continue
                            if temp_line and (len(line.split(' ')) < 6 or 'chr' not in line):
                                temp_line += " " + line
                            else:
                                if temp_line:
                                    short_variants.append(temp_line)
                                temp_line = line
                        if temp_line:  # 確保最後一行被添加
                            short_variants.append(temp_line)

                        # 解析 short_variants
                        if len(short_variants) > 0:
                            short_variantllist = []
                            for variant in short_variants:
                                parts = variant.split(' ')
                                if len(parts) >= 6:
                                    try:
                                        functional_effect = parts[7] if len(parts) > 7 else ''
                                        depth = parts[8] if len(parts) > 8 else ''
                                        transcript = parts[6]
                                        if transcript == 'frameshift':
                                            transcript = 'frameshift Deletion'
                                        short_variantllist.append({
                                            "cds_effect": parts[2],
                                            "depth": depth,
                                            "functional_effect": functional_effect,
                                            "gene": parts[0],
                                            "percent_reads": parts[5],
                                            "position": parts[4],
                                            "protein_effect": parts[1],
                                            "transcript": transcript,
                                        })
                                    except IndexError:
                                        continue
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variantllist

                # 輸出 XML 文件
                with open(os.path.join(dirpath, ReportNo + '_(' + MPNo + ').xml'), 'w', encoding="utf-8") as output:
                    output.write(xmltodict.unparse(basedict, pretty=True))
        except Exception as e:
            print(dirpath + ' NG: ' + str(e))
    os.chdir('..')
    return 'BRCAAssay2xml done'
''' 
### BRCA Assay meta###
def BRCAAssay2xml(PdfPath):
    os.chdir(PdfPath)
    dirlist=glob.glob('*_*')
    #print(len(dirlist))
    for dirpath in dirlist:
        basedict={
            "rr:ResultsReport": {
                "rr:ResultsPayload": {
                    "FinalReport":{
                        "Sample": {
                            "FM_Id": "",
                            "SampleId": "",
                            "BlockId": "",
                            "TRFNumber": "",
                            "TestType": "",
                            "SpecFormat": "",
                            "ReceivedDate": "",
                            },
                        "PMI" : {
                            "ReportId": "",
                            "MRN": "",
                            "FullName": "",
                            "FirstName": "",
                            "LastName": "",
                            "SubmittedDiagnosis": "",
                            "Gender": "",
                            "DOB": "",
                            "OrderingMD": "",
                            "OrderingMDId": "",
                            "Pathologist": "",
                            "CopiedPhysician1": "",
                            "MedFacilName": "",
                            "MedFacilID": "",
                            "SpecSite": "",
                            "CollDate": "",
                            "ReceivedDate": "",
                            "CountryOfOrigin": ""
                           }
                        },
                    "variant-report": {
                        "short_variants": {
                            "short_variant":[]
                            },
                        "copy_number_alterations": {
                            "copy_number_alteration": []
                            },
                        "rearrangements": {
                        	"rearrangement": []
                        },
                        "biomarkers": {
                            "microsatellite_instability": {
                                "status": ""
                            },
                            "tumor_mutation_burden": {
                                "score": ""
                            }
                        }                
                    }
                    }
                }
            }
        ReportNo, MPNo= dirpath.replace('(', '').replace(')', '').split('_')
        filepathlist =glob.glob(os.path.join(dirpath, "*).pdf"))
        #print(filepathlist)
        try:        
            for filename in filepathlist:
                    #print(filename)            
                    reader = PyPDF2.PdfReader(filename)
                    #text_file = open("Output.txt", "w", encoding="utf-8")
                    text=[]
                    for i in range(len(reader.pages)):
                        text.append(reader.pages[i].extract_text())
                        #text_file.write(reader.pages[i].extract_text())
                    #text_file.close()            
                    short_variants = []            
                    rearrangement = []
                    biomarkers = []
                    copy_number_alterations = []
                    pmi = [] 
                    
                    for i in range(len(text)):
                        try:
                            #copy_number_alterations
                            
                            if text[i].find('Copy Number') > -1: 
                                start = text[i].find('Locus Copy Number')
                                end = text[i].find('Copy Number Variation')
                                #print(text[i][start+17:end].strip())
                                copy_number_alterations.extend(text[i][start+28:end].strip().split('\n'))
                                copy_number_alterationlist=[]
                                
                                    
                                for copy_number_alteration in copy_number_alterations:
                                    alterationlist = copy_number_alteration.split(' ')
                                    copy_number_alterationlist.append({"copy_number": alterationlist[2],
                                                              "gene": alterationlist[0],
                                                              "position": alterationlist[1]})
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['copy_number_alterations']['copy_number_alteration'] = copy_number_alterationlist
                                #print(len(text[i][start+43:end-4].split(' \n')))
                            #print(copy_number_alterations)
                        except:
                            None
            
                        if text[i].find('Sample Information') > -1: 
                            #print('\nPMI')
                            #print(text[0])
                            start = text[i].find('Sample Information')
                            end = text[i].find('Note:')
                            #print(text[i][start:end])
                            PATIENT=text[i][start+18:end].strip() 
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split('\n')[0].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split('\n')[1].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split('\n')[3].split(':')[1].strip()
                            try:
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[1]
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[0]
                            except:
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['ReportId'] = PATIENT.split('\n')[7].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TestType'] = PATIENT.split('\n')[12].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = PATIENT.split('\n')[13].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = PATIENT.split('\n')[14].split(':')[1].strip()
                            try:
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TumorPurity'] = PATIENT.split('\n')[15].split(':')[1].strip()
                            except:
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = ''
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['ReceivedDate'] = PATIENT.split('\n')[14].split(':')[1].strip()
                            
                            start = text[i].find('Cancer Type:')
                            end = text[i].find('Table of Contents')
                            (text[i][start:end])
                            CancerType = text[i][start+12:end].strip() 
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = CancerType
                           
                        if text[i].find('DNA Sequence') > -1:
                            #print('\nDETECTED VARIANTS')                        
                            #print(text[i])
                            start = text[i].find('ClinVar 1 Coverage')
                            end = text[i].find('DNA Sequence')
                            short_variants.extend(text[i][start+18:end].strip().split('\n'))
                            #print(len(text[i][start+22:end-5].split(' \n')))
                            #print(text[i][start+22:end-5].split(' \n'))
                            
                        if len(short_variants) > 0:
                            short_variantllist=[]
                            for i in range(len(short_variants)):
                                if len(short_variants[i].split(' ')) > 6 : 
                                    try:
                                        functional_effect = short_variants[i].split(' ')[7]
                                        depth = short_variants[i].split(' ')[8]
                                    except:
                                        depth = ''
                                        functional_effect = ''
                                        
                                    if  short_variants[i].split(' ')[6] == 'frameshift':
                                        transcript = 'frameshift Deletion'
                                    else:
                                        transcript = short_variants[i].split(' ')[6]
                                    if  functional_effect=='Taipei': #functional_effect =='' or
                                        None                                
                                    else:
                                        short_variantllist.append({
                                            "cds_effect": short_variants[i].split(' ')[2],
                                            "depth":depth,
                                            "functional_effect": functional_effect,
                                            "gene": short_variants[i].split(' ')[0],
                                            "percent_reads": short_variants[i].split(' ')[5],
                                            "position": short_variants[i].split(' ')[4],
                                            "protein_effect": short_variants[i].split(' ')[1],
                                            "transcript": transcript,
                                            })
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variantllist
                            #print(short_variantllist)
                    with open(os.path.join(dirpath,ReportNo+'_('+MPNo+').xml'), 'w', encoding="utf-8") as output:
                        output.write(xmltodict.unparse(basedict, pretty=True))            
                    #print(dirpath + ' OK')
        except:
            print(dirpath + ' NG')
    os.chdir('..')
    return 'BRCAAssay2xml done'

### Myeloid Assay meta###
def MyeloidAssay2xml(PdfPath):
    os.chdir(PdfPath)
    dirlist=glob.glob('*_*')
    #print(len(dirlist))
    for dirpath in dirlist:
        basedict={
            "rr:ResultsReport": {
                "rr:ResultsPayload": {
                    "FinalReport":{
                        "Sample": {
                            "FM_Id": "",
                            "SampleId": "",
                            "BlockId": "",
                            "TRFNumber": "",
                            "TestType": "",
                            "SpecFormat": "",
                            "ReceivedDate": "",
                            },
                        "PMI" : {
                            "ReportId": "",
                            "MRN": "",
                            "FullName": "",
                            "FirstName": "",
                            "LastName": "",
                            "SubmittedDiagnosis": "",
                            "Gender": "",
                            "DOB": "",
                            "OrderingMD": "",
                            "OrderingMDId": "",
                            "Pathologist": "",
                            "CopiedPhysician1": "",
                            "MedFacilName": "",
                            "MedFacilID": "",
                            "SpecSite": "",
                            "CollDate": "",
                            "ReceivedDate": "",
                            "CountryOfOrigin": ""
                           }
                        },
                    "variant-report": {
                        "short_variants": {
                            "short_variant":[]
                            },
                        "copy_number_alterations": {
                            "copy_number_alteration": []
                            },
                        "rearrangements": {
                        	"rearrangement": []
                        },
                        "biomarkers": {
                            "microsatellite_instability": {
                                "status": ""
                            },
                            "tumor_mutation_burden": {
                                "score": ""
                            }
                        }                
                    }
                    }
                }
            }
        ReportNo, MPNo= dirpath.replace('(', '').replace(')', '').split('_')
        filepathlist =glob.glob(os.path.join(dirpath, "*).pdf"))
        #print(filepathlist)
        filename='D:\OneDrive - Wistron Corporation\Desktop\20240611_upload_test\Myeloid Assay\M112-00227_(MY23059).pdf'
        try:        
            for filename in filepathlist:
                    print(filename)            
                    reader = PyPDF2.PdfReader(filename)
                    #text_file = open("Output.txt", "w", encoding="utf-8")
                    text=[]
                    for i in range(len(reader.pages)):
                        text.append(reader.pages[i].extract_text())
                        #text_file.write(reader.pages[i].extract_text())
                    #text_file.close()            
                    short_variants = []            
                    rearrangement = []
                    biomarkers = []
                    copy_number_alterations = []
                    pmi = [] 
                    
                    for i in range(len(text)):                        
                        try:    
                            #rearrangement
                            if text[i].find('Fusions (RNA)') > -1: 
                                rearrangementlist=[]
                                #print(text[i])
                                start = text[i].find('Read Count')
                                end = text[i].find('Gene Fusions')
                                rearrangement.extend(text[i][start+11:end].split('  '))
                                rearrangement=rearrangement[0].split('\n')
                                for j in range(len(rearrangement)):
                                    rearrangementlist.append({
                                        "description": "",
                                        "equivocal": "",
                                        "in_frame": "",
                                        "other_gene": rearrangement[0].replace(' - ', '-').split(' ')[1],
                                        "pos1": rearrangement[0].replace(' - ', '-').split(' ')[2],
                                        "pos2": "",
                                        "status": "",
                                        "supporting_read_pairs": rearrangement[0].replace(' - ', '-').split(' ')[3],
                                        "targeted_gene": rearrangement[0].replace(' - ', '-').split(' ')[0],
                                        "type": "",
                                        "dna_evidence": {
                                        "sample": ""
                                        }})
                                
                                print('\nFusions')
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement']=rearrangementlist
                                #print(rearrangement)    
                        except:
                            None
            
                        if text[i].find('Sample Information') > -1: 
                            #print('\nPMI')
                            #print(text[0])
                            start = text[i].find('Sample Information')
                            end = text[i].find('Note:')
                            #print(text[i][start:end])
                            PATIENT=text[i][start+18:end].strip() 
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split('\n')[0].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split('\n')[1].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split('\n')[3].split(':')[1].strip()
                            try:
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[1]
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[0]
                            except:
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['ReportId'] = MPNo
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TestType'] = PATIENT.split('\n')[12].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = PATIENT.split('\n')[13].split(':')[1].strip()
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = PATIENT.split('\n')[14].split(':')[1].strip()
                            try:
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TumorPurity'] = PATIENT.split('\n')[15].split(':')[1].strip()
                            except:
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = ''
                                basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['ReceivedDate'] = PATIENT.split('\n')[14].split(':')[1].strip()
                            
                            start = text[i].find('Cancer Type:')
                            end = text[i].find('Table of Contents')
                            (text[i][start:end])
                            CancerType = text[i][start+12:end].strip() 
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = CancerType
                            
                        try:   
                            if text[i].find('DNA Sequence') > -1:
                                #print('\nDETECTED VARIANTS')                        
                                #print(text[i])
                                start = text[i].find('Effect Coverage')
                                end = text[i].find('DNA Sequence')
                                short_variants.extend(text[i][start+16:end].strip().split('\n'))
                                #print(len(text[i][start+22:end-5].split(' \n')))
                                #print(text[i][start+22:end-5].split(' \n'))
                        except:
                            None
                            
                        try:    
                            if len(short_variants) > 0:
                                short_variantllist=[]
                                short_variantllist_temp=''
                                for j in range(len(short_variants)):
                                    if len(short_variants[j].split(' ')) > 8 : 
                                        try:
                                            functional_effect = short_variants[j].split(' ')[7]
                                            depth = short_variants[j].split(' ')[8]
                                        except:
                                            depth = ''
                                            functional_effect = ''
                                        if  short_variants[j].split(' ')[6] == 'frameshift':
                                            transcript = 'frameshift Deletion'
                                        else:
                                            transcript = short_variants[j].split(' ')[6]
                                        short_variantllist.append({
                                            "cds_effect": short_variants[j].split(' ')[2],
                                            "depth":depth,
                                            "functional_effect": functional_effect,
                                            "gene": short_variants[j].split(' ')[0],
                                            "percent_reads": short_variants[j].split(' ')[5],
                                            "position": short_variants[j].split(' ')[4],
                                            "protein_effect": short_variants[j].split(' ')[1],
                                            "transcript": transcript,
                                            })
                                    else:
                                       short_variantllist_temp=short_variantllist_temp + short_variants[i]
                                       if len(short_variantllist_temp.split(' ')) > 6:
                                           short_variantllist.append({
                                               "cds_effect": short_variantllist_temp.split(' ')[2],
                                               "depth":short_variantllist_temp.split(' ')[6][len(short_variantllist_temp.split(' ')[6])-4:],
                                               "functional_effect": short_variantllist_temp.split(' ')[6][:len(short_variantllist_temp.split(' ')[6])-4],
                                               "gene": short_variantllist_temp.split(' ')[0],
                                               "percent_reads": short_variantllist_temp.split(' ')[4],
                                               "position": short_variantllist_temp.split(' ')[3],
                                               "protein_effect": short_variantllist_temp.split(' ')[1],
                                               "transcript": short_variantllist_temp.split(' ')[5],
                                               })
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variantllist                                       
                            #print('short_variantllist')
                        except:
                            None
                    with open(os.path.join(dirpath,ReportNo+'_('+MPNo+').xml'), 'w', encoding="utf-8") as output:
                        output.write(xmltodict.unparse(basedict, pretty=True)) 
                    
                    #print(basedict)
                    #print(dirpath+'\\'+ReportNo+'_('+MPNo+').xml')
        except:
            print(dirpath + ' NG')
    os.chdir('..')
    return 'MyeloidAssay2xml done'

### Tumor Mutation Load Assay###
def MutationLoadAssay2xml(PdfPath):
    os.chdir(PdfPath)
    dirlist=glob.glob('*_*')
    #print(len(dirlist))
    for dirpath in dirlist:
        basedict={
            "rr:ResultsReport": {
                "rr:ResultsPayload": {
                    "FinalReport":{
                        "Sample": {
                            "FM_Id": "",
                            "SampleId": "",
                            "BlockId": "",
                            "TRFNumber": "",
                            "TestType": "",
                            "SpecFormat": "",
                            "ReceivedDate": "",
                            },
                        "PMI" : {
                            "ReportId": "",
                            "MRN": "",
                            "FullName": "",
                            "FirstName": "",
                            "LastName": "",
                            "SubmittedDiagnosis": "",
                            "Gender": "",
                            "DOB": "",
                            "OrderingMD": "",
                            "OrderingMDId": "",
                            "Pathologist": "",
                            "CopiedPhysician1": "",
                            "MedFacilName": "",
                            "MedFacilID": "",
                            "SpecSite": "",
                            "CollDate": "",
                            "ReceivedDate": "",
                            "CountryOfOrigin": ""
                           }
                        },
                    "variant-report": {
                        "short_variants": {
                            "short_variant":[]
                            },
                        "copy_number_alterations": {
                            "copy_number_alteration": []
                            },
                        "rearrangements": {
                        	"rearrangement": []
                        },
                        "biomarkers": {
                            "microsatellite_instability": {
                                "status": ""
                            },
                            "tumor_mutation_burden": {
                                "score": ""
                            }
                        }                
                    }
                    }
                }
            }
        ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
        filepathlist =glob.glob(os.path.join(dirpath, "*).pdf"))
        #print(filepathlist)
        #try:        
        for filename in filepathlist:
                #print(filename)            
                reader = PyPDF2.PdfReader(filename)
                #text_file = open("Output.txt", "w", encoding="utf-8")
                text=[]
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                    #text_file.write(reader.pages[i].extract_text())
                #text_file.close()            
                short_variants = []            
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = [] 
                
                for i in range(len(text)):                        
                    try:    
                        #rearrangement
                        if text[i].find('Fusions (RNA)') > -1: 
                            rearrangementlist=[]
                            #print(text[i])
                            start = text[i].find('Read Count')
                            end = text[i].find('Gene Fusions')
                            rearrangement.extend(text[i][start+11:end].split('  '))
                            rearrangement=rearrangement[0].split('\n')
                            for j in range(len(rearrangement)):
                                rearrangementlist.append({
                                    "description": "",
                                    "equivocal": "",
                                    "in_frame": "",
                                    "other_gene": rearrangement[0].replace(' - ', '-').split(' ')[1],
                                    "pos1": rearrangement[0].replace(' - ', '-').split(' ')[2],
                                    "pos2": "",
                                    "status": "",
                                    "targeted_gene": rearrangement[0].replace(' - ', '-').split(' ')[0],
                                    "type": "",
                                    "dna_evidence": {
                                    "sample": ""
                                    }})
                            
                            print('\nFusions')
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement']=rearrangementlist
                            #print(rearrangement)    
                    except:
                        None
        
                    if text[i].find('Sample Information') > -1: 
                        #print('\nPMI')
                        #print(text[0])
                        start = text[i].find('Sample Information')
                        end = text[i].find('Note:')
                        #print(text[i][start:end])
                        PATIENT=text[i][start+18:end].strip() 
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split('\n')[0].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split('\n')[1].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split('\n')[3].split(':')[1].strip()
                        try:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[0]
                        except:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['ReportId'] = MPNo
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TestType'] = PATIENT.split('\n')[12].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = PATIENT.split('\n')[13].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = PATIENT.split('\n')[14].split(':')[1].strip()
                        try:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TumorPurity'] = PATIENT.split('\n')[15].split(':')[1].strip()
                        except:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = ''
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['ReceivedDate'] = PATIENT.split('\n')[14].split(':')[1].strip()
                        
                        start = text[i].find('Cancer Type:')
                        end = text[i].find('Table of Contents')
                        (text[i][start:end])
                        CancerType = text[i][start+12:end].strip() 
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = CancerType
                       
                    if text[i].find('DNA Sequence') > -1:
                        #print('\nDETECTED VARIANTS')                        
                        #print(text[i])
                        start = text[i].find('Effect Coverage')
                        end = text[i].find('DNA Sequence')
                        short_variants.extend(text[i][start+16:end].strip().split('\n'))
                        #print(len(text[i][start+22:end-5].split(' \n')))
                        #print(text[i][start+22:end-5].split(' \n'))
                        
                    if len(short_variants) > 0:
                        short_variantllist=[]
                        short_variantllist_temp=''
                        for j in range(len(short_variants)):
                            if len(short_variants[j].split(' ')) > 8 : 
                                try:
                                    functional_effect = short_variants[j].split(' ')[7]
                                    depth = short_variants[j].split(' ')[8]
                                except:
                                    depth = ''
                                    functional_effect = ''
                                if  short_variants[j].split(' ')[6] == 'frameshift':
                                    transcript = 'frameshift Deletion'
                                else:
                                    transcript = short_variants[j].split(' ')[6]
                                short_variantllist.append({
                                    "cds_effect": short_variants[j].split(' ')[2],
                                    "depth":depth,
                                    "functional_effect": functional_effect,
                                    "gene": short_variants[j].split(' ')[0],
                                    "percent_reads": short_variants[j].split(' ')[5],
                                    "position": short_variants[j].split(' ')[4],
                                    "protein_effect": short_variants[j].split(' ')[1],
                                    "transcript": transcript,
                                    })
                            else:
                               short_variantllist_temp=short_variantllist_temp+short_variants[i]
                               if len(short_variantllist_temp.split(' ')) > 6:
                                   short_variantllist.append({
                                       "cds_effect": short_variantllist_temp.split(' ')[2],
                                       "depth":short_variantllist_temp.split(' ')[6][len(short_variantllist_temp.split(' ')[6])-4:],
                                       "functional_effect": short_variantllist_temp.split(' ')[6][:len(short_variantllist_temp.split(' ')[6])-4],
                                       "gene": short_variantllist_temp.split(' ')[0],
                                       "percent_reads": short_variantllist_temp.split(' ')[4],
                                       "position": short_variantllist_temp.split(' ')[3],
                                       "protein_effect": short_variantllist_temp.split(' ')[1],
                                       "transcript": short_variantllist_temp.split(' ')[5],
                                       })
                                   
        
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variantllist
                        #print('short_variantllist')
                        
                with open(os.path.join(dirpath,ReportNo+'_('+MPNo+').xml'), 'w', encoding="utf-8") as output:
                    output.write(xmltodict.unparse(basedict, pretty=True))            
                #print(dirpath + ' OK')
        #except:
            #print(dirpath + ' NG')
    os.chdir('..')
    return 'MutationLoadAssay2xml done'


import pdfplumber
def FocusAssay2xml(PdfPath):
    os.chdir(os.getcwd() + '/' + PdfPath)
    dirlist = glob.glob('*_*')
    
    for dirpath in dirlist:
        basedict = {  # XML 结构
            "rr:ResultsReport": {
                "rr:ResultsPayload": {
                    "FinalReport": {"Sample": {}, "PMI": {}},
                    "variant-report": {
                        "short_variants": {"short_variant": []},
                        "copy_number_alterations": {"copy_number_alteration": []},
                        "rearrangements": {"rearrangement": []},
                        "biomarkers": {"microsatellite_instability": {"status": ""}, "tumor_mutation_burden": {"score": ""}}
                    }
                }
            }
        }

        try:
            ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
            filepathlist = glob.glob(os.path.join(dirpath, "*.pdf"))
            
            for filename in filepathlist:
                text = []
                with pdfplumber.open(filename) as pdf:
                    for page in pdf.pages:
                        text.append(page.extract_text())
                
                full_text = '\n'.join(text)
                full_text = full_text.replace('-\n', '')  # 處理連字符換行
                full_text = full_text.replace('\n', ' ')  # 連接一般換行
                
                # 解析變異資訊
                short_variants = []
                for line in full_text.split('\n'):
                    if 'p.(' in line or 'c.' in line:  # 處理蛋白與核苷酸變異
                        parts = line.split()
                        if len(parts) >= 4:
                            short_variants.append({
                                "gene": parts[0],
                                "protein_effect": parts[1],
                                "cds_effect": parts[2],
                                "extra_info": ' '.join(parts[3:])
                            })
                basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variants
                
                with open(os.path.join(dirpath, ReportNo + '_(' + MPNo + ').xml'), 'w', encoding="utf-8") as output:
                    output.write(xmltodict.unparse(basedict, pretty=True))
        except Exception as e:
            print(f"Error processing {dirpath}: {e}")
    
    os.chdir('..')
    return 'FocusAssay2xml done'

'''
### creating a pdf reader object Focus Assay ###
def FocusAssay2xml(PdfPath):
    #print('FocusAssay2xml')
    #print(os.getcwd())
    os.chdir(os.getcwd()+'/'+PdfPath)
    #dirlist=glob.glob('M112-10065_(PT23030)*')#Fusions
    dirlist=glob.glob('*_*')
    #print(len(dirlist))
    for dirpath in dirlist:
        basedict={
            "rr:ResultsReport": {
                "rr:ResultsPayload": {
                    "FinalReport":{
                        "Sample": {
                            "FM_Id": "",
                            "SampleId": "",
                            "BlockId": "",
                            "TRFNumber": "",
                            "TestType": "",
                            "SpecFormat": "",
                            "ReceivedDate": "",
                            },
                        "PMI" : {
                            "ReportId": "",
                            "MRN": "",
                            "FullName": "",
                            "FirstName": "",
                            "LastName": "",
                            "SubmittedDiagnosis": "",
                            "Gender": "",
                            "DOB": "",
                            "OrderingMD": "",
                            "OrderingMDId": "",
                            "Pathologist": "",
                            "CopiedPhysician1": "",
                            "MedFacilName": "",
                            "MedFacilID": "",
                            "SpecSite": "",
                            "CollDate": "",
                            "ReceivedDate": "",
                            "CountryOfOrigin": ""
                           }
                        },
                    "variant-report": {
                        "short_variants": {
                            "short_variant":[]
                            },
                        "copy_number_alterations": {
                            "copy_number_alteration": []
                            },
                        "rearrangements": {
                        	"rearrangement": []
                        },
                        "biomarkers": {
                            "microsatellite_instability": {
                                "status": ""
                            },
                            "tumor_mutation_burden": {
                                "score": ""
                            }
                        }                
                    }
                    }
                }
            }
      
        try:    
            ReportNo, MPNo  = dirpath.replace('(', '').replace(')', '').split('_')
            filepathlist =glob.glob(os.path.join(dirpath, "*).pdf"))
            #print(filepathlist)
            
            for filename in filepathlist:
                #print(filename)            
                reader = PyPDF2.PdfReader(filename)
                #text_file = open("Output.txt", "w", encoding="utf-8")
                text=[]
                for i in range(len(reader.pages)):
                    text.append(reader.pages[i].extract_text())
                    #text_file.write(reader.pages[i].extract_text())
                #text_file.close()            
                short_variants = []            
                rearrangement = []
                biomarkers = []
                copy_number_alterations = []
                pmi = []           
                
                for i in range(len(text)):
                    #print(i)
                    #print(text[i])
                    #print(text[i].find('Gene Fusions') > -1)
                    try:
                        #rearrangement
                        
                        if text[i].find('Gene Fusions (RNA)') > -1: 
                            #print(text[i])                    
                            start = text[i].find('ID Locus Read Count')
                            end = text[i].find('Gene Fusions')
                            #print(text[i][start+19:end-5].strip().split('\n'))
                            
                            rearrangement.extend(text[i][start+19:end].strip().split('\n'))
                            rearrangementlist=[]
                            for j in range(len(rearrangement)):
                                rearrangementlist.append({
                            		"description": rearrangement[j].replace(' - ', '-').split(' ')[1].split('.')[0]+'.'+rearrangement[i].replace(' - ', '-').split(' ')[1].split('.')[1],
                            		"other_gene": rearrangement[j].replace(' - ', '-').split(' ')[0].split('-')[0],
                                    "pos1": rearrangement[j].replace(' - ', '-').split(' ')[2].split('-')[0],
                                    "pos2": rearrangement[j].replace(' - ', '-').split(' ')[2].split('-')[1],
                            		"targeted_gene": rearrangement[j].replace(' - ', '-').split(' ')[0].split('-')[1]
                                    })                                                       
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['rearrangements']['rearrangement']=rearrangementlist
                            #print(len(text[i][start+16:end-5].split(' \n')))    
                            #print('rearrangementlist')
                    except:
                        None
                            
                    #print(text[i].find('Copy Number Variations') > -1)
                    try:
                        #copy_number_alterations
                        
                        if text[i].find('Copy Number') > -1: 
                            #print('\ncopy_number_alterations')
                            #print(text[i])
                            start = text[i].find('Locus Copy Number')
                            end = text[i].find('Copy Number Variation')
                            #print(text[i][start+17:end].strip())
                            copy_number_alterations.extend(text[i][start+17:end].strip().split('\n'))
                            copy_number_alterationlist=[]
                            
                                
                            for copy_number_alteration in copy_number_alterations:
                                alterationlist = copy_number_alteration.split(' ')
                                copy_number_alterationlist.append({"copy_number": alterationlist[2],
                                                          "gene": alterationlist[0],
                                                          "position": alterationlist[1]})
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['copy_number_alterations']['copy_number_alteration'] = copy_number_alterationlist
                            #print(len(text[i][start+43:end-4].split(' \n')))
                        #print(copy_number_alterations)
                    except:
                        None

                    #pmi
                    #print(text[i].find('Sample Information') > -1)
                    #:
                    if text[i].find('Sample Information') > -1: 
                        #print('\nPMI')
                        #print(text[0])
                        start = text[i].find('Sample Information')
                        end = text[i].find('Note:')
                        #print(text[i][start:end])
                        PATIENT=text[i][start+18:end].strip() 
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['FullName'] = PATIENT.split('\n')[0].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['Gender'] = PATIENT.split('\n')[1].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['MRN'] = PATIENT.split('\n')[3].split(':')[1].strip()
                        try:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMD'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[1]
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip().split(' ')[0]
                        except:
                            basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['OrderingMDId'] = PATIENT.split('\n')[6].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['ReportId'] = PATIENT.split('\n')[7].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['ReportId'] = PATIENT.split('\n')[8].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['BlockId'] = dirpath
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['TestType'] = PATIENT.split('\n')[12].split(':')[1].strip()
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['Sample']['SpecFormat'] = PATIENT.split('\n')[13].split(':')[1].strip()
                        
                        start = text[i].find('Cancer Type:')
                        end = text[i].find('Table of Contents')
                        (text[i][start:end])
                        CancerType = text[i][start+12:end].strip() 
                        basedict['rr:ResultsReport']['rr:ResultsPayload']['FinalReport']['PMI']['SubmittedDiagnosis'] = CancerType
                    #except:
                        #None
                        
                    #short variants
                    #print(text[i].find('DNA Sequence') > -1)                   
                    if text[i].find('DNA Sequence') > -1:
                        #print('\nDETECTED VARIANTS')                        
                        #print(text[i])
                        start = text[i].find('Effect Coverage')
                        end = text[i].find('DNA Sequence')
                        short_variants.extend(text[i][start+15:end].strip().split('\n'))
                        #print(len(text[i][start+22:end-5].split(' \n')))
                        #print(text[i][start+22:end-5].split(' \n'))
                        
                    if len(short_variants) > 0:
                        short_variantllist=[]
                        for j in range(len(short_variants)):
                            if len(short_variants[j].split(' '))==9:                                
                                short_variantllist.append({
                                    "cds_effect": short_variants[j].split(' ')[2],
                                    "depth": short_variants[j].split(' ')[8],
                                    "functional_effect": short_variants[j].split(' ')[7],
                                    "gene": short_variants[j].split(' ')[0],
                                    "percent_reads": short_variants[j].split(' ')[5],
                                    "position": short_variants[j].split(' ')[4],
                                    "protein_effect": short_variants[j].split(' ')[1],
                                    "transcript": short_variants[j].split(' ')[6],
                                    }) 

                        basedict['rr:ResultsReport']['rr:ResultsPayload']['variant-report']['short_variants']['short_variant'] = short_variantllist
                        #print('short_variantllist')
                        
                with open(os.path.join(dirpath,ReportNo+'_('+MPNo+').xml'), 'w', encoding="utf-8") as output:
                    output.write(xmltodict.unparse(basedict, pretty=True))            
                #print(dirpath + ' OK')           
        except:
            None
            #print(dirpath + ' NG')            
    os.chdir('..')
    return 'FocusAssay2xml done'
'''
### 轉出PDF 至 目錄 ###
def pdf2dir(PdfPath, root):
    os.chdir(PdfPath)
    try:
        dirlist = glob.glob('*_*')
        for dirpath in dirlist:
            try:
                ReportNo, MPNo = dirpath.replace('(', '').replace(')', '').split('_')
                filepathlist = glob.glob(os.path.join(dirpath, "*).pdf"))
                print(filepathlist)
                
                for filename in filepathlist:
                    # 源文件路径
                    source = filename
                    # 目标文件路径
                    destination_dir = os.path.join(root, 'gene')
                    destination = os.path.join(destination_dir, os.path.basename(filename))

                    # 如果目标目录不存在，则创建它
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir)
                        print(f"创建目录: {destination_dir}")

                    # 复制源文件到目标位置
                    dest = shutil.copyfile(source, destination)
                    print(f"{dirpath} OK")
            except ValueError as ve:
                print(f"处理目录 {dirpath} 时发生错误: {ve}")
            except Exception as e:
                print(f"处理文件 {filename} 时发生未预期的错误: {e}")
    except Exception as e:
        print(f"处理目录列表时发生错误: {e}")
    os.chdir('..')
    return 'pdf2dir done'