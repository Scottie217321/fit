#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######

import sys
import pkgutil
from inspect import isclass
from importlib import import_module

from PyQt6 import QtCore, QtWidgets, uic

import view.configurations
from view.configurations import classname2objectname


from common.constants.view.configurations import tabs
from common.utility import resolve_path, get_version

from ui.configuration import resources


class Configuration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Configuration, self).__init__(parent)

        self.__tabs = list()
        self.__init_ui()

    def __init_ui(self):
        uic.loadUi(resolve_path("ui/configuration/configuration.ui"), self)

        # HIDE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # CUSTOM TOP BAR
        self.left_box.mouseMoveEvent = self.move_window

        # MINIMIZE BUTTON
        self.minimize_button.clicked.connect(self.showMinimized)

        # CLOSE BUTTON
        self.close_button.clicked.connect(self.close)

        # SET VERSION
        self.version.setText(get_version())

        # CANCEL BUTTON
        self.cancel_button.clicked.connect(self.reject)
        # SAVE BUTTON
        self.save_button.clicked.connect(self.accept)

        self.__load_tabs()
        for tab in self.__tabs:
            self.menu_tabs.addTopLevelItem(QtWidgets.QTreeWidgetItem([tab.name]))

        self.tabs.setCurrentIndex(0)
        self.menu_tabs.topLevelItem(0).setSelected(True)

        self.menu_tabs.itemClicked.connect(self.__on_tab_clicked)

    def __on_tab_clicked(self, item, column):
        self.tabs.setCurrentIndex(self.menu_tabs.indexOfTopLevelItem(item))

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def move_window(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def __load_tabs(self):
        package = view.configurations

        for importer, modname, ispkg in pkgutil.walk_packages(
            path=package.__path__, prefix=package.__name__ + ".", onerror=lambda x: None
        ):
            # import module if not loaded
            if modname not in sys.modules and not ispkg:
                import_module(modname)

            if modname in sys.modules and not ispkg:
                # find class name in a module
                class_name = [
                    x
                    for x in dir(sys.modules[modname])
                    if isclass(getattr(sys.modules[modname], x))
                    and getattr(sys.modules[modname], "__is_tab__")
                    and x.lower() == modname.rsplit(".", 1)[1]
                ]

                if class_name:
                    class_name = class_name[0]
                    ui_tab = self.__dict__.get(
                        classname2objectname.__dict__.get(class_name.upper())
                    )

                    if ui_tab:
                        tab_class = getattr(sys.modules[modname], class_name)
                        tab = tab_class(
                            ui_tab, tabs.__dict__.get(ui_tab.objectName().upper())
                        )
                        self.__tabs.append(tab)

    def accept(self):

        for tab in self.__tabs:
            tab.accept()

        return super().accept()

    def reject(self):
        for tab in self.__tabs:
            tab.reject()

        return super().reject()
