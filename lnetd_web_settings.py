from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LnetdSettings(QtWidgets.QDialog):
    settings_change = QtCore.pyqtSignal(str,str,str)

    def change(self):
        metric = None
        capacity = None
        try:
            url = str(self.url_txt.text())
            password = str(self.password_txt.text())
            username = str(self.username_txt.text())
        except ValueError:
            QtWidgets.QMessageBox.critical(
                    self.changeLnetdSettings, "Error!", "The all values must be strings !"
                )
        if url is not None or password is not None or username is not None:

            self.settings_change.emit(url,password,username)
            self.changeLnetdSettings.accept()

    def setupUi(self, changeLnetdSettings, url,password,username ):
        self.username = username
        self.url = url
        self.password = password
        self.changeLnetdSettings = changeLnetdSettings
        self.changeLnetdSettings.setObjectName("changeLnetdSettings")
        self.changeLnetdSettings.resize(291, 196)

        self.gridLayout_2 = QtWidgets.QGridLayout(self.changeLnetdSettings)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.url_txt = QtWidgets.QLineEdit(self.changeLnetdSettings)
        self.url_txt.setObjectName("url_txt")
        self.gridLayout.addWidget(self.url_txt, 3, 1, 1, 1)

        self.username_lbl = QtWidgets.QLabel(self.changeLnetdSettings)
        self.username_lbl.setObjectName("username_lbl")
        self.gridLayout.addWidget(self.username_lbl, 1, 0, 1, 1)

        self.username_txt = QtWidgets.QLineEdit(self.changeLnetdSettings)
        self.username_txt.setObjectName("username_txt")
        self.gridLayout.addWidget(self.username_txt, 1, 1, 1, 1)

        self.password_lbl = QtWidgets.QLabel(self.changeLnetdSettings)
        self.password_lbl.setObjectName("password_lbl")
        self.gridLayout.addWidget(self.password_lbl, 2, 0, 1, 1)

        self.url_lbl = QtWidgets.QLabel(self.changeLnetdSettings)
        self.url_lbl.setObjectName("url_lbl")
        self.gridLayout.addWidget(self.url_lbl, 3, 0, 1, 1)

        self.password_txt = QtWidgets.QLineEdit(self.changeLnetdSettings)
        self.password_txt.setObjectName("password_txt")
        self.password_txt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.password_txt, 2, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.save_btn = QtWidgets.QPushButton(self.changeLnetdSettings)
        self.save_btn.setObjectName("save_btn")

        self.gridLayout_2.addWidget(self.save_btn, 1, 0, 1, 1)


        self.retranslateUi(changeLnetdSettings)
        self.save_btn.clicked.connect(self.change)
        QtCore.QMetaObject.connectSlotsByName(self.changeLnetdSettings)

    def retranslateUi(self, changeLnetdSettings):
        _translate = QtCore.QCoreApplication.translate
        changeLnetdSettings.setWindowTitle(_translate("changeLnetdSettings", "LnetD WEB Settings"))
        self.save_btn.setText(_translate("changeLnetdSettings", "Save"))

        self.username_lbl.setText(_translate("changeLnetdSettings", "Username:"))
        self.username_txt.setText(str(self.username))
        self.password_lbl.setText(_translate("changeLnetdSettings", "Password:"))
        self.password_txt.setText(str(self.password))
        self.url_lbl.setText(_translate("changeLnetdSettings", "URL: "))
        self.url_txt.setText(str(self.url))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    changeLnetdSettings = QtWidgets.QDialog()
    ui = Ui_changeLnetdSettings()
    ui.setupUi(changeLnetdSettings)
    changeLnetdSettings.show()
    sys.exit(app.exec_())

