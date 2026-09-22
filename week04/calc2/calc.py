class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.display = "0"
        self.current_input = "0"
        self.running_total = None
        self.pending_operator = None
        self.is_error = False
        self.last_result_was_equal = False
        self.waiting_for_new_number = False

    def _format_display(self, val):
        res = round(val, 10)
        s = format(res, 'f').rstrip('0').rstrip('.')
        if s == "" or s == "-": return "0"
        if s == "-0": return "0"
        return s

    def _get_current_val_as_float(self):
        try: return float(self.current_input)
        except ValueError: return 0.0

    def _calculate(self, a, b, op):
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/": return a / b if b != 0 else "DIV_ZERO"
        return b

    def press(self, key: str):
        if self.is_error:
            if key == "C": self.reset()
            return
        if key == "C":
            self.reset()
            return
        if key == "BS":
            if self.last_result_was_equal or self.current_input == "0": return
            new_input = self.current_input[:-1]
            if new_input == "" or new_input == "-": new_input = "0"
            elif new_input == ".": new_input = "0"
            if len(new_input) > 1 and new_input.startswith("0") and new_input[1] != ".":
                new_input = new_input.lstrip("0")
                if not new_input: new_input = "0"
                elif new_input.startswith("."): new_input = "0" + new_input
            self.current_input = new_input
            self.display = self.current_input
            return
        if key == "+/-":
            if self.current_input == "0": pass
            elif self.current_input.startswith("-"): self.current_input = self.current_input[1:]
            else: self.current_input = "-" + self.current_input
            if self.current_input == "-0": self.current_input = "0"
            elif self.current_input.startswith("-0."): pass
            elif len(self.current_input) > 1 and self.current_input.startswith("-0") and self.current_input[2] != ".":
                self.current_input = "-" + self.current_input[2:].lstrip("0")
                if not self.current_input.startswith("-"): self.current_input = "-" + self.current_input
            self.display = self.current_input
            return
        if key == "%":
            try:
                val = float(self.current_input) / 100.0
                self.current_input = self._format_display(val)
                self.display = self.current_input
            except: pass
            return
        if key in "0123456789.":
            if self.last_result_was_equal:
                self.current_input, self.running_total, self.pending_operator = "", None, None
                self.last_result_was_equal = self.waiting_for_new_number = False
            if key == ".":
                if "." in self.current_input: return
                self.current_input = "0." if self.current_input == "0" else self.current_input + "."
            else:
                if len(self.current_input.replace(".", "").replace("-", "")) >= 12: return
                if self.current_input == "0": self.current_input = key
                else: self.current_input += key
                if len(self.current_input) > 1 and self.current_input.startswith("0") and self.current_input[1] != ".":
                    self.current_input = self.current_input.lstrip("0")
                    if not self.current_input: self.current_input = "0"
                    elif self.current_input.startswith("."): self.current_input = "0" + self.current_input
            self.display, self.waiting_for_new_number = self.current_input, False
            return
        if key in "+-*/=":
            if self.last_result_was_equal:
                if key == "=": return
                self.last_result_was_equal, self.current_input, self.waiting_for_new_number = False, self.display, False
            if key == "=":
                if self.pending_operator is None or self.waiting_for_new_number:
                    self.last_result_was_equal = True
                    return
                try:
                    res = self._calculate(self.running_total, self._get_current_val_as_float(), self.pending_operator)
                    if res == "DIV_ZERO":
                        self.is_error, self.display = True, "0으로 나눌 수 없습니다"
                        return
                    self.display, self.current_input, self.running_total = self._format_display(res), self._format_display(res), res
                    self.pending_operator, self.last_result_was_equal, self.waiting_for_new_number = None, True, True
                except: self.is_error, self.display = True, "Error"
                return
            if self.waiting_for_new_number:
                self.pending_operator = key
                return
            try:
                if self.pending_operator is None: self.running_total = self._get_current_val_as_float()
                else:
                    res = self._calculate(self.running_total, self._get_current_val_as_float(), self.pending_operator)
                    if res == "DIV_ZERO":
                        self.is_error, self.display = True, "0으로 나눌 수 없습니다"
                        return
                    self.display, self.current_input, self.running_total = self._format_display(res), self._format_display(res), res
                self.pending_operator, self.waiting_for_new_number = key, True
            except: self.is_error, self.display = True, "Error"
