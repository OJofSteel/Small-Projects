import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = MainWindow()
        self.result_window = ResultWindow()
        self.main_window.show()

        self.main_window.submitted.connect(self.result_window.initial_logic)


# noinspection PyArgumentList
class MainWindow(qtw.QWidget):
    submitted = qtc.pyqtSignal(int, float, float, float, float, int, int, float)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Genshin Impact Damage Calculator")
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


def crit_bonus(crit_rate: float, crit_dmg: float):
    return 1 + ((crit_rate / 100) * (crit_dmg / 100))


def defense(player_level: int, enemy_level: int, defense_drop: float = 1):
    return (100 + player_level) / ((100 + player_level) + (100 + enemy_level) * defense_drop)


def eff_atk(atk, dmg):
    return atk * (1 + (dmg / 100))


def damage_on_crit(eff_attack, crit_dmg, ability, resistance, total_defense):
    return eff_attack * (ability/100) * (1 + (crit_dmg/100)) * total_defense * (1-(resistance/100))


def damage_on_non_crit(eff_attack, ability, resistance, total_defense):
    return eff_attack * (ability/100) * total_defense * (1-(resistance/100))


def average_damage(eff_attack, total_crit_bonus, ability, resistance, total_defense):
    return eff_attack * (ability/100) * total_crit_bonus * total_defense * (1-(resistance/100))


class ResultWindow(qtw.QWidget):
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
