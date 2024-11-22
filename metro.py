import sys

import sqlite3
from random import choice
from design_new import Ui_Dialog
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QTableView, QMessageBox


class MyWidget(QMainWindow, Ui_Dialog, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.lst = []
        self.coords_x = 0
        self.coords_y = 0
        self.mode = ''
        self.right_lst = []
        self.chosen_line_lst = []
        self.station_name = ''
        self.temporary_rusult_label = QLabel(self)

        self.pixmnamed = QtGui.QPixmap('named.jpg')
        self.inamed = QtWidgets.QLabel(self)

        self.pixmapnamed = QtGui.QPixmap('nonamed.jpg')
        self.imagenamed = QtWidgets.QLabel(self)
        self.counter = 0
        self.stat_txt = ''
        self.con = sqlite3.connect("metro_db.sqlite")
        self.cur = self.con.cursor()
        self.view = QTableView(self)
        self.view.hide()
        self.flag = True

    def initUI(self):
        guide = QMessageBox(self)
        guide.setWindowTitle("Гайд")
        guide.setText(
            """ \t\t\tДобро пожаловать! \n
            Эта программа предназначена для запоминания расположения станций метро Санкт-Петербурга.\n
            Для начала выберите режим работы: общий (тренировка всех линий), красной ветки, синей ветки, зелёной ветки,
            оранжевой ветки, фиолетовой ветки. \n
            Под картой метро будет название станции, на которую Вам нужно нажать.Если Вы нажали правильно, то в правом
            нижнем углу к количеству правильных ответов прибавится ещё один. В ином случае количество правильных ответов
            останется неизменным. \n
            После появления надписи 'Тест пройден', Вы можете нажать на кнопку с текстом 'Запомнить попытку', чтобы
            позже посмотреть свои результаты попыток.\n
            Для просмотра статистики нажмите на кнопку 'Статистика'. \n
            Если Вам хочется узнать расположение некоторых станций, нажмите на кнопку 'Карта с названиями'. \n
            Для продолжения прохождения тестов достаточно нажать на кнопку одного из режимов.\n
            Удачной игры!""")
        guide.setIcon(QMessageBox.Icon.Information)

        guide.setStandardButtons(QMessageBox.StandardButton.Ok)
        guide.exec()
        guide.hide()

        self.pixmapnamed = QtGui.QPixmap('nonamed.jpg')
        self.imagenamed = QtWidgets.QLabel(self)
        self.imagenamed.move(231, 10)
        self.imagenamed.resize(461, 640)
        self.imagenamed.setPixmap(self.pixmapnamed)

        self.station = QLabel(self)
        self.station.setText('Выберите режим')
        self.station.setGeometry(410, 670, 190, 20)

        self.pushButton_2.clicked.connect(self.station_choice2)
        self.pushButton_2.clicked.connect(self.nonamed_map)

        self.pushButton_3.clicked.connect(self.station_choice3)
        self.pushButton_3.clicked.connect(self.nonamed_map)

        self.pushButton_4.clicked.connect(self.station_choice4)
        self.pushButton_4.clicked.connect(self.nonamed_map)

        self.pushButton_5.clicked.connect(self.station_choice5)
        self.pushButton_5.clicked.connect(self.nonamed_map)

        self.pushButton_6.clicked.connect(self.station_choice6)
        self.pushButton_6.clicked.connect(self.nonamed_map)

        self.pushButton_7.clicked.connect(self.station_choice7)
        self.pushButton_7.clicked.connect(self.nonamed_map)

        self.pushButton_8.clicked.connect(self.named_map)

        self.pushButton_9.clicked.connect(self.statistics_btn)

        self.pushButton_10.clicked.connect(self.record_stat)

    def mousePressEvent(self, event):
        self.coords_x = event.pos().x()
        self.coords_y = event.pos().y()
        if len(self.chosen_line_lst) - len(self.lst) - 1 >= 0 and self.flag:
            self.temporary_rusult_label.setGeometry(600, 670, 100, 40)
            self.temporary_rusult_label.setText(f'Правильно: {len(self.right_lst)}/{len(self.chosen_line_lst)}\n'
                                                f'Пройдено: {len(self.chosen_line_lst) - len(self.lst)}/'
                                                f'{len(self.chosen_line_lst)}')
            self.stat_txt = f"{round(len(self.right_lst) / len(self.chosen_line_lst), 2) * 100}%"
            print(self.stat_txt)
            if not self.lst:
                self.flag = False
        self.check()

    def named_map(self):
        self.view.hide()
        self.imagenamed.show()
        self.imagenamed.setPixmap(self.pixmnamed)
        self.imagenamed.setGeometry(231, 10, 461, 640)

    def nonamed_map(self):
        self.view.hide()
        self.imagenamed.show()
        self.imagenamed.setPixmap(self.pixmapnamed)
        self.imagenamed.setGeometry(231, 10, 461, 640)

    def station_choice2(self):
        self.right_lst = []
        self.mode = 'общая'
        con = sqlite3.connect("metro_db.sqlite")
        cur = con.cursor()
        self.lst = cur.execute(f"""SELECT stations_name FROM metro_db""").fetchall()
        self.chosen_line_lst = cur.execute(f"""SELECT stations_name FROM metro_db""").fetchall()
        self.station_name = choice(self.lst)
        self.station.setText(*self.station_name)
        self.lst.remove(self.station_name)
        self.flag = True

    def station_choice3(self):
        self.right_lst = []
        self.mode = 'красная'
        con = sqlite3.connect("metro_db.sqlite")
        cur = con.cursor()
        self.lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'красная'""").fetchall()
        self.chosen_line_lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'красная'""").fetchall()
        self.station_name = choice(self.lst)
        self.station.setText(*self.station_name)
        self.lst.remove(self.station_name)
        self.flag = True

    def station_choice4(self):
        self.right_lst = []
        self.mode = 'синяя'
        con = sqlite3.connect("metro_db.sqlite")
        cur = con.cursor()
        self.lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'синяя'""").fetchall()
        self.chosen_line_lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'синяя'""").fetchall()
        self.station_name = choice(self.lst)
        self.station.setText(*self.station_name)
        self.lst.remove(self.station_name)
        self.flag = True

    def station_choice5(self):
        self.right_lst = []
        self.mode = 'зелёная'
        con = sqlite3.connect("metro_db.sqlite")
        cur = con.cursor()
        self.lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'зелёная'""").fetchall()
        self.chosen_line_lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'зелёная'""").fetchall()
        self.station_name = choice(self.lst)
        self.station.setText(*self.station_name)
        self.lst.remove(self.station_name)
        self.flag = True

    def station_choice6(self):
        self.right_lst = []
        self.mode = 'оранжевая'
        con = sqlite3.connect("metro_db.sqlite")
        cur = con.cursor()
        self.lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'оранжевая'""").fetchall()
        self.chosen_line_lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'оранжевая'""").fetchall()
        self.station_name = choice(self.lst)
        self.station.setText(*self.station_name)
        self.lst.remove(self.station_name)
        self.flag = True

    def station_choice7(self):
        self.right_lst = []
        self.mode = 'фиолетовая'
        con = sqlite3.connect("metro_db.sqlite")
        cur = con.cursor()
        self.lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'фиолетовая'""").fetchall()
        self.chosen_line_lst = cur.execute(f"""SELECT stations_name FROM metro_db
                WHERE lines_color like 'фиолетовая'""").fetchall()
        self.station_name = choice(self.lst)
        self.station.setText(*self.station_name)
        self.lst.remove(self.station_name)
        self.flag = True

    def record_stat(self):
        self.counter += 1
        self.con = sqlite3.connect("metro_db.sqlite")
        self.cur = self.con.cursor()
        self.cur.execute('''INSERT INTO stat (type_of_try, percent)VALUES (?, ?)''',
                         (self.mode, self.stat_txt))
        self.con.commit()

    def statistics_btn(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('metro_db.sqlite')
        if not self.db.open():
            return
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('stat')
        self.model.select()
        self.view = QTableView(self)
        self.view.setModel(self.model)
        self.view.setGeometry(231, 10, 461, 640)
        self.view.show()

        self.imagenamed.hide()

    def check(self):
        if self.mode:
            self.con = sqlite3.connect("metro_db.sqlite")
            self.cur = self.con.cursor()
            clicked_station = self.cur.execute(f"""SELECT stations_name FROM metro_db
                        WHERE  coords_x BETWEEN {self.coords_x - 6} AND {self.coords_x + 6}
                        AND coords_y BETWEEN {self.coords_y - 6} AND {self.coords_y + 6}""").fetchall()
            if clicked_station:
                if self.station_name in clicked_station:
                    self.right_lst.append(self.station_name)
                if self.lst:
                    self.station_name = choice(self.lst)
                    self.station.setText(*self.station_name)
                    self.lst.remove(self.station_name)
                else:
                    self.station.setText('Тест пройден')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
