import sys
import timeit

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


def time_function(function_name, text):
    times = timeit.timeit(lambda: function_name(text), number=10000)
    return "{:2f}".format(times) + "s"


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = MainWindow()
        self.main_window.show()


class MainWindow(qtw.QWidget):
    inputted_string: str

    def __init__(self):
        super().__init__()

        self.slice_time_text = "Time to slice: "
        self.loop_time_text = "Time to loop: "
        self.recursion_time_text = "Time to recurse: "
        self.stack_time_text = "Time to stack: "
        self.reversed_time_text = "Time to reverse(): "

        self.info_label = qtw.QLabel("Please Enter Text")
        self.input_string = qtw.QLabel("Inputted Text: ")
        self.reversed_sliced = qtw.QLabel('Reversed using slicing: ')
        self.reversed_loop = qtw.QLabel("Reversed using loop: ")
        self.reversed_recursion = qtw.QLabel("Reversed using recursion: ")
        self.reversed_stack = qtw.QLabel("Reversed using stack: ")
        self.reversed_reversed = qtw.QLabel("Reversed using reverse(): ")

        self.slice_time = qtw.QLabel(self.slice_time_text)
        self.loop_time = qtw.QLabel(self.loop_time_text)
        self.recursion_time = qtw.QLabel(self.recursion_time_text)
        self.stack_time = qtw.QLabel(self.stack_time_text)
        self.reversed_time = qtw.QLabel(self.reversed_time_text)

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
        self.layout().addWidget(self.slice_time)
        self.layout().addWidget(self.loop_time)
        self.layout().addWidget(self.recursion_time)
        self.layout().addWidget(self.stack_time)
        self.layout().addWidget(self.reversed_time)

        self.input.textChanged.connect(self.inputted_logic)
        self.input.editingFinished.connect(self.edited)

    def inputted_logic(self):
        self.inputted_string = self.input.text()
        self.input_string.setText("Inputted Text: " + self.inputted_string)
        self.reversed_sliced.setText('Reversed using slicing: ' + reverse_string_slice(self.inputted_string))
        self.reversed_loop.setText("Reversed using loop: " + reverse_string_loop(self.inputted_string))
        self.reversed_recursion.setText("Reversed using recursion: " + reverse_string_recursion(self.inputted_string))
        self.reversed_stack.setText("Reversed using stack: " + reverse_string_stack(self.inputted_string))
        self.reversed_reversed.setText("Reversed using reverse(): " + reverse(self.inputted_string))
        self.adjustSize()

    def edited(self):
        self.slice_time.setText(self.slice_time_text + time_function(reverse_string_slice, self.inputted_string))
        self.loop_time.setText(self.loop_time_text + time_function(reverse_string_loop, self.inputted_string))
        self.recursion_time.setText(self.recursion_time_text + time_function(reverse_string_recursion,
                                                                             self.inputted_string))
        self.stack_time.setText(self.stack_time_text + time_function(reverse_string_stack, self.inputted_string))
        self.reversed_time.setText(self.reversed_time_text + time_function(reverse, self.inputted_string))


if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
