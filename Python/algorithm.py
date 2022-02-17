#!/usr/bin/env python3
#
# Copyright 2021-2022 9th grade 5th class.
#
# Authors:
#     5jx2oh@gmail.com


import os
import sys
import shutil
import psutil


class FileAutoDelete:
    """
    Delete the oldest folder from the path specified by user
    """

    def __init__(self):
        """
        initial function
        """

        drive = []
        # Save all of the user's drives in drive variable.
        for i in range(len(psutil.disk_partitions())):
            drive.append(str(psutil.disk_partitions()[i])[18:19])

        # Set the drive as the reference to D
        self.diskLabel = 'D://'
        self.total, self.used, self.free = shutil.disk_usage(self.diskLabel)

        # print(f'{self.diskLabel} {self.byte_transform(self.free, "GB")} GB')
        print(f'Total storage - {self.total}')
        print(f'Used storage - {self.used}')
        print(f'Free storage - {self.free}')

        self.path = None

        try:
            self.need_storage = int(input(f'How much storage space do you want? '
                                          f'(Now you have {self.byte_transform(self.free, "GB")} GB) : '))
        except ValueError:
            print('Insert only number!!!!!!!!!!!!!')
            sys.exit()
        self.btn_click()

    def byte_transform(self, bytes, to, bsize=1024):
        """
        Unit conversion of byte received from shutil

        :return: Capacity of the selected unit (int)
        """
        unit = {'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4}
        r = float(bytes)
        for i in range(unit[to]):
            r = r / bsize
        return float(r)

    def delete_oldest_files(self, path, minimum_storage_GB: int):
        """
        The main function of this Program
        Find oldest file and proceed with deletion

        :param path: Path to proceed with a auto-delete
        :param minimum_storage_GB: Minimum storage space desired by the user
        """
        is_old = {}

        if minimum_storage_GB >= self.byte_transform(self.free, 'GB'):

            for f in os.listdir(path):

                i = os.path.join(path, f)
                is_old[f'{i}'] = int(os.path.getctime(i))

            value = list(is_old.values())
            key = {v: k for k, v in is_old.items()}
            old_folder = key.get(min(value))

            box = input(f'Are you sure to delete "{old_folder}" folder?')
            if box == "":
                print('yes')
                # Main syntax for deleting folders
                # shutil.rmtree(old_folder)
            else:
                print('no')

        else:
            print('Already you have enough storage.')

    def btn_click(self):
        # If storage space required is more than current storage space,
        if self.need_storage >= self.byte_transform(self.free, 'GB'):
            # diskLabel, 즉 D 드라이브의 vista 폴더 경로를 path 변수에 지정
            self.path = os.path.join(self.diskLabel, 'vista')
            try:
                self.delete_oldest_files(self.path, self.need_storage)
            except FileNotFoundError:
                print(f'[{self.path}] - Not Found Error')

        else:
            print('Input storage again')


if __name__ == "__main__":

    start = FileAutoDelete()