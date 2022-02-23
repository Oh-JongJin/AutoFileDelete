#!/usr/bin/env python3
#
# Copyright 2021-2022 9th grade 5th class.
#
# Authors:
#     5jx2oh@gmail.com

from PyQt5.QtCore import QSettings


class AFDSettings:
    settings = QSettings('9th grade 5th class', 'AFD')
    defaults = {
        'drive': 'C',
        'storage': 0
    }

    @classmethod
    def set(cls, key, value):
        cls.settings.setValue(key, value)

    @classmethod
    def get(cls, key):
        return cls.settings.value(
            key,
            cls.defaults[key],
            type(cls.defaults[key])
        )
