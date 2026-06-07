import os
from datetime import datetime
from unittest import TestCase
from file_manager import FileManager, Folder, DAY_NAMES, Image


class TestFileManager(TestCase):
    def setUp(self):
        self.fm = FileManager("c:\\Temp")
        self.fm.prepare_test_structure()

    def test_root_folder_exists(self):
        self.assertTrue(os.path.isdir(self.fm.root_folder))


    def test_folders_created(self):
        for folder in self.fm.test_folders:
            self.assertTrue(os.path.isdir(os.path.join(self.fm.root_folder, folder)))

    def test_remove_folders(self):
        self.fm.remove_test_folders()
        for folder in self.fm.test_folders:
            self.assertFalse(os.path.exists(os.path.join(self.fm.root_folder, folder)))

    def test_list_directories(self):
        dirs = self.fm.list_directories()
        self.assertListEqual(dirs, self.fm.test_folders)

    def test_list_directories_full_path(self):
        dirs = self.fm.list_directories_full_path()
        expected_dirs = [os.path.join(self.fm.root_folder, folder) for folder in self.fm.test_folders]
        self.assertListEqual(dirs, expected_dirs)

    def test_get_folders(self):
        folders = self.fm.get_folders()
        self.assertEqual(len(folders), len(self.fm.test_folders))
        for folder in folders:
            self.assertIsInstance(folder, Folder)
            self.assertEqual(folder.file_count, len(self.fm.test_images))
            self.assertEqual(folder.full_path, os.path.join(self.fm.root_folder, folder.name))
            self.assertIn(folder.day_name, DAY_NAMES)
            self.assertEqual(folder.date_obj, datetime.strptime(folder.name, '%Y_%m_%d').date())

    def test_list_files_in_folder(self):
        for folder in self.fm.test_folders:
            files = self.fm.list_files_in_folder(folder)
            self.assertEqual(len(files), len(self.fm.test_images))

    def test_list_files_in_folder_full_path(self):
        for folder in self.fm.test_folders:
            files = self.fm.list_files_in_folder_full_path(folder)
            self.assertEqual(len(files), len(self.fm.test_images))
            expected_files = [os.path.join(self.fm.root_folder, folder, image) for image in self.fm.test_images]
            self.assertListEqual(files, expected_files)

    def test_get_images_in_folder(self):
        for folder in self.fm.test_folders:
            images = self.fm.get_images_in_folder(folder)
            self.assertEqual(len(images), len(self.fm.test_images))
            for image in images:
                self.assertIsInstance(image, Image)

    def tearDown(self):
        self.fm.remove_test_folders()

