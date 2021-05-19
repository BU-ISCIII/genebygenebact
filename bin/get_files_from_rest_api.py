#!/usr/bin/env python3
import argparse
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import requests
from urllib.parse import urlparse
from utils_get_files_from_rest_api.common_functions import *
from urllib.request import urlopen

#from rest_api_class.model import *

# -output_dir /srv/project_wgmlst/pasteur_schema schema -api_url pasteur_listeria -schema_name cgMLST1748 
# -out /srv/tmp/ schema --api_url enterobase --schema_name wgMLST --database ecoli --api_key  API_KEY_ENTEROBASE 

def check_arg(args=None):
    text_description = str('This program will download the locus fasta files for a selected schema using the API REST request. So far only pubMLST, bigsdb and EnteroBase are supported.')
    
    parser = argparse.ArgumentParser(prog = 'get_files_from_rest_api.py', 
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description = text_description)
    parser.add_argument('-v' ,'--version', action='version', version='%(prog)s 0.1.3')
    
    parser.add_argument('-out','--output_dir', help = 'Directory where the result files will be stored')
    subparser = parser.add_subparsers(help = 'interactive/no_interactive are the 2 available options to download the locus', dest = 'chosen_method')
    #subparser = parser.add_subparsers(help = 'interactive/schema are the 2 available options to download the locus', dest = 'chosen_method')

    ## Como se indica arriba en el subparser, hay dos formas de descargarse los esquemas, pued ser "interactive" o "schema". A continuación se indican los argumentos para cada opción, aunque no acabo de entenderlo:

    interactive_parser = subparser.add_parser('interactive', help = 'interactive downloads the schema for pubMLST and bigsdb ') ## ??? Pero no de Enterobase?
#    interactive_parser.add_argument('-db','--db_url', choices = ['pubMLST',''] ,help = 'database url to download the locus files. "pubMLST" value can be used as nick name to connect to pubMLST database') ## solo se puede acceder a pubmlst?
    interactive_parser.add_argument('-api','--api_url', required = True, help = 'database url to download the locus files. "pubMLST" value can be used as nick name to connect to pubMLST database') ## solo se puede acceder a pubmlst?
#    interactive_parser.add_argument('-out','--output_dir',help = 'Directory where the result files will be stored')
    interactive_parser.add_argument('-ftyp', '--file_type', required = True, help = 'File type to download.'
                                                                                + 'scheme: Download schema file.'
                                                                                + 'profile: Download ST profile file.')


    #schema_parser = subparser.add_parser('schema', help = 'Download the locus fasta files for a given schema')
    schema_parser = subparser.add_parser('no_interactive', help = 'Download the locus fasta files for a given schema')
    schema_parser.add_argument('-api', '--api_url', required = True, help = 'Nick name to connect to REST API. Accepted values are: bigsdb, pubMLST') ## por qué pasteur listeria solo?
    schema_parser.add_argument('-org', '--organism_id', required = True, help = 'Organism ID whose schema or profile is going to be donwloaded') ## schema_name y database no es lo mismo? El nombre del esquema pero para distinta base de datos?
    schema_parser.add_argument('-db', '--schema_database', required = True, help = 'ID for schema database')
    schema_parser.add_argument('-styp', '--schema_type', required = True, help = 'ID for schema type to download')
    schema_parser.add_argument('-ftyp', '--file_type', required = True, help = 'File type to download.'
                                                                                + 'scheme: Download schema file.'
                                                                                + 'profile: Download ST profile file.')

   # schema_parser.add_argument('-db', '--database', help = 'Database name required for enterobase', required= False) ## la api de enterobase no furula
   # schema_parser.add_argument('-key', '--api_key', help = 'File name with the Token Key for enterobase', required= False) ## la api de enterobase no furula
    
    return parser.parse_args()

"""
def download_locus_enterobase (api_url, api_key, database, schema, out_dir):
    '''
    Description:
        Function will check if all projects given in the project list
        are defined on database
        Return True if all are in , False if not
    Input:
        project_list    #list of the project to check
    variables:
        logger # logging object to write in the log file
    Return:
        list of the downloaded loci
    '''
    locus_downloaded_list = []
    enterobase_object = EnterobaseApi(api_url, api_key, database, schema)
    try:
        locus_addresses = enterobase_object.get_locus_in_schema()
    except  urllib.error.URLError as e :         
        string_text = str(e) + '  '+ str(e.fp.read().decode("utf-8"))
        logging_errors(string_text, False , True )
        raise
        
    if len(locus_addresses) > 0:
        print('Start downloading the fasta files for the schema')
        for file_name, download_address  in locus_addresses.items():
            try:
                enterobase_object.download_fasta_locus (download_address, out_dir, file_name)
                locus_downloaded_list.append(file_name)
            except Exception as e:
                print ('Exception error ' , e)
                continue
        print('Download completed')
    else:
        print('Error when fetching the addresses to download locus')
    return locus_downloaded_list
"""

def get_url_files_to_download ( api_url, organism_id, schema_database, schema_type, file_type, logger): ### se repiten pasos que en la opción interactiva hace sueltos, condensar?
    
    #Pasan a ser equivalentes al número de la elección (choice):
    #organism_id 
    #schema_database
    #schema_type

    schema_db = get_database_options (api_url, logger)
####    r = requests.get(api_url)
####    logger.info('Connecting to %s to get the schemas' , api_url)
####    if r.status_code != 200 :
####        logger.error('Unable to connect to %s ', api_url)
####        return False
####    schema_db = r.json()

    schema_url = ''
    print("schema_db: ", schema_db, '\n') ## borrar
    print("schema_db type: ", type(schema_db), '\n') ## borrar
 #   print("schema_db['schemes']: ", schema_db['schemes'], '\n') ## borrar
 #   print("schema_db['schemes'] len: ", len(schema_db['schemes']), '\n') ## borrar
  #  for index in range(len(schema_db['schemes'])):
    
    for index_1 in range(len(schema_db)):

        print("index_1: ", index_1, '\n') #borrar
        print("index_1 type: ", type(index_1), '\n') # borrar
      #  print("Comparando organism_id indicado con schema_db['schemes'][index]['description']: " ,schema_db['schemes'][index]['description'], '\n')
       # print("Comparando organism_id indicado con schema_db['schemes'][index]['name']: " ,schema_db['schemes'][index]['name'], '\n')
        #if organism_id == schema_db['schemes'][index]['description'] :
        ##if organism_id == schema_db['schemes'][index]['name'] :
          ##  schema_index = schema_db['schemes'][index]['scheme']
        
        print("organism_id: ", organism_id, '\n') # borrar
        print("organism_id type: ", type(organism_id), '\n') # borrar
        if organism_id == index_1 :
            print('Ha entrado a organism_id == index_1', '\n') # borrar
            print("schema_db[index]: ", schema_db[index_1], '\n') ## borrar
           # schema_databases = schema_db[index]['databases']
          #  print("schema_index: schema_db[index]['databases']: ", schema_databases, '\n')
            for index_2 in range(len(schema_db[index_1]['databases'])) :
                print(index_2, " : ", schema_db[index_1]['databases'][index_2], '\n' )
                
                if schema_database == index_2:
                    schema_url = schema_db[index_1]['databases'][index_2]['href']
                    break

    if schema_url == '' :
        logger.error('The given organism ID, %s, it is not included in the schema database', organism_id)
        return False
    print("Se va a hacer un request de la base de datos elegida: ", schema_database, '\n') # borrar
    
    r_json = get_database_options (schema_url, logger)
####    r = requests.get(schema_url)
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json 1: ", r_json, '\n') # borrar

    r_json = get_database_options (r_json['schemes'], logger)
####    r = requests.get(r_json['schemes'])
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json 2: ", r_json, '\n') # borrar

    schema_url = ''
    for index_3 in range(len(r_json['schemes'])):
        if schema_type == index_3:
            schema_url = r_json['schemes'][index_3]['scheme']

    if schema_url == '' :
        logger.error('The given schema type ID, %s, it is not included in the schema database', schema_type)
        return False

    r_json = get_database_options (schema_url, logger)
####    r = requests.get(schema_url)
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json 3: ", r_json, '\n') # borrar


    if file_type == 'schema':
        print("Ha entrado a if filey_type == schema", '\n') ## borrar
        locus_url_list = []
        for loci in range(r_json['locus_count']) :
            locus_url_list.append(r_json['loci'][loci])
        
        print("locus_url_list: ", locus_url_list, '\n') # borrar
        #logger.info('The locus list for the schema %s has been successfully fetched ', organism_id)
        logger.info('The locus list has been successfully fetched ')

        return locus_url_list


    elif file_type == 'profile':
        print("Ha entrado a if filey_type == profile", '\n') ## borrar
        if 'profiles_csv' in r_json:
            profiles_url = r_json['profiles_csv']
            print("profiles_url: ", profiles_url, '\n') ## borrar
            logger.info('The ST profile URL has been successfully fetched ')
        else:
            print("Ha entrado a profiles_url = '' ") ## borrar
            profiles_url = ''
            logger.info('There is not ST profile available for schema type with ID %s', schema_type)
            
        return profiles_url


# Función antes de intentar utilizar el número de choice para llegar a la url de descarga en lugar de los nombres ya que hay nombres con espacios
"""
def get_url_files_to_download ( api_url, organism_id, schema_database, schema_type, file_type, logger): ### se repiten pasos que en la opción interactiva hace sueltos, condensar?
    
    schema_db = get_database_options (api_url, logger)
####    r = requests.get(api_url)
####    logger.info('Connecting to %s to get the schemas' , api_url)
####    if r.status_code != 200 :
####        logger.error('Unable to connect to %s ', api_url)
####        return False
####    schema_db = r.json()

    schema_url = ''
    print("schema_db: ", schema_db, '\n') ## borrar
    print("schema_db type: ", type(schema_db), '\n') ## borrar
 #   print("schema_db['schemes']: ", schema_db['schemes'], '\n') ## borrar
 #   print("schema_db['schemes'] len: ", len(schema_db['schemes']), '\n') ## borrar
  #  for index in range(len(schema_db['schemes'])):
    
    for index_1 in range(len(schema_db)):
      #  print("Comparando organism_id indicado con schema_db['schemes'][index]['description']: " ,schema_db['schemes'][index]['description'], '\n')
       # print("Comparando organism_id indicado con schema_db['schemes'][index]['name']: " ,schema_db['schemes'][index]['name'], '\n')
        #if organism_id == schema_db['schemes'][index]['description'] :
        ##if organism_id == schema_db['schemes'][index]['name'] :
          ##  schema_index = schema_db['schemes'][index]['scheme']
        if organism_id == schema_db[index_1]['name'] :
            print("schema_db[index]: ", schema_db[index_1], '\n') ## borrar
           # schema_databases = schema_db[index]['databases']
          #  print("schema_index: schema_db[index]['databases']: ", schema_databases, '\n')
            for index_2 in range(len(schema_db[index_1]['databases'])) :
                print(index_2, " : ", schema_db[index_1]['databases'][index_2], '\n' )
                
                if schema_database == schema_db[index_1]['databases'][index_2]['name']:
                    schema_url = schema_db[index_1]['databases'][index_2]['href']
                    break

    if schema_url == '' :
        logger.error('The given schema name, %s, it is not included in the schema database', organism_id)
        return False
    print("Se va a hacer un request de la base de datos elegida: ", schema_database, '\n') # borrar
    
    r_json = get_database_options (schema_url, logger)
####    r = requests.get(schema_url)
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json 1: ", r_json, '\n') # borrar

    r_json = get_database_options (r_json['schemes'], logger)
####    r = requests.get(r_json['schemes'])
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json 2: ", r_json, '\n') # borrar

    schema_url = ''
    for index_3 in range(len(r_json['schemes'])):
        if schema_type == r_json['schemes'][index_3]['description']:
            schema_url = r_json['schemes'][index_3]['scheme']

    if schema_url == '' :
        logger.error('The given schema type %s, it is not included in the schema database', organism_id)
        return False

    r_json = get_database_options (schema_url, logger)
####    r = requests.get(schema_url)
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json 3: ", r_json, '\n') # borrar


    if file_type == 'schema':
        print("Ha entrado a if filey_type == schema", '\n') ## borrar
        locus_url_list = []
        for loci in range(r_json['locus_count']) :
            locus_url_list.append(r_json['loci'][loci])
        
        print("locus_url_list: ", locus_url_list, '\n') # borrar
        logger.info('The locus list for the schema %s has been successfully fetched ', organism_id)
        
        return locus_url_list


    elif file_type == 'profile':
        print("Ha entrado a if filey_type == profile", '\n') ## borrar
        profiles_url = r_json['profiles_csv']
        print("profiles_url: ", profiles_url, '\n') ## borrar
        logger.info('The ST profile URL for %s has been successfully fetched ', organism_id)
        
        return profiles_url
"""

"""
## añadiendo función para la descarga de perfil ST de pubmlst y bigsdb-pasteur. Fusionar con la función de obtención de locus? Ponerlo como script aparte?No, no? Porque habría que copiar 
## casi todo lo de este script
## hacer que para esquemas se meta directamente en la URL del terminado en ISOLATES y para profile que se meta automaicamente en isolate?
def get_ST_profile( api_url, organism_id, schema_database, schema_type, logger): ### se repiten pasos que en la opción interactiva hace sueltos, condensar?
    
    schema_db = get_database_options (api_url, logger)
####    r = requests.get(api_url)
####    logger.info('Connecting to %s to get the schemas' , api_url)
####    if r.status_code != 200 :
####        logger.error('Unable to connect to %s ', api_url)
####        return False
####    schema_db = r.json()

    schema_url = ''
    print("schema_db: ", schema_db, '\n') ## borrar
    print("schema_db type: ", type(schema_db), '\n') ## borrar
 #   print("schema_db['schemes']: ", schema_db['schemes'], '\n') ## borrar
 #   print("schema_db['schemes'] len: ", len(schema_db['schemes']), '\n') ## borrar
  #  for index in range(len(schema_db['schemes'])):
    
    for index_1 in range(len(schema_db)):
      #  print("Comparando organism_id indicado con schema_db['schemes'][index]['description']: " ,schema_db['schemes'][index]['description'], '\n')
       # print("Comparando organism_id indicado con schema_db['schemes'][index]['name']: " ,schema_db['schemes'][index]['name'], '\n')
        #if organism_id == schema_db['schemes'][index]['description'] :
        ##if organism_id == schema_db['schemes'][index]['name'] :
          ##  schema_index = schema_db['schemes'][index]['scheme']
        
        if organism_id == schema_db[index_1]['name'] :
            print("schema_db[index]: ", schema_db[index_1], '\n') ## borrar
           # schema_databases = schema_db[index]['databases']
          #  print("schema_index: schema_db[index]['databases']: ", schema_databases, '\n')
            
            ### AQUÍ EN DATABASES SE ELEGIRÍA ISOLATES O SEQDEF
            for index_2 in range(len(schema_db[index_1]['databases'])) :
                print(index_2, " : ", schema_db[index_1]['databases'][index_2], '\n' )
                
                if schema_database == schema_db[index_1]['databases'][index_2]['name']:
                    schema_url = schema_db[index_1]['databases'][index_2]['href']
                    break

    if schema_url == '' :
        logger.error('The given schema name, %s, it is not included in the schema database', organism_id)
        return False
    print("Se va a hacer un request de la base de datos elegida: ", schema_database, '\n') # borrar
    
    r_json = get_database_options (schema_url, logger)
####    r = requests.get(schema_url)
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json: ", r_json, '\n') # borrar

    r_json = get_database_options (r_json['schemes'], logger)
####    r = requests.get(r_json['schemes'])
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json: ", r_json, '\n') # borrar

    schema_url = ''
    for index_3 in range(len(r_json['schemes'])):
        if schema_type == r_json['schemes'][index_3]['description']:
            schema_url = r_json['schemes'][index_3]['scheme']

    if schema_url == '' :
        logger.error('The given schema type %s, it is not included in the schema database', organism_id)
        return False

    r_json = get_database_options (schema_url, logger)
####    r = requests.get(schema_url)
####    if r.status_code != 200 :
####        return False
####    r_json = r.json()
    print("r_json: ", r_json, '\n') # borrar

    profiles_url = r_json['profiles_csv']
    
    logger.info('The ST profile URL for %s has been successfully fetched ', organism_id)
    
    return profiles_url

"""




### Mirar bien dónde poner los comentarios logger, en esta función o en la función que la llama

def download_fasta_locus (locus_list, output_dir, logger):
    download_counter = 0
    for loci in locus_list :
        print("loci ", loci, '\n') # borrar
        tmp_split = loci.split('/')
        loci_name = tmp_split[-1]
        print("loci_name: ", loci_name, '\n') # borrar
        r = requests.get(loci + '/alleles_fasta')
        print("r.status_code: ", r.status_code, '\n') # borrar
        
        if r.status_code != 200 :
            logger.error('Unable to download the fasta file for allele %s ', loci_name)
        else :
            fasta_alleles = r.text
            fasta_file =  os.path.join(output_dir, str(loci_name + '.fasta'))
            with open (fasta_file , 'w') as fasta_fh :
                fasta_fh.write(fasta_alleles)
            download_counter += 1
    if download_counter == len(locus_list) :
        logger.info('All alleles have been successfully downloaded and saved on %s', output_dir)
        return True 
    else :
        return False

### meter nombre de organismo y tipo de esquema para construir el nombre del csv donde se va a guardar el ST?
def download_csv_profile (profiles_url, output_dir, logger):
    tmp_split = profiles_url.split('/')
    profile_name = tmp_split[-1] ## si meto el organismo y el tipo de equema no tengo que sacar esto, porque esto es para el nombre del archivo donde se van a guardar los STs
    print("profile_name: ", profile_name, '\n') # borrar
    r = requests.get(profiles_url)
    print("r.status_code: ", r.status_code, '\n') # borrar
    
    ### LLAMAR A FUNCIÓN QUE CHECKEA DESCARGA CORRECTA
    if r.status_code != 200 :
        logger.error('Unable to download the profile CSV file')
        return False
    else :
        csv_STs = r.text
        csv_file =  os.path.join(output_dir, str(profile_name + '.csv'))
        with open (csv_file , 'w') as csv_fh :
            csv_fh.write(csv_STs)
        return True

"""
api_url = {'bigsdb':'http://api.bigsdb.pasteur.fr' ,
           'pasteur_listeria': 'http://api.bigsdb.pasteur.fr/db/pubmlst_listeria_seqdef_public/schemes' ,
           'pubMLST_neisseria' : 'http://rest.pubmlst.org/db/pubmlst_neisseria_isolates/isolates',
           'pubMLST' : 'http://rest.pubmlst.org/',
           'enterobase': 'http://enterobase.warwick.ac.uk/api/v2.0/'}
"""

api_url = {'bigsdb':'http://api.bigsdb.pasteur.fr',
           'pubMLST': 'http://rest.pubmlst.org/',
           'enterobase': 'http://enterobase.warwick.ac.uk/api/v2.0/'} ## enterobase API no tiene soporte


def url_validation (url): # No es necesaria esta función si se compara la URL de API proporcionada con los valores del diccionario api_url
    result = urlparse(url)
    # El módulo urllib.parse proporciona funciones para manipular URLs y sus componentes, para descomponerlas o construirlas.
    # El valor de retorno de la función urlparse() es un objeto ParseResult que actúa como un tuple con seis elementos.
    # Las partes de la URL disponibles a través de la interfaz de la tupla son los parámetros de esquema (scheme (http)), ubicación de red (netloc (lo que va detrás de http)), ruta, segmento de ruta (separados de la ruta por un punto y coma), consulta y fragmento.
    return result.scheme and result.netloc

# No es necesaria esta función si se compara la URL de API proporcionada con los valores del diccionario api_url
def validate_db_connection (url) : ## valida que se pueda abrir la url accediendo al sitio web
    
    try:
        urlopen(url)
        return True
    except URLError:
    
        return False


def print_menu (value_list, db_url) :
    
    invalid_selection = True ### se inicializa invalid_selection como True
    while invalid_selection :
        os.system('clear') ### The line os. system('clear') tells Python to talk to the operating system, and ask the system to run the clear command. You can see this same thing by typing clear in any open terminal window. On a technical note, the screen is not actually erased when you enter the clear command.
        
        print ('You are connected to database : ', db_url)
        print ('\n')
        print(30 * '-', ' MENU ', 30 * '-','\n')
        for index, value in enumerate(value_list) :
            print(index, 2*'', value)
        print ('\n q  To Quit')
        choice_value = input(' Enter your selection  >>  ') ### choice_value toma el valor de la elección que introduzca el usuario en la terminal de la lista de opciones ofrecidas por la base de datos
        if choice_value == 'q' or choice_value == 'Q' :
            invalid_selection = False 
        else :
            try:
                value_integer = int(choice_value)
            except:
                continue
            if  0 <= value_integer <= len(value_list)-1 :
                invalid_selection = False
    
    return choice_value


def get_database_options (db_url, logger):
    r = requests.get(db_url) ###se accede a la url y se guarda la info en el objeto r 
    print("r tras requests.get(db_url): ", r, '\n') ## borrar
    logger.info('Connecting to %s to get the options.' , db_url)
    if r.status_code != 200 : ### response.status_code returns a number that indicates the status (200 is OK, 404 is Not Found)
        logger.error('Unable to connect to %s ', db_url)
        return False
    print("r.json() tras requests.get(db_url): ", r.json(), '\n') ## borrar
    return r.json() ### se devuelve la info de la url en formato json


if __name__ == '__main__' :

    if len (sys.argv) == 1 :
        print('Usage: get_files_from_rest_api.py [OPTION] ')
        print('Try  get_files_from_rest_api.py --help for more information.')
        exit(2)
    arguments = check_arg(sys.argv[1:])
    start_time = datetime.now()

    ## Create output directory
    try:
        create_directory (arguments.output_dir)
    except OSError as e:
        print('Unable to create the directory \n')
        print(e)
        exit(1)
    
    ## Create log file
    log_folder = arguments.output_dir
    log_name = 'rest_api.log'
    
    try:
        logger = open_log (log_name, log_folder)
    except OSError as e:
        print('Unable to create the log file \n')
        print(e)
        exit(1)
    

    # Check if provided nick name to connect to database REST API to download the locus files is accepted
    if arguments.api_url in api_url : # si la clave? que se ha indicado se encuentra en el diccionario api_url (aunque no entiendo que ponga solo pubmlst en el mensaje de help) entonces se obtiene la url que es el valor de la key en el diccionario api_url
        db_url = api_url[arguments.api_url]
        print("db_url: ", db_url, '\n') ## borrar
    
    # If api_url is not an accepted nick name, check if it is a valid and accepted API URL
    else :
        if arguments.api_url in api_url.values():
            db_url = arguments.api_url
        else :
            print ('The requested REST API it is not allowed \n')
            exit (2)

            #print("Ha entrado en el else: ", '\n')
###            valid_url = url_validation (arguments.api_url) ### si no se encuentra la clave introducida dentro del diccionario api_url lo que se hace es validar la url que se ha introducido por la terminal sacando el scheme y el netloc            
###            if not valid_url : ### si no se obtiene resultado tras aplicar la url_validation, el formato de la url introducida por terminalno es válida y se finaliza la ejecución del programa
###                print ('Invalid url format')
###                exit(2)
###            else: ## en caso de que el formato de la url introducida (no habiendo introducido clave (pubmlst, etc) y no habiendo tomado la url del diccionario de api_url) sea válido, se toma como db_url dicha url
###                db_url = arguments.api_url
        
        # Check database connection using api url
###        if not validate_db_connection(db_url) : ## se comprueba que es posible la conexión al sitio web con la url 
###            print ('Unable to connect to database ', db_url)
###            exit(1)
        
    ## Interactive schema download method chosen
    if arguments.chosen_method =='interactive' :

        # Get available bacteria options to download databases 
        #if not 'db' in db_url :
        #if not 'xx' in db_url :
        db_output = get_database_options (db_url, logger) ### se obtienen las opciones/info de la base de datos indicada (pubmlst, etc)
        option_list = []
        for index in range( len(db_output)) :
            option_list.append(db_output[index]['description']) ### por cada opción de la base de datos se guarda la descripción en la lista option_list
        
        # Interactive user database choice
        choice = print_menu(option_list, db_url) ### se ejecuta función para printear las opciones y que el usuario elija 
        
        # If choice = q/Q exit the program
        if choice == 'q' or choice == 'Q' :
            print ('Exiting the program. Returning to shell prompt')
            exit(0)

        # Get available databases options list to download for chosen bacteria
        else :
            db_selection = db_output[int(choice)]['databases']
            option_list = []
            for index in range (len(db_selection)) :
                option_list.append(db_selection[index]['description'])

            # Interactive user database choice        
            choice = print_menu(option_list, db_url)

            # If choice = q/Q exit the program
            if choice == 'q' or choice == 'Q' :
                print ('Exiting the program. Returning to shell prompt')
                exit(0)

            else :
                # Get the schemas href
                db_url = db_selection[int(choice)]['href']
                db_output = get_database_options (db_url, logger)
                
                # Get schemas types list to choose
                option_list = []
                ###if 'schemes' in db_output : ### comento este if porque no tiene sentido que se mire si 'schemes' en db_output si luego fuera del if se mira for index in range(len(deb_output['schemes']))
                db_url = db_output['schemes']
                db_output = get_database_options (db_url, logger)
                for index in range(len(db_output['schemes'])) :
                    option_list.append(db_output['schemes'][index]['description'])
                
                # Interactive user schema type choice        
                choice = print_menu(option_list, db_url)

                # If choice = q/Q exit the program
                if choice == 'q' or choice == 'Q' :
                    print ('Exiting the program. Returning to shell prompt')
                    exit(0)

                # Get the allele list for the schema type chosen
                db_url = db_output['schemes'][int(choice)]['scheme']
                db_output = get_database_options (db_url, logger)

                if arguments.file_type == 'schema':
                    locus_list =[]
                    for index in range(len(db_output['loci'])):
                        locus_list.append(db_output['loci'][index])
                    print("locus_list: ", locus_list, '\n') ## borrar

                    # Get fasta file for each locus
                    fasta_locus = download_fasta_locus (locus_list, arguments.output_dir, logger)
                    if not fasta_locus :
                        logger.error('Locus list for schema cannot be fetched ')
                        print('Some of the alleles files cannot be downloaded. Check log file')
                    else:
                        logger.info('All alleles have been successfully downloaded and saved on %s', arguments.output_dir)
                        print ('All alleles have been downloaded from the schema')
                
                elif arguments.file_type == 'profile':
                    profiles_url = db_output['profiles_csv']
                    csv_profile = download_csv_profile (profiles_url, arguments.output_dir, logger)
                    if not csv_profile :
                        logger.error('Profile URL cannot be fetched ')
                        print('Profile CSV cannot be downloaded. Check log file')
                    else:
                        logger.info('Profile CSV file have been successfully downloaded and saved on %s', arguments.output_dir)
                        print ('Profile CSV have been downloaded', '\n')

        print ('Exiting the interactive dialog\n \nReturning to shell prompt \n')  
    

    ## No interactive schema download method chosen
    ### En la forma no interactiva no se está permitiendo que se meta URL pero sí en la forma interactiva. Sin embargo, no tendría sentido que se permitiese
    ### meter url porque a lo mejor, aunque el formato de la URL y la conexión de la misma sean válidos, puede que no sea la url de la api/alguna de las apis permitidas, por lo que va a dar error más adelante...
    ### igual tengo que comparar el enlace de la hipotética api proporcionado por el usuario con los valores del diccionario api_url a ver si coincide, y si no coincide sacar mensaje de error y salir del programa
    else:

        ### ENTEROBASE API NOT SUPPORTED ANYMORE
        #if arguments.api_url == 'enterobase':
         #   logger.debug('Starting recording log activity for %s', arguments.api_url)
          #  if not os.path.isfile(arguments.api_key):
           #     string_text = 'File ' + arguments.api_key + ' does not exists' 
            #    logging_errors(string_text, False , True )
             #   exit (2)
            #try:
             #   result_download = download_locus_enterobase (db_url, arguments.api_key, 
              #              arguments.database, arguments.organism_id,arguments.out)
               # print ('Download was completed')
            #except :
             #   print ('Some errors found when download locus for enterobase',
              #          '\n Check log files\n')
                    
        #else:
        ###
        if arguments.file_type == 'schema':
            locus_list = get_url_files_to_download (db_url, int(arguments.organism_id), int(arguments.schema_database), int(arguments.schema_type), arguments.file_type, logger)
            if not locus_list :
                logger.error('Locus list for schema %s cannot be fetched ', arguments.organism_id)
                print ('Unable to get the locus list for the schema ' , arguments.organism_id)
                exit(0)
            #  import pdb; pdb.set_trace()
            #  print("pdb.set_trace(): ", pdb.set_trace(), '\n')
            fasta_locus = download_fasta_locus ( locus_list, arguments.output_dir, logger)
            if not fasta_locus :
                logger.error('Locus list for schema %s cannot be fetched ', arguments.organism_id)
                print('Some of the alleles files cannot be downloaded. Check log file')
            else:
                logger.info('All alleles have been successfully downloaded and saved on %s', arguments.output_dir)
                print ('All alleles have been downloaded from the schema')

        elif arguments.file_type == 'profile':
            ### DESCARGA DE PROFILE ###
            profiles_url = get_url_files_to_download (db_url, int(arguments.organism_id), int(arguments.schema_database), int(arguments.schema_type), arguments.file_type, logger)
            if not profiles_url:
                logger.error('Profile URL for schema %s cannot be fetched ', arguments.organism_id)
                print ('Unable to get the profile URL for schema %s ', arguments.organism_id)
                exit(0)
            #  import pdb; pdb.set_trace()
            #  print("pdb.set_trace(): ", pdb.set_trace(), '\n')
            
            #if profiles_url == '':
             #   logger.info('There is not ST profile available for schema type with ID %s', schema_type)
              #  print ('There is not ST profile available for schema type with ID %s', schema_type)
               # exit(0)

            csv_profile = download_csv_profile (profiles_url, arguments.output_dir, logger)
            if not csv_profile :
                logger.error('Profile URL for schema %s cannot be fetched ', arguments.organism_id)
                print('Profile CSV cannot be downloaded. Check log file')
            else:
                logger.info('Profile CSV file have been successfully downloaded and saved on %s', arguments.output_dir)
                print ('Profile CSV have been downloaded')
            


