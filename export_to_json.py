import json
import os.path

def build_json_file(reddit_data:json, file_export_name:str) -> None:
    '''
    Takes a json object and exports the results as a json file. 

    Returns: 
        None
    '''
    file_export_name = f"{file_export_name}.json"

    if not(os.path.exists(file_export_name)):

        with open(file_export_name,"w",encoding='utf-8') as f:
            json.dump(reddit_data, f, ensure_ascii=False, indent=4)

    else:

        with open(file_export_name,"r",encoding='utf-8') as f:
            data = json.load(f)
        
        data.append(reddit_data)
        
        with open(file_export_name,"w",encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def build_error_text_file(data:str, file_export_name:str) -> None:
    '''
    Takes a string and exports the results as a text file. 

    Returns: 
        None
    '''
    with open(f"{file_export_name}_error.txt", 'a', encoding='utf-8') as error_file:
        error_file.write(f"{data}\n")