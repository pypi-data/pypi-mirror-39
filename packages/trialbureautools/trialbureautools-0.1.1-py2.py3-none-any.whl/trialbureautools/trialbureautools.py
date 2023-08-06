# -*- coding: utf-8 -*-

"""Main module."""

from icaclswrap.foldertool import WinFolderPermissionTool
from icaclswrap.rights import FULL_ACCESS, READ_DELETE

PERMISSIONS = {'full_access': FULL_ACCESS,
               'read_delete': READ_DELETE}


def set_folder_permissions(folder, permissions):
    tool = WinFolderPermissionTool()
    print(f"settings folder'{folder}' permissions to {permissions}")
