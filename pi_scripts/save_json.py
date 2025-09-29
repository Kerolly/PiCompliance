import json

def save_to_json(data,filename):
    try:
        with open (filename,'w') as f:
            print(f'[SUCCES] Date salvate din: {filename}')
            json.dump(data,f,indent=4)
    except Exception as e:
        print(f"Error: {e}")
        return None        
        
def load_from_json(filename):       
    try: 
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'Load Succesful: {filename}')
        return data
    except FileNotFoundError:
        print(f"The file called {filename} doesn't exist")
        return None
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None
    
    
def get_macs_from_json():
    datas = load_from_json('nmap_ips_macs_scan.json') 
    macs = []
    for data in datas:
        temp = data.get('mac')
        macs.append(temp)
    print(macs)
    return macs