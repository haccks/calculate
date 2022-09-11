import tkinter as tk
from tkinter import ttk, font

GRAY = "#808080"
BLACK = "#1C1C1C"
LIVER = "#505050"
ORANGE = "#FF9500"
GAINSBORO = "#DCDCDC"
BUTTONS = {
    'C': (1, 0),
    '\u00B1': (1, 1),  # Todo: Not implemented
    '%': (1, 2),
    '\u00F7': (1, 3),
    '\u00D7': (2, 3),
    '-': (3, 3),
    '+': (4, 3),
    '=': (5, 3)
}
DIGITS = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['0', '0', '.']
]


class CalculatorFrame(ttk.Frame):
    """Frame to contain all other widgets.

    This frame will be attached to the main window (container) and will act as a container
    for all other widgets. Main window will act as master for this frame.
    """
    def __init__(self, container):
        """Initialize the frame.

        Initialize the frame and create/initialize all widgets attached to it.
        :param container: Master window.
        """
        super().__init__(container)
        self.grid(row=0, column=0)
        # self.grid_rowconfigure(0, minsize=70)
        self.rowconfigure(0, minsize=70)        # This will set and fix the height of display widget in pixel.
                                                # Same effect with height, image and compound options set for display
        # self.columnconfigure(0, minsize=60)
        self.pack_propagate(False)
        self.result = ''         # Will be set only when '=' key is pressed. Unset when clear is pressed
        self.expression = ''     # Mathematical expression to be evaluated
        self.txt_input = ''      # User input or result of the evaluated expression to be displayed on label
        self.display_font = font.Font(family='Helvetica', size=35)
        self.display_txt = tk.StringVar()
        self.pixel = tk.PhotoImage(width=1, height=1)

        self.display = tk.Label(
            self,
            relief=tk.SUNKEN,
            font=self.display_font,
            bg=BLACK,
            fg=GAINSBORO,
            textvariable=self.display_txt,
            anchor=tk.E,
            borderwidth=0,
            padx=10,
            pady=10,
            width=8,
            # height=70,
            # image=self.pixel,
            # compound='bottom'
        )
        self.display_txt.set('0')
        self.display.grid(row=0, column=0, sticky='nsew', columnspan=4)

        self.digit_buttons()
        self.operation_buttons()

    def digit_buttons(self):
        """Create digit buttons.

        Create all digit buttons including '.' and attach it to this frame.
        """
        for i in range(2, 6):
            for j in range(3):
                cs = 2 if i == 5 and j == 0 else 1
                if i == 5 and j == 1:
                    continue

                btn = tk.Button(
                    self,
                    text=DIGITS[i-2][j],
                    relief=tk.RAISED,
                    width=2,
                    font=('Helvetica', 16),
                    bg=GRAY,
                    fg=GAINSBORO,
                    borderwidth=0,
                    command=lambda d=DIGITS[i-2][j]: self.update_display(d)
                )
                btn.grid(row=i, column=j, ipadx=5, ipady=5, columnspan=cs, sticky='ew')
                btn.config(highlightbackground=BLACK)

    def operation_buttons(self):
        """Create operations button.

        Create all operation buttons including clear all and sign change and attach is to this frame.
        """
        for key, value in BUTTONS.items():
            if key in ['C', '\u00B1', '%']:
                bg_color = LIVER
            else:
                bg_color = ORANGE
            btn = tk.Button(
                self,
                text=key,
                relief=tk.RAISED,
                width=2, height=1,
                font=('Helvetica', 16),
                bg=bg_color,
                fg=GAINSBORO,
                borderwidth=0,
                command=lambda op=key: self.calculate(op)
            )
            btn.grid(row=value[0], column=value[1], ipadx=5, ipady=5)
            btn.config(highlightbackground=BLACK)

    def resize_font(self, text):
        """Resize display font.

        Dynamically adjust the font size of display.
        :param text: Current text on the calculator display.
        """
        char_pix = self.display_font.measure('0')
        lbl_width = self.display.cget('width')
        lbl_pix_width = char_pix * lbl_width

        font_size = self.display_font.actual('size')
        temp_font = font.Font(**self.display_font.config())
        text_size = temp_font.measure(text)

        while True:
            # print(text_size)
            if text_size > lbl_pix_width:
                font_size -= 1
                temp_font.config(size=font_size)
                text_size = temp_font.measure(text)
            else:
                break

        # print(text_size, font_size)
        self.display.config(font=temp_font)
        # print(self.lbl.cget('height'))

    def update_display(self, exp=''):
        """Update display text.

        Update display to show user input and the evaluated expression result.
        :param exp: Character input from the user.
        """
        if exp == '.':
            if not self.txt_input:                      # Display .num to 0.num (.1 -> 0.1)
                self.txt_input = '0'
            elif self.txt_input[-1] == '.':             # No multiple '.' should be together (ex: 2.....3 is not valid)
                self.txt_input = self.txt_input[:-1]
                self.expression = self.expression[:-1]
            elif '.' in self.txt_input:                 # No multiple '.' in a number (ex: 22.3.2 is not valid)
                return
        elif self.expression == '' and exp == '0':        # Remove any leading zero (012 is invalid. It should be 12)
            self.display_txt.set('0')
            self.txt_input = ''
            return

        self.txt_input += str(exp)
        self.expression += str(exp)
        print(self.expression)
        self.resize_font(self.txt_input)
        self.display_txt.set(self.txt_input)

    def all_clear(self):
        """Reset all variables and display widget.

        """
        self.result = ''
        self.expression = ''
        self.txt_input = ''
        self.display_txt.set('0')
        self.display.config(font=self.display_font)

    def evaluate(self):
        """Evaluate the mathematical expression formed.

        """
        try:
            # self.expression = self.expression.replace('\u00F7', '/')
            # self.expression = self.expression.replace('\u00D7', '*')
            if self.expression:
                self.txt_input = str(eval(self.expression))
                self.result = self.txt_input
                self.expression = ''
                self.update_display()
                self.txt_input = ''
        except ZeroDivisionError or Exception:
            self.expression = '1/0'
            self.txt_input = 'Not a number'
            self.update_display()
            self.txt_input = ''

    def calculate(self, operator):  # Todo: Bind keyboard keys to buttons.
        """Calculate the result.

        Form mathematical expression which will be evaluated further.
        :param operator: Operator to perform operation.
        """
        if operator == 'C':
            self.all_clear()

        elif operator == '=':
            self.evaluate()

        else:
            if not self.expression:  # If an operator key is pressed just after '=' then expression should be the result
                self.expression = self.result

            if operator == '\u00F7':
                operator = '/'
            elif operator == '\u00D7':
                operator = '*'
            if self.expression and self.expression[-1] in ['+', '-', '/', '*', '%']:
                # No two operators should be together
                self.expression = self.expression[:-1]
            elif not self.expression:  # If expression is empty and any operator pressed then do nothing
                return
            self.expression += operator
            self.txt_input = ''


class Calculator(tk.Tk):
    """Main window application.

    It will act as a main container for all other frames and widgets.
    """
    def __init__(self):
        super().__init__()

        # self.geometry('230x300')
        self.resizable(False, False)
        self.config(background=BLACK)
        img = tk.PhotoImage(file='calc.png')
        self.iconphoto(True, img)


if __name__ == '__main__':
    calc = Calculator()    # Create main window
    CalculatorFrame(calc)  # Create frame and attach it to main window
    calc.mainloop()
