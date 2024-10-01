#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######
import sys

from PyQt6 import QtWidgets, QtGui
from common.utility import resolve_path

from view.init import Init as InitView
from view.wizard import Wizard as WizardView
from view.scrapers.web.web import Web as WebView
from view.scrapers.mail.mail import Mail as MailView
from view.scrapers.instagram.instagram import Instagram as InstagramView
from view.scrapers.video.video import Video as VideoView
from view.scrapers.entire_website.entire_website import (
    EntireWebsite as EntireWebsiteView,
)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resolve_path("icon.ico")))

    acquisition_window = None
    def start_task(task, case_info):
        global acquisition_window
        options = {}
        if task == "web":
            acquisition_window = WebView()
        elif task == "mail":
            acquisition_window = MailView()
        elif task == "instagram":
            acquisition_window = InstagramView()
        elif task == "video":
            acquisition_window = VideoView()
        elif task == "entire_website":
            acquisition_window = EntireWebsiteView()

        acquisition_window.init(case_info, wizard, options)
        acquisition_window.show()

    init = InitView()
    wizard = WizardView()

    init.finished.connect(wizard.show)
    # Wizard sends a signal when start button is clicked and case is stored on the DB
    wizard.finished.connect(lambda task, case_info: start_task(task, case_info))

    init.init_check()

    sys.exit(app.exec())
