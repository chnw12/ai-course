import unittest
from calc import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_cases(self):
        tests = [
            ([], "0"),
            ("1 2 + 3 =".split(), "15"),
            ("2 + 3 * 4 =".split(), "20"),
            ("5 + - 3 =".split(), "2"),
            ("0 . 1 + 0 . 2 =".split(), "0.3"),
            ("6 / 3 =".split(), "2"),
            ("7 / 2 =".split(), "3.5"),
            ("5 / 0 =".split(), "0으로 나눌 수 없습니다"),
            ("5 / 0 = 7".split(), "0으로 나눌 수 없습니다"),
            ("5 / 0 = C".split(), "0"),
            ("1 . . 5".split(), "1.5"),
            (".".split(), "0."),
            ("0 0 7".split(), "7"),
            ("1 2 3 BS".split(), "12"),
            ("5 BS".split(), "0"),
            ("9 +/-".split(), "-9"),
            ("5 0 %".split(), "0.5"),
            ("2 + 3 = 4".split(), "4"),
            ("2 + 3 = + 4 =".split(), "9"),
            ("2 + 3 = =".split(), "5"),
        ]

        all_passed = True
        for i, (inputs, expected) in enumerate(tests):
            self.calc.reset()
            for key in inputs:
                self.calc.press(key)
            
            if self.calc.display != expected:
                print(f"Test {i+1} FAILED: input={inputs}, expected='{expected}', actual='{self.calc.display}'")
                all_passed = False
        
        if all_passed:
            print(f"모든 테스트 통과 ({len(tests)}개)")
        else:
            exit(1)

if __name__ == "__main__":
    test_obj = TestCalculator()
    test_obj.setUp()
    test_obj.test_cases()
