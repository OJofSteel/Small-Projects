import sys

from PyQt5 import QtWidgets as qtw


def reverse_string_slice(inputted: str):
    return inputted[::-1]


def reverse_string_loop(text: str):
    string = ""
    for i in text:
        string = i + string
    return string


def reverse_string_recursion(text: str):
    # base case
    if len(text) == 0:
        return text
    # recursive case
    else:
        return reverse_string_recursion(text[1:]) + text[0]


def create_stack():
    stack = []
    return stack


def size(stack):
    return len(stack)


def is_empty(stack):
    if size(stack) == 0:
        return True


def push(stack, item):
    stack.append(item)


def pop(stack):
    if is_empty(stack):
        return
    return stack.pop()


def reverse_string_stack(string):
    n = len(string)

    stack = create_stack()

    for i in range(0, n, 1):
        push(stack, string[i])

    string = ""

    for i in range(0, n, 1):
        string += pop(stack)
    return string


def reverse(string):
    string = "".join(reversed(string))
    return string


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = MainWindow()
        self.main_window.show()


class MainWindow(qtw.QWidget):
    inputted_string: str

    def __init__(self):
        super().__init__()
        self.info_label = qtw.QLabel("Please Enter Text")
        self.input_string = qtw.QLabel()
        self.reversed_sliced = qtw.QLabel()
        self.reversed_loop = qtw.QLabel()
        self.reversed_recursion = qtw.QLabel()
        self.reversed_stack = qtw.QLabel()
        self.reversed_reversed = qtw.QLabel()

        self.setWindowTitle("Reverse String")
        self.setMinimumSize(250, 50)

        self.input = qtw.QLineEdit()
        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.info_label)
        self.layout().addWidget(self.input)
        self.layout().addWidget(self.input_string)
        self.layout().addWidget(self.reversed_sliced)
        self.layout().addWidget(self.reversed_loop)
        self.layout().addWidget(self.reversed_recursion)
        self.layout().addWidget(self.reversed_stack)
        self.layout().addWidget(self.reversed_reversed)

        self.input.textChanged.connect(self.inputted_logic)

    def inputted_logic(self):
        self.inputted_string = self.input.text()
        self.input_string.setText("Inputted String: " + self.inputted_string)
        self.reversed_sliced.setText('Reversed using Slicing: ' + reverse_string_slice(self.inputted_string))
        self.reversed_loop.setText("Reversed using loop: " + reverse_string_loop(self.inputted_string))
        self.reversed_recursion.setText("Reversed using recursion: " + reverse_string_recursion(self.inputted_string))
        self.reversed_stack.setText("Reversed using stack: " + reverse_string_stack(self.inputted_string))
        self.reversed_reversed.setText("Reversed using reverse(): " + reverse(self.inputted_string))
        self.adjustSize()


if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())

# Function that reverses the string given
