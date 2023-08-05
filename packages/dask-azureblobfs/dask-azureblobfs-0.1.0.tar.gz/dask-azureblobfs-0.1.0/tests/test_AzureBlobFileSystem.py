#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `azureblobfs` package."""

import os
import unittest
import warnings

from azureblobfs.fs import AzureBlobFileSystem
from azureblobfs.utils import generate_guid


class AzureBlobFileSystemTest(unittest.TestCase):
    account_name = "e29"
    container = "azure-blob-filesystem"

    def setUp(self):
        self.account_key = os.environ.get("AZURE_BLOB_ACCOUNT_KEY")
        self.fs = AzureBlobFileSystem(self.account_name, self.account_key)
        try:
            warnings.simplefilter("ignore", ResourceWarning)
        except:
            pass

    def test_ls(self):
        folder_list = self.fs.ls(self.container)
        self.assertIn('artifacts/samples/artifacts (3).json', folder_list)
        self.assertIn('weathers/vs_Enterprise.exe', folder_list)
        self.assertIn('03_section_zhen.pdf', folder_list)
        self.assertIn('image.png', folder_list)

    def test_ls_pattern(self):
        folder_list = self.fs.ls(self.container, "artifacts*")
        self.assertIn("artifacts/samples/artifacts (2).json", folder_list)
        self.assertIn("artifacts/samples/artifacts (3).json", folder_list)

    def test_touch_rm(self):
        file_name = "test_touch_rm/{file}.txt".format(file=generate_guid())
        self.assertEqual(self.fs.touch(self.container, file_name), file_name)
        self.fs.rm(self.container, file_name)

    def test_du(self):
        du_results = self.fs.du(self.container)
        self.assertIn(('weathers/rdu-weather-history.csv', 480078), du_results.items())
        self.assertIn(('weathers/Local_Weather_Data.csv', 7580289), du_results.items())

    def test_head(self):
        head_content = self.fs.head(self.container, "weathers/Local_Weather_Data.csv", 20)
        self.assertEqual(len(head_content), 20)
        self.assertEqual(head_content, b'RowID,DateTime,TempO')

    def test_tail(self):
        tail_content = self.fs.tail(self.container, "weathers/Local_Weather_Data.csv", 50)
        self.assertEqual(len(tail_content), 50)
        self.assertEqual(tail_content, b'.201,0,68.7,38,42.1,66.1,7.55,0.0748,351,1,100,15\n')

    def test_touch_mv_cp_rm(self):
        folder_name = "test_touch_mv_cp_rm"
        self.fs.mkdir(self.container, folder_name)
        src_file_name = "{folder_name}/{file}".format(folder_name=folder_name, file=generate_guid())
        dst_file_name = "{folder_name}/{file}".format(folder_name=folder_name, file=generate_guid())
        try:
            self.assertEqual(self.fs.touch(self.container, src_file_name), src_file_name)
            self.assertIn(src_file_name, self.fs.ls(self.container))
            self.assertTrue(self.fs.mv(self.container, src_file_name, dst_file_name))
            self.assertNotIn(src_file_name, self.fs.ls(self.container))
            self.assertIn(dst_file_name, self.fs.ls(self.container))
            self.fs.cp(self.container, dst_file_name, src_file_name)
            self.assertIn(src_file_name, self.fs.ls(self.container))
            self.assertIn(dst_file_name, self.fs.ls(self.container))
        finally:
            self.fs.rm(self.container, src_file_name)
            self.fs.rm(self.container, dst_file_name)
