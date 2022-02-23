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


class AutoFileDelete:
    """
    Delete the oldest folder from the path specified by user
    """
    drive = []
    total = ''
    used = ''
    free = ''

    def __init__(self):

        self.need_storage = None

        # Save all of the user's drives in drive variable.
        for i in range(len(psutil.disk_partitions())):
            AutoFileDelete.drive.append(str(psutil.disk_partitions()[i])[18:19])

        # Set the drive as the reference to D
        self.diskLabel = 'D://'
        AutoFileDelete.total, AutoFileDelete.used, AutoFileDelete.free = shutil.disk_usage(self.diskLabel)

        self.path = None

    def start(self):
        try:
            self.need_storage = int(input(f'How much storage space do you want? '
                                          f'(Now you have {self.byte_transform(self.free, "GB")} GB) : '))
        except ValueError:
            print('Insert only number!!!!!!')
            sys.exit()
        self.main()

    def byte_transform(self, bytes, to, bsize=1024):
        """
        Unit conversion of byte received from shutil

        :return: Capacity of the selected unit (int)
        """
        unit = {'KB': 1, 'MB': 2, 'GB': 3, 'TB': 4}
        r = float(bytes)
        for i in range(unit[to]):
            r = r / bsize
        return int(r)

    def delete_oldest_files(self, path, minimum_storage_GB: int):
        """
        The main function of this Program
        Find oldest file and proceed with deletion

        :param path: Path to proceed with a auto-delete
        :param minimum_storage_GB: Minimum storage space desired by the user
        :return: None
        """
        is_old = {}

        while minimum_storage_GB >= self.byte_transform(self.free, 'GB'):

            for f in os.listdir(path):

                i = os.path.join(path, f)
                is_old[f'{i}'] = int(os.path.getctime(i))
                print(i)

            value = list(is_old.values())
            key = {v: k for k, v in is_old.items()}
            oldest = key.get(min(value))

            box = input(f'Are you sure to delete "{oldest}" folder?')
            if box == "":
                # Main syntax for deleting folders
                # shutil.rmtree(oldest)
                print(f'{oldest} delete complete.')
            else:
                sys.exit()

        print('Already you have enough storage.')

    def main(self):
        """
        Delete files by comparing "need_storage" with the current storage space

        :return: None
        """
        # If storage space required is more than current storage space
        if self.need_storage >= self.byte_transform(self.free, 'GB'):
            # Specify the Vista folder path of the d drive as a path variable
            self.path = os.path.join(self.diskLabel, 'vista')
            try:
                self.delete_oldest_files(self.path, self.need_storage)
            except FileNotFoundError:
                print(f'[{self.path}] - Not Found Error')

        else:
            print('Input storage again')


if __name__ == "__main__":

    start = AutoFileDelete()
