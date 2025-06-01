import time
import os
import re
from watchdog.observers import Observer
from colorama import Fore, Style
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import json

class WatcherHandler(FileSystemEventHandler):
    def __init__(self, folder_to_watch:str, callback) -> None:
        self.folder_to_watch = folder_to_watch
        self.callback = callback


    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            self.handle_created_directory(event.src_path)
        else:
            self.handle_created_file(event.src_path)


    def handle_created_directory(self, directory_path: str) -> None:
        parent_dir = os.path.dirname(directory_path)
        subfolder_name = os.path.basename(directory_path)
        print(f'''Created: {Fore.BLUE}{Style.BRIGHT}{subfolder_name}{Style.RESET_ALL}
        └──> in {Fore.BLUE}{Style.BRIGHT}{parent_dir}{Style.RESET_ALL}''')
        if parent_dir != self.folder_to_watch:
            self.callback(directory_path) 
        if parent_dir == self.folder_to_watch:
            json_file_path = os.path.join(directory_path,f'{subfolder_name}.json')
            with open(json_file_path,'w') as json_file:
                json.dump({}, json_file)
        
                


    def handle_created_file(self, file_path)-> None:
        file_name = os.path.basename(file_path)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')) or file_name.lower().endswith(('.json')):
            subdir = os.path.dirname(file_path)  
            if subdir.rstrip(os.sep).count(os.sep) != 1:
                print(f'''Added: {Fore.BLUE}{Style.BRIGHT}{file_name}{Style.RESET_ALL}
            └──> to {Fore.BLUE}{Style.BRIGHT}{subdir}{Style.RESET_ALL}''')
                self.callback(file_path)
            elif subdir.rstrip(os.sep).count(os.sep) == 1 and file_name.lower().endswith(('.json')):
                print(f'''Added: {Fore.BLUE}    {Style.BRIGHT}{file_name}{Style.RESET_ALL}
            └──> to {Fore.BLUE}{Style.BRIGHT}{subdir}{Style.RESET_ALL}''')
            else:
                print(f"{Fore.RED}{Style.BRIGHT}Warning{Style.RESET_ALL}: '{subdir}' only allow created folder or json file. Do not create non-json files!")
                os.remove(file_path)
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Warning{Style.RESET_ALL}: '{file_path}' is not an image file. Do not create non-image files")
            os.remove(file_path)


    def on_moved(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            self.handle_changed_directory(event.src_path,event.dest_path)
        else:
            self.handle_changed_file(event.src_path,event.dest_path)


    def handle_changed_directory(self,path,changed_path):
        if os.path.basename(path) != os.path.basename(changed_path):
                print(f'''Changed: {Fore.GREEN}{Style.BRIGHT}{path}{Style.RESET_ALL}
        └──> into {Fore.GREEN}{Style.BRIGHT}{changed_path}{Style.RESET_ALL}''')
                parent_folder = os.path.dirname(path)
                if parent_folder != self.folder_to_watch:
                    self.callback(path) 


    def handle_changed_file(self,path,changed_path):
        if path.endswith('.json'):
            new_json_name = changed_path.replace("\\","/").split(self.folder_to_watch)[-1].split("/")[1] + '.json'
            new_json_dir = os.path.join(os.path.dirname(changed_path),new_json_name)
            if changed_path != new_json_dir:
                os.rename(changed_path,new_json_dir)
                print(f'''\t├── {Fore.GREEN}{Style.BRIGHT}{path}{Style.RESET_ALL}
        └──> into {Fore.GREEN}{Style.BRIGHT}{new_json_dir}{Style.RESET_ALL}''')
        else:
            if os.path.basename(path) != os.path.basename(changed_path):
                print(f'''Changed: {Fore.GREEN}{Style.BRIGHT}{path}{Style.RESET_ALL}
        └──> into {Fore.GREEN}{Style.BRIGHT}{changed_path}{Style.RESET_ALL}''')
                self.callback(changed_path)         


    def on_deleted(self, event: FileSystemEvent) -> None:
        parent_folder = os.path.dirname(event.src_path)
        print(f"Deleted: {Fore.RED}{Style.BRIGHT}{event.src_path}{Style.RESET_ALL}")
        if parent_folder != self.folder_to_watch:
            self.callback(event.src_path)
 

def watch_folder(folder_path, callback=None) -> None:
    if callback is None:
        callback = update_json
    event_handler = WatcherHandler(folder_path, callback)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def check_json(path_given)->str:
    base = FOLDER_TO_WATCH.replace("./",".\/")
    normalized_path = path_given.replace("\\","/")
    reg_pattern = rf"(^{base}\/([^\/]+))"
    match = re.match(reg_pattern, normalized_path)
    json_name = match.group(2) + '.json'
    path_contains_json = os.path.join(match.group(1),json_name)
    if os.path.exists(path_contains_json):
        return path_contains_json
    else:
        return f"{json_name} not found!"


def update_json(path):
    jsonfile = check_json(path)
    if "not found" in jsonfile:
        print(f" |\n"
            f" └──> {Fore.RED}{Style.BRIGHT}{jsonfile}{Style.RESET_ALL}" + 
              f" Please create the {Fore.BLUE}{Style.BRIGHT}{jsonfile.removesuffix(' not found!')}{Style.RESET_ALL}!")
    else:
        sub_dir = os.path.dirname(jsonfile)
        json_data = {}

        for item in os.listdir(sub_dir):
            if os.path.isdir(os.path.join(sub_dir, item)):
                json_data[item] = {}
                json_data[item]["template"] = None
                json_data[item]["handwriting_template"] = None
                for file in os.listdir(os.path.join(sub_dir, item)):
                    img_template_path = f"{FOLDER_TO_WATCH}/{os.path.basename(sub_dir)}/{item}/{file}"
                    if file.endswith("_template.png"):
                        json_data[item]["template"] = img_template_path
                    elif file.endswith("_hwtemplate.png"):
                        json_data[item]["handwriting_template"] = img_template_path
 
        with open(jsonfile, 'w') as f:
            json.dump(json_data, f, indent=2)
        print("Updated: "+jsonfile)

    

if __name__ == "__main__":
    FOLDER_TO_WATCH = "./templates"
    watch_folder(FOLDER_TO_WATCH)