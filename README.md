# smart-aquarium
Live view to aquarium

# File structure manager

## Browse operations

### Setup

>>> from file_manager import FileManager
>>> fm = FileManager('c:\\Temp')
>>> fm.prepare_test_structure()

### Create a manager

>>> fm = FileManager('c:\\Temp')
>>> fm.root_folder
'c:\\Temp'

### List directories in a folder

>>> fm.list_directories()
['2026_06_04', '2026_06_05', '2026_06_06']

### List directories with full paths in a folder

>>> fm.list_directories_full_path()
['c:\\Temp\\2026_06_04', 'c:\\Temp\\2026_06_05', 'c:\\Temp\\2026_06_06']

### Get folders with details

>>> fm.get_folders()
[Folder(name='2026_06_06', label='2026.06.06', file_count=3, full_path='c:\\Temp\\2026_06_06', day_name='sobota', date_obj=datetime.date(2026, 6, 6)), Folder(name='2026_06_05', label='2026.06.05', file_count=3, full_path='c:\\Temp\\2026_06_05', day_name='piątek', date_obj=datetime.date(2026, 6, 5)), Folder(name='2026_06_04', label='2026.06.04', file_count=3, full_path='c:\\Temp\\2026_06_04', day_name='czwartek', date_obj=datetime.date(2026, 6, 4))]

### List files in a folder
>>> fm.list_files_in_folder('2026_06_04')
['image_12_01_01.jpg', 'image_12_01_02.jpg', 'image_12_01_03.jpg']

### List files in a folder with full paths

>>> fm.list_files_in_folder_full_path('2026_06_04')
['c:\\Temp\\2026_06_04\\image_12_01_01.jpg', 'c:\\Temp\\2026_06_04\\image_12_01_02.jpg', 'c:\\Temp\\2026_06_04\\image_12_01_03.jpg']

### Get image files with details
>>> images = fm.get_images_in_folder('2026_06_04')
>>> image = images[0]
>>> image.name
'image_12_01_03.jpg'
>>> image.full_path
'c:\\Temp\\2026_06_04\\image_12_01_03.jpg'
>>> image.hour
'12'
>>> image.minute
'01'

