#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright 2023 LG Electronics Inc.
# SPDX-License-Identifier: Apache-2.0
import logging

logger = logging.getLogger(__name__)

PKG_NAME = "fosslight_android"
CONST_NULL = ""
CONST_TLSH_NULL = "0"
MODULE_INFO_FILE_NAME = "module-info.json"
MODULE_TYPE_NAME = "MODULE_NAME"
MODULE_TYPE_OUTPUT = "MODULE_OUTPUT"
MODULE_TYPE_INSTALLED = "installed"
NEED_CHECK_WORD = "(NEED_CHECK)"
skip_license = ['Other Proprietary License', 'LGE License', 'LGE Proprietary License']
NOTICE_FILE_NAME = "NOTICE"


class AndroidBinary:
    bin_name = ""
    bin_name_with_installed_path = ""
    binary_name_without_path = ""
    source_code_path = ""
    module_name = ""
    notice = ""
    mk_file_path = ""
    tlsh = ""
    checksum = ""
    oss_name = ""
    oss_version = ""
    license = ""
    comment = ""
    exclude = ""
    url = ""
    additional_oss_items = []
    download_location = ""
    homepage = ""
    is_new_bin = True

    def __init__(self, value):
        self.bin_name = value
        self.binary_name_without_path = ""
        self.bin_name_with_installed_path = ""
        self.source_code_path = CONST_NULL
        self.module_name = ""
        self.notice = CONST_NULL
        self.mk_file_path = CONST_NULL
        self.tlsh = CONST_TLSH_NULL
        self.checksum = CONST_TLSH_NULL
        self.license = CONST_NULL
        self.oss_name = CONST_NULL
        self.oss_version = ""
        self.comment = ""
        self.exclude = ""
        self.url = ""
        self.download_location = ""
        self.homepage = ""
        self.additional_oss_items = []
        self.is_new_bin = True

    def __del__(self):
        pass

    def set_bin_name(self, value):
        self.bin_name = value

    def set_bin_name_with_installed_path(self, value):
        self.bin_name_with_installed_path = value

    def set_comment(self, value):
        self.comment = value

    def set_source_code_path(self, value):
        self.source_code_path = value

    def set_module_name(self, value):
        self.module_name = value

    def set_exclude(self, value):
        if value:
            self.exclude = "Exclude"
        else:
            self.exclude = ""

    def set_notice(self, value):
        self.notice = value

    def set_mk_file_path(self, value):
        self.mk_file_path = value

    def set_tlsh(self, value):
        self.tlsh = value

    def set_checksum(self, value):
        self.checksum = value

    def set_license(self, value):
        self.license = value

    def set_additional_oss_items(self, value):
        self.additional_oss_items.append(value)
        self.additional_oss_items = list(set(self.additional_oss_items))

    def set_oss_name(self, value):
        self.oss_name = value

    def set_oss_version(self, value):
        self.oss_version = value

    def set_url(self, value):
        self.url = value

    def set_homepage(self, value):
        self.homepage = value

    def set_download_location(self, value):
        self.download_location = value

    def get_print_items(self):
        print_items_txt = []
        print_items_excel = []
        oss_name = self.oss_name
        source_path = self.source_code_path
        item_license = self.license

        empty_columns, license_to_notice = check_empty_column(item_license, oss_name, source_path)
        comment = get_comment(self.comment, license_to_notice, self.notice, empty_columns)
        if comment != "":
            need_check = "O"
        else:
            need_check = ""
        print_items_txt.append(f"{self.bin_name}\t{source_path}\t{self.notice}\t"
                               f"{oss_name}\t{self.oss_version}\t{self.license}\t{need_check}\t{comment}\t{self.tlsh}\t{self.checksum}")
        repo_link = self.download_location if self.is_new_bin else ""
        print_items_excel.append([self.bin_name, source_path, self.notice, oss_name,
                                  self.oss_version, self.license, repo_link, repo_link, '', '', '', comment, need_check])

        if self.additional_oss_items is not None:
            for item in self.additional_oss_items:
                print_items_txt.append(f"{self.bin_name}\t{source_path}\t{self.notice}\t{item}"
                                       f"\t{need_check}\t{comment}\t{self.tlsh}\t{self.checksum}")
                excel_item = [self.bin_name, source_path, self.notice]
                excel_item.extend(item.split('\t'))
                excel_item.extend(['', '', '', '', '', comment, need_check])
                print_items_excel.append(excel_item)
        return print_items_txt, print_items_excel


def check_empty_column(license, oss_name, directory):
    empty_columns = []
    license_to_notice = True

    if license != CONST_NULL:
        for license_item in license.split(','):
            if license_item in skip_license:
                license_to_notice = False
                break
    else:
        empty_columns.append('License')
    if oss_name == CONST_NULL and license_to_notice:
        empty_columns.append('OSS Name')
    if directory == CONST_NULL:
        empty_columns.append('Source Code Path')
    return empty_columns, license_to_notice


def get_comment(default_comment, license_to_notice, notice_value, empty_columns):
    comment = ""

    if empty_columns is not None and len(empty_columns) > 0:
        comment = "Fill in " + ",".join(empty_columns) + "."

    if notice_value == 'nok' and license_to_notice:
        if comment != "":
            comment += "/"
        comment += "Add NOTICE to path."

    elif notice_value == 'nok(NA)' and license_to_notice:
        if comment != "":
            comment += "/"
        comment += "Add NOTICE to proper path."

    comment = default_comment + comment  # Paste Auto ID comment in front.

    return comment


def set_value_switch(bin, key, value):
    switcher = {
        'BinaryName': bin.set_bin_name,
        'SourceCodePath': bin.set_source_code_path,
        'ModuleName': bin.set_module_name,
        'NOTICE': bin.set_notice,
        'License': bin.set_license,
        'mkFilePath': bin.mk_file_path,
        'tlsh': bin.set_tlsh,
        'checksum': bin.set_checksum,
        'OSSName': bin.set_oss_name,
        'OSSVersion': bin.set_oss_version,
        'Comment': bin.set_comment
    }
    func = switcher.get(key, lambda key: invalid(key))
    func(value)


def invalid(cmd):
    print('[{}] is invalid'.format(cmd))
