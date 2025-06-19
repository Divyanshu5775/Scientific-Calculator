import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt

class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Scientific Calculator")
        self.setGeometry(300, 100, 500, 600)
        self.angle_mode = "DEG"
        self.history = []
        self.last_answer = ""
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #121212; color: white;")

        main_layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            background-color: #1E1E1E;
            color: white;
            font-size: 24px;
            padding: 10px;
            border: none;
        """)
        main_layout.addWidget(self.display)

        self.history_label = QLabel("History: ")
        self.history_label.setStyleSheet("font-size: 14px; color: gray;")
        main_layout.addWidget(self.history_label)

        mode_layout = QHBoxLayout()
        self.mode_box = QComboBox()
        self.mode_box.addItems(["DEG", "RAD"])
        self.mode_box.currentTextChanged.connect(self.change_mode)
        self.mode_box.setStyleSheet("""
            background-color: #2E2E2E;
            color: white;
            border: none;
            padding: 5px;
        """)
        mode_layout.addWidget(QLabel("Angle Mode: "))
        mode_layout.addWidget(self.mode_box)
        main_layout.addLayout(mode_layout)

        grid = QGridLayout()
        buttons = [
            ["7", "8", "9", "/", "sin"],
            ["4", "5", "6", "*", "cos"],
            ["1", "2", "3", "-", "tan"],
            ["0", ".", "=", "+", "log"],
            ["(", ")", "C", "DEL", "ln"],
            ["π", "e", "^", "√", "exp"],
            ["!", "%", "abs", "Ans", "Clear History"]
        ]

        for row, line in enumerate(buttons):
            for col, btn_text in enumerate(line):
                btn = QPushButton(btn_text)
                btn.setFixedHeight(40)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2E2E2E;
                        color: white;
                        font-weight: bold;
                        border: 1px solid #444;
                    }
                    QPushButton:hover {
                        background-color: #3C3C3C;
                    }
                """)
                btn.clicked.connect(self.handle_input)
                grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def change_mode(self, mode):
        self.angle_mode = mode

    def handle_input(self):
        btn = self.sender()
        text = btn.text()
        expr = self.display.text()

        try:
            if text == "=":
                result = self.evaluate(expr)
                self.display.setText(str(result))
                self.last_answer = str(result)
                self.history.append(f"{expr} = {result}")
                self.update_history()

            elif text == "C":
                self.display.clear()
            elif text == "DEL":
                self.display.setText(expr[:-1])
            elif text == "Ans":
                self.display.setText(expr + self.last_answer)
            elif text == "Clear History":
                self.history = []
                self.update_history()
            else:
                self.display.setText(expr + text)

        except Exception:
            self.display.setText("Error")

    def update_history(self):
        hist_text = "History:\n" + "\n".join(self.history[-5:])
        self.history_label.setText(hist_text)

    def evaluate(self, expr):
        # Replace constants
        expr = expr.replace('π', str(math.pi))
        expr = expr.replace('e', str(math.e))

        # Replace operations
        expr = expr.replace('^', '**')
        expr = expr.replace('√', 'math.sqrt')
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('ln', 'math.log')
        expr = expr.replace('exp', 'math.exp')
        expr = expr.replace('abs', 'math.fabs')

        # Angle-based trig functions
        if self.angle_mode == "DEG":
            expr = expr.replace('sin', 'math.sin(math.radians')
            expr = expr.replace('cos', 'math.cos(math.radians')
            expr = expr.replace('tan', 'math.tan(math.radians')
            expr = self.auto_close(expr, ['math.sin(', 'math.cos(', 'math.tan('])
        else:
            expr = expr.replace('sin', 'math.sin')
            expr = expr.replace('cos', 'math.cos')
            expr = expr.replace('tan', 'math.tan')

        # Handle factorial (!)
        while '!' in expr:
            idx = expr.index('!')
            num = ''
            i = idx - 1
            while i >= 0 and (expr[i].isdigit() or expr[i] == '.'):
                num = expr[i] + num
                i -= 1
            expr = expr[:i+1] + f'math.factorial({num})' + expr[idx+1:]

        # Final evaluation
        return eval(expr)

    def auto_close(self, expr, funcs):
        for func in funcs:
            idx = 0
            while (idx := expr.find(func, idx)) != -1:
                idx_end = idx + len(func)
                count = 1
                i = idx_end
                while i < len(expr) and count > 0:
                    if expr[i] == '(':
                        count += 1
                    elif expr[i] == ')':
                        count -= 1
                    i += 1
                expr = expr[:i] + ')' + expr[i:]
                idx = i + 1
        return expr

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = ScientificCalculator()
    calc.show()
    sys.exit(app.exec_())
