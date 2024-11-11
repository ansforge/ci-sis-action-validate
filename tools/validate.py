import requests
import xml.etree.ElementTree as ET
import lxml
import base64
import os
import sys
import glob 
import time
import hl7
from hl7apy.parser import parse_message

class NoValidateurException(Exception):
    "Pas de validateur pour le fichier"
    pass

class ValidateException(Exception):
    "Erreur à la validation"
    pass

class GetReportException(Exception):
    "Erreur à la récupération du rapport"
    pass

class TransformReportException(Exception):
    "Erreur à la transformation du rapport"
    pass

github_action_path = sys.argv[1] 
dir_path_exemple =  sys.argv[2] 
file_output = sys.argv[3] 

#URL d'accés à l'API de gazelle
url = 'https://interop.esante.gouv.fr/evs/rest/validations'


#Function de validation
def validate(fileName, validationServiceName, validationserviceValidator):
    time.sleep(5)
    #Recuperation du contenu du fichier 
    with open(fileName, mode="rb") as validate_file:
        contents = validate_file.read()
    docbase64  = base64.b64encode(bytes(contents)).decode('ascii')    

    #Creation du contenu XML pour l'API
    validation = ET.Element('validation')
    validation.set("xmlns", "http://evsobjects.gazelle.ihe.net/")
   
    validationService = ET.SubElement(validation, 'validationService')
    validationService.set("xmlns", "http://evsobjects.gazelle.ihe.net/")
    validationService.set("name", validationServiceName )
    validationService.set("validator", validationserviceValidator)

    validationObject = ET.SubElement(validation, 'object')
    validationObject.set("xmlns", "http://evsobjects.gazelle.ihe.net/")
    validationObject.set("originalFileName", fileName)

    validationContent = ET.SubElement(validationObject, 'content')
    validationContent.text = str(docbase64)
    tree = ET.ElementTree(validation)
    validate_data = ET.tostring(validation)

    #Appel de la validation
    try:
        headers = {'Content-Type': 'application/xml'}
        res =  requests.post(url, data=validate_data, headers=headers)
        locationRapport = (res.headers["X-Validation-Report-Redirect"])
    except Exception as e:   
        print(e)  
        raise ValidateException
    return locationRapport

#Fonction de récupération du rapport de validation
def getReport(location_report):
    try:
        headers = {'accept': 'application/xml'}
        request =  requests.get(f"{location_report}?severityThreshold=WARNING", headers=headers)
    except Exception as e:   
        print(e)  
        raise GetReportException    
    return request

#Fonction de transdormation du rapport de validation
def transformReport(rapport, github_action_path, file_output,nameFile, time):
    try:   
        from lxml import etree
        parser = etree.ETCompatXMLParser()
        xsl_path = f"{github_action_path}/tools/svr-to-table-tr.xsl"
        xsl = etree.parse(xsl_path)
        dom = etree.fromstring(rapport.content, parser)

        transform = etree.XSLT(xsl)
        resultHtml= transform(dom,nameFile=etree.XSLT.strparam(nameFile),elapsedTime=etree.XSLT.strparam(time))
        print(resultHtml,file=open(file_output, "a"))
    except Exception as e:   
        print(e)  
        raise TransformReportException    
    
#Fonction qui permet de récuperer les validateurs
def findValidateur (FileInput):
    validationService = ""
    validationValidator = ""    
    with open(FileInput, errors='ignore') as fileIn:
        strInputFile = fileIn.read()    


        # ************************ DICOM*********************************************        
        if '.dcm' in FileInput.lower()  :
            validationService = "Dicom3tools"
            validationValidator = "DICOM Standard Conformance"

        # ************************ METADATA*********************************************        
        if 'METADATA.XML' in FileInput :
            validationService = "Model-based XDS Validator"
            validationValidator = "ASIP XDM ITI-32 FR Distribute Document Set on Media"

        # ************************ CDA *********************************************        
        if '<ClinicalDocument' in strInputFile :
            validationService = "Schematron Based CDA Validator"
            validationValidator = ".Structuration minimale des documents de santé v1.16"

        # ************************ HL7V2*********************************************
        if 'MSH|' in strInputFile :
            parsed_message = parse_message(strInputFile)
            print(parsed_message)
     

            validationService = "Gazelle HL7v2.x validator"
            
            if '2.1^CISIS_CDA_HL7_V2'  in strInputFile :
                if 'ORU^R01^ORU_R01' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.19"
                if 'MDM^T02^MDM_T02' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.24"
                if 'MDM^T04^MDM_T02' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.25"
                if 'MDM^T10^MDM_T02' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.21"
        
            if '1.1^CISIS_CDA_HL7_LPS'  in strInputFile :
                if 'MDM^T02^MDM_T02' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.20"
                if 'MDM^T04^MDM_T02' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.22"
                if 'MDM^T10^MDM_T02' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.23"

            if 'ACK^'  in strInputFile :
                if '2.6' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.27"
                if '2.5' in strInputFile :
                    validationValidator = "1.3.6.1.4.1.12559.11.36.8.3.26"


            if '2.11~IHE_FRANCE-2.11-PAM'  in strInputFile :
                    validationValidator = "2.16.840.1.113883.2.8.3.1.1"
    if ((validationService == "") and (validationValidator == "")) :
         raise NoValidateurException
    return validationService, validationValidator
  


print("source : " +dir_path_exemple)
print("output : " +     file_output)    
print("<table><tr> <th>Fichier</th> <th>Etat</th> <th>validateur</th> <th>Nombre d'erreur</th> <th>Nombre de warning</th> <th>Temps</th> <th>Nombre de contrainte</th> </tr>" ,file=open(file_output, "a"))    

for p in glob.iglob(dir_path_exemple+'/**/*.*', recursive=True):
    if(os.path.isfile(p)):
        try:     
            print ("" + p ) 
            validationService,  validationValidator = findValidateur(p)
            print("- Validation : " + validationService + " :" +  validationValidator)            
            start_time = time.time()
            locationRepport = validate(p, validationService, validationValidator)
            end_time = time.time()
            timeValidation = str(end_time - start_time)
            rapport = getReport(locationRepport)
            transformReport(rapport, github_action_path, file_output, p, timeValidation)
            print("- Location report "  + locationRepport)
        except NoValidateurException as e:
            print("	 <tr><td>" + p  + "</td><td> Pas de validateur trouvé  </td> <td></td> <td></td> <td></td> <td></td> <td></td>  </tr>" ,file=open(file_output, "a"))    
            print("- Pas validateur")  
        except ValidateException as e:
            print("	 <tr><td>" + p  + "</td><td> Erreur à la validation </td> <td></td> <td></td> <td></td> <td></td> <td></td>  </tr>" ,file=open(file_output, "a"))    
            print("- Erreur à la validation")            
        except GetReportException as e:
            print("	 <tr><td>" + p  + "</td><td> Erreur à la recuperation du rapport </td> <td></td> <td></td> <td></td> <td></td> <td></td>  </tr>" ,file=open(file_output, "a"))    
            print("- Erreur à la récuperation du rapport")          
        except TransformReportException as e:
            print("	 <tr><td>" + p  + "</td><td> Erreur à la transformation du rapport </td> <td></td> <td></td> <td></td> <td></td> <td></td>  </tr>" ,file=open(file_output, "a"))    
            print("- Erreur à la transformation  du rapport")          
        except Exception as e:
            print(e)
            print("	 <tr><td>" + p  + "</td><td> Erreur  </td> <td></td> <td></td> <td></td> <td></td> <td></td>  </tr>" ,file=open(file_output, "a"))    
            print("- Erreur   : " + p)     


            

print("</table>" ,file=open(file_output, "a"))    
