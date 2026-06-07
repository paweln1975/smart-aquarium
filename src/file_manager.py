import os
import shutil
import time
from datetime import datetime
from dataclasses import dataclass

IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
DAY_NAMES = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']

def is_image(fname):
    return os.path.splitext(fname)[1].lower() in IMAGE_EXT

def is_date_folder(folder: str):
    # check if folder is in format yyyy_dd_mm
    try:
        parts = folder.split('_')
        if len(parts) != 3:
            return False
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        return 1 <= month <= 12 and 1 <= day <= 31 and 2026 <= year <= 2099
    except ValueError:
        return False

def get_time_from_filename(fname: str):
    parts = fname.split('.')[0].split('_')
    if len(parts) != 4:
        return None
    name, hour, minute, _ = parts
    return hour, minute

@dataclass
class Folder:
    name: str
    label: str
    file_count: int
    full_path: str
    day_name: str
    date_obj: datetime.date

@dataclass
class Image:
    name: str
    full_path: str
    time_obj: time
    hour: str
    minute: str

class FileManager:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.test_folders = ['2026_06_04', '2026_06_05', '2026_06_06']
        self.test_images = ['image_12_01_01.jpg', 'image_12_01_02.jpg', 'image_12_01_03.jpg']

    def create_folder(self, folder_name):
        path = os.path.join(self.root_folder, folder_name)
        if not os.path.exists(path):
            os.makedirs(path)

    def prepare_test_structure(self):
        for folder in self.test_folders:
            self.create_folder(folder)
            for image in self.test_images:
                with open(os.path.join(self.root_folder, folder, image), 'w') as f:
                    f.write('This is a test image file.')

    def remove_test_folders(self):
        for folder in self.test_folders:
            if os.path.exists(os.path.join(self.root_folder, folder)):
                shutil.rmtree(os.path.join(self.root_folder, folder))

    def list_directories(self):
        return [d for d in os.listdir(self.root_folder)
                if os.path.isdir(os.path.join(self.root_folder, d))
                and is_date_folder(d)]

    def list_directories_full_path(self):
        dirs = self.list_directories()
        return [os.path.join(self.root_folder, d) for d in dirs]

    def get_folders(self):
        dirs = self.list_directories()
        folders = [
            Folder(name=d,
                   label=d.replace('_', '.'),
                   date_obj=datetime.strptime(d, '%Y_%m_%d').date(),
                   day_name=DAY_NAMES[datetime.strptime(d, '%Y_%m_%d').date().weekday()],
                   file_count=len([f for f in os.listdir(os.path.join(self.root_folder, d)) if is_image(f)]),
                   full_path=os.path.join(self.root_folder, d)) for d in dirs]

        folders.sort(key=lambda x: x.date_obj, reverse=True)
        return folders

    def get_folder(self, folder_name):
        folders = self.get_folders()
        for folder in folders:
            if folder.name == folder_name:
                return folder
        return None

    def list_files_in_folder(self, folder_name):
        path = os.path.join(self.root_folder, folder_name)
        return [f for f in os.listdir(path) if is_image(f)]

    def list_files_in_folder_full_path(self, folder_name):
        path = os.path.join(self.root_folder, folder_name)
        return [os.path.join(self.root_folder, folder_name, f) for f in os.listdir(path) if is_image(f)]

    def get_images_in_folder(self, folder_name):
        path = os.path.join(self.root_folder, folder_name)
        images = [
            Image(
                name=image,
                full_path=os.path.join(path, image),
                time_obj=os.path.getmtime(os.path.join(path, image)),
                hour=get_time_from_filename(image)[0],
                minute=get_time_from_filename(image)[1]
            )
            for image in self.list_files_in_folder(folder_name)
        ]

        images.sort(key=lambda x: x.time_obj, reverse=True)
        return images

