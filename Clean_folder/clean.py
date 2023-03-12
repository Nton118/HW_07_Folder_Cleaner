from pathlib import Path
import pkgutil
import shutil
import sys
from .translit import normalize



CATEGORIES = {}
found_files = {}

known_types = []
unknown_types = []


def read_config():
    cfg = pkgutil.get_data(__package__, 'config.txt') 
    cfg_str = cfg.decode('utf-8')
            
    lines = cfg_str.split('\n')
    for line in lines:
        line = line.replace(' ','').replace('\n','')
        key = line.split(':')[0]
        value = line.split(':')[1].split(',')
        CATEGORIES.update({key:value})   
        found_files.update({key:[]})


def scan_folder(path:Path):
    
    contents = [x for x in path.iterdir()]
    for item in contents:
        is_unknown = True    
        if item.is_file():
            ext = item.suffix[1:].upper()
                    
            for name, types in CATEGORIES.items():
                if ext in types: 
                    found_files[name].append(item)
                    known_types.append(ext)
                    is_unknown = False
                    break
                    
            if is_unknown:
                unknown_types.append(ext)
           
        else:
            if item.name not in CATEGORIES.keys():
                scan_folder(item)
            else: 
                continue


def move_files(files_list:list, target_path:Path, new_folder_name:str) -> list:
    output_list = []
    new_dir = target_path / new_folder_name
    try:
        new_dir.mkdir()
    except FileExistsError:
        pass
    for file in files_list:
        new_name = normalize(file.name)
        output_list.append(new_name)
        try:
            file.rename(f'{new_dir}\{new_name}')
        except FileExistsError:
            file.unlink() #delete doubles
    return output_list
 
        
def unpack_files(target_path:Path):
    
    arc_dir = target_path / 'archives'
    files = [x for x in arc_dir.iterdir()]
    
    for file in files:
        new_name = normalize(file.name).split('.')[0]
        new_dir = arc_dir / new_name
        new_dir.mkdir()
        shutil.unpack_archive(file, new_dir)
        file.unlink() #delete unpacked archive  


def del_empty_folders(path:Path):
    folders = [x for x in path.iterdir() if x.is_dir()]
    for item in folders:
        if item.name not in CATEGORIES.keys():
            if len(list(Path(item).iterdir())) == 0:
                item.rmdir()
            else:
                del_empty_folders(item)
        else:
            continue        

            
def normalize_all(path:Path):
    items = [x for x in path.iterdir()]
    for item in items:
        if item.is_file():
            new_name = item.parent / normalize(item.name)
            item.rename(new_name)
        else:
            if item.name not in CATEGORIES.keys():
                new_name = item.parent / normalize(item.name)
                item.rename(new_name)
                normalize_all(item)
            else: 
                continue    

def report_category(category:str, files_lst: list):
    print(f'Found files in category "{category.capitalize()}": ', len(files_lst))
    for file in files_lst:   
        print(file)  


def main():
    
    read_config()
    

    try:
        work_path = sys.argv[1]
        
    except IndexError:
        print('Please specify target folder in script parameters')
        exit()
        
    path = Path(work_path)
    
    if not path.exists():
        print('Path does not exist')
        exit()
    
    scan_folder(path)
    
    found_known = set(known_types)
    found_unknown = set(unknown_types)
    
    # create folders only for found file types
    for category in found_files.keys(): 
        if len(found_files.get(category)) > 0:
            report_category(category, move_files(found_files.get(category), path, str(category)))
            
    # unpack archives if found any
    if len(found_files.get('archives')) > 0:    
       unpack_files(path)    
    
    del_empty_folders(path)
    
    normalize_all(path)
    
    print('Found known file types:', ", ".join(f for f in found_known))
    print('Found unknown file types:', ", ".join(f for f in found_unknown))  
    
    
if __name__ == '__main__':
    main()


