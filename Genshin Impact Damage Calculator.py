import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


# from PyQt5 import QtGui as qtg


def crit_bonus(crit_rate: float, crit_dmg: float):
    return 1 + ((crit_rate / 100) * (crit_dmg / 100))


def defense(player_level: int, enemy_level: int, defense_drop: float = 1):
    return (100 + player_level) / ((100 + player_level) + (100 + enemy_level) * defense_drop)


def eff_atk(atk, dmg):
    return atk * (1 + (dmg / 100))


def damage_on_crit(eff_attack, crit_dmg, ability, resistance, total_defense):
    return eff_attack * (ability / 100) * (1 + (crit_dmg / 100)) * total_defense * (1 - (resistance / 100))


def damage_on_non_crit(eff_attack, ability, resistance, total_defense):
    return eff_attack * (ability / 100) * total_defense * (1 - (resistance / 100))


def average_damage(eff_attack, total_crit_bonus, ability, resistance, total_defense):
    return eff_attack * (ability / 100) * total_crit_bonus * total_defense * (1 - (resistance / 100))


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = MainWindow()
        self.calc_window = CalcWindow()
        self.weapon_compare_window = WeaponCompareWindow()
        self.calc_result_window = CalcResultWindow()
        self.main_window.show()

        self.main_window.calculation_requested.connect(self.calc_window.show)
        self.main_window.weapon_comparison_requested.connect(self.weapon_compare_window.show)

        self.calc_window.submitted.connect(self.calc_result_window.initial_logic)


class MainWindow(qtw.QWidget):
    calculation_requested = qtc.pyqtSignal()
    weapon_comparison_requested = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Genshin Impact Calculators")
        self.setMinimumSize(260, 260)

        self.calc_button = qtw.QPushButton("Calculate Damage")
        self.weapon_compare_button = qtw.QPushButton("Compare Weapons")

        self.setLayout(qtw.QGridLayout())
        self.layout().addWidget(self.calc_button)
        self.layout().addWidget(self.weapon_compare_button)

        self.calc_button.clicked.connect(self.calculation_requested.emit)
        self.weapon_compare_button.clicked.connect(self.weapon_comparison_requested.emit)


# noinspection PyArgumentList
class WeaponCompareWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genshin Weapon Comparison")
        self.setMinimumSize(580, 440)

        self.frame1 = qtw.QFrame()
        self.frame1.setGeometry(qtc.QRect(320, 150, 118, 3))
        self.frame1.setFrameShape(qtw.QFrame.VLine)
        self.frame1.setFrameShadow(qtw.QFrame.Sunken)

        self.frame2 = qtw.QFrame()
        self.frame2.setGeometry(qtc.QRect(1, 1, 1, 1))
        self.frame2.setFrameShape(qtw.QFrame.VLine)
        self.frame2.setFrameShadow(qtw.QFrame.Sunken)

        self.character_atk_spinbox = qtw.QSpinBox(maximum=99999)
        self.character_asc_spinbox = qtw.QDoubleSpinBox(maximum=9999, suffix="%")
        self.character_ability_spinbox = qtw.QDoubleSpinBox(maximum=9999, suffix="%")
        self.character_level_spinbox = qtw.QSpinBox(maximum=99999)
        self.enemy_level_spinbox = qtw.QSpinBox(maximum=99999)
        self.resistance_spinbox = qtw.QDoubleSpinBox(maximum=999, suffix="%")

        self.character_asc_stat = qtw.QComboBox()
        self.character_resonance = qtw.QComboBox()
        self.artifact_dmg_set_bonus_type = qtw.QComboBox()
        self.character_asc_stat.addItems(["None", "ATK%", "Crit Rate%", "Crit Dmg%", "Physical%", "Elemental%"])
        self.character_resonance.addItems(["None", "Anemo", "Cryo", "Electro", "Geo", "Hydro", "Pyro"])
        self.artifact_dmg_set_bonus_type.addItems(["None", "Dmg%", "Skill%", "Burst%", "Physical%", "Elemental%",
                                                   "Normal Attack%", "Charged Attack%", "Normal/Charged Attack%"])

        self.artifact_atk_spinbox = qtw.QSpinBox(maximum=99999)
        self.artifact_crit_rate_spinbox = qtw.QDoubleSpinBox(maximum=100, suffix="%")
        self.artifact_crit_dmg_spinbox = qtw.QDoubleSpinBox(maximum=9999, suffix="%")
        self.artifact_dmg_set_bonus_spinbox = qtw.QDoubleSpinBox(maximum=9999, suffix="%")
        self.artifact_dmg_spinbox = qtw.QDoubleSpinBox(maximum=9999, suffix="%")
        self.atk_set_bonus = qtw.QCheckBox("+18% ATK%")
        self.crit_rate_set_bonus = qtw.QCheckBox("+12% Crit Rate%")
        self.dmg_set_bonus = qtw.QCheckBox("Dmg% Set Bonus: ")
        self.number_of_weapons = qtw.QSpinBox(maximum=50)
        self.weapon_number_submit = qtw.QPushButton("Apply")
        self.submit_button = qtw.QPushButton("Submit", styleSheet="font: bold")

        self.upper_spacer = qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)

        self.character_stat_layout = qtw.QGridLayout()
        self.character_stat_layout.addWidget(qtw.QLabel("Character", styleSheet="font: bold"))
        self.character_stat_layout.addWidget(qtw.QLabel("Character Base ATK:"), 1, 0)
        self.character_stat_layout.addWidget(self.character_atk_spinbox, 1, 1)
        self.character_stat_layout.addWidget(qtw.QLabel("Ability%:"), 2, 0)
        self.character_stat_layout.addWidget(self.character_ability_spinbox, 2, 1)
        self.character_stat_layout.addWidget(qtw.QLabel("Player Level:"), 3, 0)
        self.character_stat_layout.addWidget(self.character_level_spinbox, 3, 1)
        self.character_stat_layout.addWidget(qtw.QLabel("Enemy Level:"), 4, 0)
        self.character_stat_layout.addWidget(self.enemy_level_spinbox, 4, 1)
        self.character_stat_layout.addWidget(qtw.QLabel("Enemy Resistance:"), 5, 0)
        self.character_stat_layout.addWidget(self.resistance_spinbox, 5, 1)
        self.character_stat_layout.addWidget(qtw.QLabel("Resonance:"), 6, 0)
        self.character_stat_layout.addWidget(self.character_resonance, 6, 1)
        self.character_stat_layout.addWidget(qtw.QLabel("Ascension Stat:"), 7, 0)
        self.character_stat_layout.addWidget(self.character_asc_stat, 7, 1)
        self.character_stat_layout.addWidget(self.character_asc_spinbox, 7, 2)

        self.artifact_stat_layout = qtw.QGridLayout()
        self.artifact_stat_layout.addWidget(qtw.QLabel("Artifacts", styleSheet="font: bold"))
        self.artifact_stat_layout.addWidget(qtw.QLabel("Total Artifact ATK:"), 1, 0)
        self.artifact_stat_layout.addWidget(self.artifact_atk_spinbox, 1, 2, 1, 2)
        self.artifact_stat_layout.addWidget(qtw.QLabel("Total Artifact Dmg%:"), 2, 0)
        self.artifact_stat_layout.addWidget(self.artifact_dmg_spinbox, 2, 2, 1, 2)
        self.artifact_stat_layout.addWidget(qtw.QLabel("Total Artifact Crit Rate%:"), 3, 0)
        self.artifact_stat_layout.addWidget(self.artifact_crit_rate_spinbox, 3, 2, 1, 2)
        self.artifact_stat_layout.addWidget(qtw.QLabel("Total Artifact Crit Dmg%:"), 4, 0)
        self.artifact_stat_layout.addWidget(self.artifact_crit_dmg_spinbox, 4, 2, 1, 2)
        self.artifact_stat_layout.addWidget(qtw.QLabel("Set Bonuses", styleSheet="font: bold"), 5, 0)
        self.artifact_stat_layout.addWidget(self.atk_set_bonus, 6, 0)
        self.artifact_stat_layout.addWidget(self.frame2, 6, 1, 2, 1)
        self.artifact_stat_layout.addWidget(self.crit_rate_set_bonus, 6, 2)
        self.artifact_stat_layout.addWidget(self.dmg_set_bonus, 7, 0)
        self.artifact_stat_layout.addWidget(self.artifact_dmg_set_bonus_type, 8, 0)
        self.artifact_stat_layout.addWidget(self.artifact_dmg_set_bonus_spinbox, 8, 2)

        self.weapon_boxes = qtw.QWidget()
        self.weapon_box_scrollArea = qtw.QScrollArea()
        self.weapon_box_layout = qtw.QVBoxLayout()

        self.weapon_box_scrollArea.setWidgetResizable(True)
        self.weapon_box_scrollArea.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.MinimumExpanding)
        self.weapon_box_scrollArea.setWidget(self.weapon_boxes)

        self.weapon_boxes.setLayout(self.weapon_box_layout)
        self.weapon_box_scrollArea.setMinimumHeight(200)
        self.weapon_box_scrollArea.setMaximumHeight(300)

        self.setLayout(qtw.QGridLayout())
        self.layout().addLayout(self.character_stat_layout, 0, 0, 1, 3)
        self.layout().addWidget(self.frame1, 0, 3, 2, 1)
        self.layout().addLayout(self.artifact_stat_layout, 0, 4, 2, 2)
        self.layout().addWidget(qtw.QLabel("Number of Weapons:"), 1, 0)
        self.layout().addWidget(self.number_of_weapons, 1, 1)
        self.layout().addWidget(self.weapon_number_submit, 1, 2)
        self.layout().addWidget(self.weapon_box_scrollArea, 2, 0, 1, 6)
        self.layout().addWidget(self.submit_button, 3, 0, 1, 6)
        self.layout().addItem(self.upper_spacer, 4, 0)

        self.weapon_number_submit.clicked.connect(self.create_weapon_box)
        self.submit_button.clicked.connect(self.submit_weapon)

    def submit_weapon(self):
        self.char_atk = int(self.character_atk_spinbox.text())
        self.char_crit_rate = 5
        self.char_crit_dmg = 50
        self.ability = float(self.character_ability_spinbox.cleanText())
        self.player_level = int(self.character_level_spinbox.text())
        self.enemy_level = int(self.enemy_level_spinbox.text())
        self.resistance = float(self.resistance_spinbox.cleanText())
        self.resonance = self.character_resonance.currentText()
        self.asc_type = self.character_asc_stat.currentText()
        self.asc_num = float(self.character_asc_spinbox.cleanText())
        self.art_atk = int(self.artifact_atk_spinbox.text())
        self.art_dmg = float(self.artifact_dmg_spinbox.cleanText())
        self.art_crit_rate = float(self.artifact_crit_rate_spinbox.cleanText())
        self.art_crit_dmg = float(self.artifact_crit_dmg_spinbox.cleanText())
        self.atk_set = self.atk_set_bonus.isChecked()
        self.crit_set = self.crit_rate_set_bonus.isChecked()
        self.dmg_set = self.dmg_set_bonus.isChecked()
        self.dmg_set_type = self.artifact_dmg_set_bonus_type.currentText()
        self.dmg_set_num = float(self.artifact_dmg_set_bonus_spinbox.cleanText())

        self.interim_atk = self.char_atk + self.art_atk
        if self.asc_type == "Physical%" or self.asc_type == "Elemental%":
            self.interim_dmg = self.asc_num + self.art_dmg
            self.asc_atk = 0
            self.interim_crit_rate = self.art_crit_rate + self.char_crit_rate
            self.interim_crit_dmg = self.art_crit_dmg + self.char_crit_dmg
        elif self.asc_type == "ATK%":
            self.interim_dmg = self.art_dmg
            self.asc_atk = self.asc_num
            self.interim_crit_rate = self.art_crit_rate + self.char_crit_rate
            self.interim_crit_dmg = self.art_crit_dmg + self.char_crit_dmg
        elif self.asc_type == "Crit Rate%":
            self.interim_dmg = self.art_dmg
            self.asc_atk = 0
            self.interim_crit_rate = self.asc_num + self.art_crit_rate + self.char_crit_rate
            self.interim_crit_dmg = self.art_crit_dmg + self.char_crit_dmg
        elif self.asc_type == "Crit Dmg%":
            self.interim_dmg = self.art_dmg
            self.asc_atk = 0
            self.interim_crit_rate = self.art_crit_rate + self.char_crit_rate
            self.interim_crit_dmg = self.asc_num + self.art_crit_dmg + self.char_crit_dmg
        else:
            self.interim_dmg = self.art_dmg
            self.asc_atk = 0
            self.interim_crit_rate = self.art_crit_rate + self.char_crit_rate
            self.interim_crit_dmg = self.art_crit_dmg + self.char_crit_dmg

        if self.atk_set:
            self.interim_atk_per = self.asc_atk + 18
        else:
            self.interim_atk_per = self.asc_atk

        if self.crit_set:
            self.second_interim_crit_rate = self.interim_crit_rate + 12
        else:
            self.second_interim_crit_rate = self.interim_crit_rate

        if self.dmg_set:
            self.second_interim_dmg = self.dmg_set_num + self.interim_dmg
        else:
            self.second_interim_dmg = self.interim_dmg

        for i in range(self.weapon_box_layout.count()):
            self.wep_name = self.weapon_box_layout.itemAt(i).widget().layout().itemAt(0).widget().text()
            self.wep_atk = int(self.weapon_box_layout.itemAt(i).widget().layout().itemAt(2).widget().text())
            self.wep_sec_stat = self.weapon_box_layout.itemAt(i).widget().layout().itemAt(5).widget().currentText()
            self.wep_sec_num = float(self.weapon_box_layout.itemAt(i).widget().layout().itemAt(6).widget().cleanText())
            print("Weapon Name: " + str(self.wep_name))
            print("Weapon ATK: " + str(self.wep_atk))
            print("Weapon Sec Stat: " + str(self.wep_sec_stat))
            print("Weapon Sec Stat Value: " + str(self.wep_sec_num))

            self.base_atk = self.wep_atk + self.char_atk
            if self.wep_sec_stat == "ATK%":
                print("Interim: " + str(self.interim_atk_per))
                print("Weapon ATK%: " + str(self.wep_sec_num))
                self.final_atk_per = self.interim_atk_per + self.wep_sec_num
                self.final_crit_rate = self.second_interim_crit_rate
                self.final_crit_dmg = self.interim_crit_dmg
                self.final_dmg = self.second_interim_dmg
            elif self.wep_sec_stat == "Crit Rate%":
                self.final_atk_per = self.interim_atk_per
                self.final_crit_rate = self.second_interim_crit_rate + self.wep_sec_num
                self.final_crit_dmg = self.interim_crit_dmg
                self.final_dmg = self.second_interim_dmg
            elif self.wep_sec_stat == "Crit Dmg%":
                self.final_atk_per = self.interim_atk_per
                self.final_crit_rate = self.second_interim_crit_rate
                self.final_crit_dmg = self.interim_crit_dmg + self.wep_sec_num
                self.final_dmg = self.second_interim_dmg
            elif self.wep_sec_stat == "Physical%" or self.wep_sec_stat == "Elemental%":
                self.final_atk_per = self.interim_atk_per
                self.final_crit_rate = self.second_interim_crit_rate
                self.final_crit_dmg = self.interim_crit_dmg
                self.final_dmg = self.second_interim_dmg + self.wep_sec_num
            else:
                self.final_atk_per = self.interim_atk_per
                self.final_crit_rate = self.second_interim_crit_rate
                self.final_crit_dmg = self.interim_crit_dmg
                self.final_dmg = self.second_interim_dmg

            self.total_atk = self.base_atk + self.art_atk + (self.base_atk * (self.final_atk_per/100))
            print(self.total_atk)
            self.eff_atk = eff_atk(self.total_atk, self.final_dmg)
            self.total_crit_bonus = crit_bonus(self.final_crit_rate, self.final_crit_dmg)
            self.total_defense = defense(self.player_level, self.enemy_level)
            self.average_dmg = average_damage(self.eff_atk, self.total_crit_bonus, self.ability,
                                              self.resistance, self.total_defense)
            self.non_crit = damage_on_non_crit(self.eff_atk, self.ability, self.resistance, self.total_defense)
            self.crit = damage_on_crit(self.eff_atk, self.final_crit_dmg, self.ability,
                                       self.resistance, self.total_defense)
            print("Crit Dmg%: " + str(self.final_crit_dmg))
            print("Eff. ATK: " + str(self.eff_atk))
            print("Tot. Crit: " + str(self.total_crit_bonus))
            print("Tot. Defense: " + str(self.total_defense))
            print("Average Dmg: " + str(self.average_dmg))
            print("Non-Crit Dmg: " + str(self.non_crit))
            print("Crit Dmg: " + str(self.crit))



    def create_weapon_box(self):
        for i in reversed(range(self.weapon_box_layout.count())):
            self.weapon_box_layout.itemAt(i).widget().setParent(None)

        for i in range(0, int(self.number_of_weapons.text())):
            self.frame1 = qtw.QFrame()
            self.frame1.setGeometry(qtc.QRect(320, 150, 118, 3))
            self.frame1.setFrameShape(qtw.QFrame.VLine)
            self.frame1.setFrameShadow(qtw.QFrame.Sunken)

            self.weapon_box = qtw.QWidget()
            self.weapon_name = qtw.QLineEdit(placeholderText="Weapon " + str(i + 1) + ": Enter Weapon Name")
            self.weapon_atk_spinbox = qtw.QSpinBox(maximum=9999)
            self.weapon_sub_stat_name = qtw.QComboBox(placeholderText="Choose Sub Stat")
            self.weapon_sub_stat_name.addItems(["None", "ATK%", "Crit Rate%", "Crit Dmg%", "Physical%", "Elemental%"])
            self.weapon_sub_stat_name.setCurrentIndex(0)
            self.weapon_sub_spinbox = qtw.QDoubleSpinBox(maximum=9999, suffix="%")

            self.weapon_box.setLayout(qtw.QGridLayout())
            self.weapon_box.layout().addWidget(self.weapon_name, 0, 0, 1, 2)
            self.weapon_box.layout().addWidget(qtw.QLabel("Weapon ATK: "), 1, 0)
            self.weapon_box.layout().addWidget(self.weapon_atk_spinbox, 1, 1)
            self.weapon_box.layout().addWidget(self.frame1, 0, 3, 2, 1)
            self.weapon_box.layout().addWidget(qtw.QLabel("Weapon Sub Stat: "), 0, 4)
            self.weapon_box.layout().addWidget(self.weapon_sub_stat_name, 1, 4)
            self.weapon_box.layout().addWidget(self.weapon_sub_spinbox, 1, 5)

            self.weapon_box.setStyleSheet(".QWidget {border: 1px solid black}")

            self.weapon_box_layout.addWidget(self.weapon_box)


# noinspection PyArgumentList
class CalcWindow(qtw.QWidget):
    submitted = qtc.pyqtSignal(int, float, float, float, float, int, int, float)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Genshin Damage Calculator")
        self.setMinimumSize(260, 260)

        self.atk_input = qtw.QSpinBox(maximum=99999)
        self.dmg_input = qtw.QDoubleSpinBox(maximum=99999, suffix="%")
        self.ability_input = qtw.QDoubleSpinBox(maximum=99999, suffix="%")
        self.crit_rate_input = qtw.QDoubleSpinBox(maximum=100, suffix="%")
        self.crit_dmg_input = qtw.QDoubleSpinBox(maximum=99999, suffix="%")
        self.player_level_input = qtw.QSpinBox(maximum=1000)
        self.enemy_level_input = qtw.QSpinBox(maximum=1000)
        self.enemy_resistance_input = qtw.QDoubleSpinBox(maximum=100, suffix="%")

        self.submit_button = qtw.QPushButton("Submit")

        self.main_layout = qtw.QVBoxLayout()
        self.input_layout = qtw.QFormLayout()
        self.input_layout.addRow("ATK:", self.atk_input)
        self.input_layout.addRow("DMG%:", self.dmg_input)
        self.input_layout.addRow("Ability%:", self.ability_input)
        self.input_layout.addRow("Crit Rate%:", self.crit_rate_input)
        self.input_layout.addRow("Crit DMG%:", self.crit_dmg_input)
        self.input_layout.addRow("Player Level:", self.player_level_input)
        self.input_layout.addRow("Enemy Level:", self.enemy_level_input)
        self.input_layout.addRow("Enemy Resistance%:", self.enemy_resistance_input)

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.submit_button)

        self.setLayout(self.main_layout)

        self.submit_button.clicked.connect(self.submit_verification)

    def error_box(self, error_title: str, error_message: str):
        qtw.QMessageBox(parent=self,
                        text=error_message,
                        icon=qtw.QMessageBox.Warning,
                        windowTitle=error_title).exec_()

    def convert_to_int(self, inputted_text, index):
        if inputted_text != "":
            try:
                int(inputted_text)
            except ValueError:
                self.error_box("Invalid Input", "Please input a whole number for " +
                               self.input_layout.itemAt(index).widget().text()[:-1])
                return False
            else:
                return True
        else:
            self.error_box("Invalid Input", "Please input a whole number for " +
                           self.input_layout.itemAt(index).widget().text()[:-1])
            return False

    def convert_to_float(self, inputted_text, index):
        if inputted_text != "":
            try:
                float(inputted_text)
            except ValueError:
                self.error_box("Invalid Input", "Please input a number for " +
                               self.input_layout.itemAt(index).widget().text()[:-1])
                return False
            else:
                return True
        else:
            self.error_box("Invalid Input", "Please input a number for " +
                           self.input_layout.itemAt(index).widget().text()[:-1])
            return False

    def submit_verification(self):
        if (self.convert_to_int(self.atk_input.text(), 0) and
                self.convert_to_float(self.dmg_input.cleanText(), 2) and
                self.convert_to_float(self.ability_input.cleanText(), 4) and
                self.convert_to_float(self.crit_rate_input.cleanText(), 6) and
                self.convert_to_float(self.crit_dmg_input.cleanText(), 8) and
                self.convert_to_int(self.player_level_input.cleanText(), 10) and
                self.convert_to_int(self.enemy_level_input.cleanText(), 12) and
                self.convert_to_float(self.enemy_resistance_input.cleanText(), 14)):
            self.submitted.emit(int(self.atk_input.cleanText()), float(self.dmg_input.cleanText()),
                                float(self.ability_input.cleanText()), float(self.crit_rate_input.cleanText()),
                                float(self.crit_dmg_input.cleanText()), int(self.player_level_input.cleanText()),
                                int(self.enemy_level_input.cleanText()), float(self.enemy_resistance_input.cleanText()))


class CalcResultWindow(qtw.QWidget):
    defense: float
    crit_bonus: float

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Results")
        self.setMinimumSize(300, 210)
        self.setWindowModality(qtc.Qt.ApplicationModal)

        self.atk_label = qtw.QLabel()
        self.dmg_label = qtw.QLabel()
        self.eff_atk_label = qtw.QLabel()
        self.crit_rate_label = qtw.QLabel()
        self.crit_dmg_label = qtw.QLabel()
        self.crit_bonus_label = qtw.QLabel()
        self.player_level_label = qtw.QLabel()
        self.enemy_level_label = qtw.QLabel()
        self.defense_label = qtw.QLabel()
        self.enemy_resistance_label = qtw.QLabel()
        self.ability_label = qtw.QLabel()
        self.average_damage_label = qtw.QLabel()
        self.average_damage_label_static = qtw.QLabel("Average Damage: ")
        self.crit_damage_label = qtw.QLabel()
        self.crit_damage_label_static = qtw.QLabel("Damage on Crit: ")
        self.non_crit_damage_label = qtw.QLabel()
        self.non_crit_damage_label_static = qtw.QLabel("Damage on Non-Crit: ")

        self.frame1 = qtw.QFrame()
        self.frame1.setGeometry(qtc.QRect(320, 150, 118, 3))
        self.frame1.setFrameShape(qtw.QFrame.HLine)
        self.frame1.setFrameShadow(qtw.QFrame.Sunken)

        self.frame2 = qtw.QFrame()
        self.frame2.setGeometry(qtc.QRect(320, 150, 118, 3))
        self.frame2.setFrameShape(qtw.QFrame.HLine)
        self.frame2.setFrameShadow(qtw.QFrame.Sunken)

        self.eff_atk_layout = qtw.QFormLayout()
        self.eff_atk_layout.addRow("ATK: ", self.atk_label)
        self.eff_atk_layout.addRow("DMG%: ", self.dmg_label)
        self.eff_atk_layout.addRow("Effective ATK: ", self.eff_atk_label)

        self.crit_bonus_layout = qtw.QFormLayout()
        self.crit_bonus_layout.addRow("Crit Rate%: ", self.crit_rate_label)
        self.crit_bonus_layout.addRow("Crit DMG%: ", self.crit_dmg_label)
        self.crit_bonus_layout.addRow("Total Crit Bonus: ", self.crit_bonus_label)

        self.defense_layout = qtw.QFormLayout()
        self.defense_layout.addRow("Player Level: ", self.player_level_label)
        self.defense_layout.addRow("Enemy Level: ", self.enemy_level_label)
        self.defense_layout.addRow("Enemy Defense: ", self.defense_label)

        self.misc_stats_layout = qtw.QFormLayout()
        self.misc_stats_layout.addRow("Enemy Resistance: ", self.enemy_resistance_label)
        self.misc_stats_layout.addRow("Ability%: ", self.ability_label)

        self.average_damage_layout = qtw.QGridLayout()
        self.left_spacer = qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.right_spacer = qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.upper_spacer = qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        self.average_damage_layout.addItem(self.left_spacer, 4, 0)
        self.average_damage_layout.addItem(self.right_spacer, 4, 3)
        self.average_damage_layout.addItem(self.upper_spacer, 4, 1)
        self.average_damage_layout.addWidget(self.non_crit_damage_label_static, 0, 1)
        self.average_damage_layout.addWidget(self.non_crit_damage_label, 0, 2)
        self.average_damage_layout.addWidget(self.crit_damage_label_static, 1, 1)
        self.average_damage_layout.addWidget(self.crit_damage_label, 1, 2)
        self.average_damage_layout.addWidget(self.average_damage_label_static, 2, 1)
        self.average_damage_layout.addWidget(self.average_damage_label, 2, 2)

        self.setLayout(qtw.QGridLayout())
        self.layout().addLayout(self.eff_atk_layout, 0, 0)
        self.layout().addWidget(self.frame1, 1, 0, 1, 2)
        self.layout().addLayout(self.crit_bonus_layout, 0, 1)
        self.layout().addLayout(self.defense_layout, 2, 0)
        self.layout().addLayout(self.misc_stats_layout, 2, 1)
        self.layout().addWidget(self.frame2, 3, 0, 1, 2)
        self.layout().addLayout(self.average_damage_layout, 4, 0, 1, 2)

    @qtc.pyqtSlot(int, float, float, float, float, int, int, float)
    def initial_logic(self, atk, dmg, ability, crit_rate, crit_dmg, player_level, enemy_level, enemy_resistance):
        self.crit_bonus = crit_bonus(crit_rate, crit_dmg)
        self.defense = defense(player_level, enemy_level)
        self.eff_atk = eff_atk(atk, dmg)
        self.average_damage = average_damage(self.eff_atk, self.crit_bonus, ability, enemy_resistance, self.defense)
        self.on_crit_damage = damage_on_crit(self.eff_atk, crit_dmg, ability, enemy_resistance, self.defense)
        self.on_non_crit_damage = damage_on_non_crit(self.eff_atk, ability, enemy_resistance, self.defense)

        self.show()
        self.atk_label.setText(str(atk))
        self.dmg_label.setText("{:.2%}".format(dmg / 100))
        self.ability_label.setText("{:.2%}".format(ability / 100))
        self.crit_rate_label.setText("{:.2%}".format(crit_rate / 100))
        self.crit_dmg_label.setText("{:.2%}".format(crit_dmg / 100))
        self.player_level_label.setText(str(player_level))
        self.enemy_level_label.setText(str(enemy_level))
        self.enemy_resistance_label.setText("{:.2%}".format(enemy_resistance / 100))

        self.crit_bonus_label.setText("{:.2%}".format(self.crit_bonus))
        self.defense_label.setText("{:.2%}".format(self.defense))
        self.eff_atk_label.setText("{:.2f}".format(self.eff_atk))
        self.average_damage_label.setText("{:.2f}".format(self.average_damage))
        self.crit_damage_label.setText("{:.2f}".format(self.on_crit_damage))
        self.non_crit_damage_label.setText("{:.2f}".format(self.on_non_crit_damage))


if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
