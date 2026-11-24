import unittest
import os
import json
from logic import (
    validate_length, 
    check_options_count, 
    generate_password, 
    save_password_to_json, 
    load_passwords_from_json
)

class TestLogic(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_passwords.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # 1. validate_length 테스트
    def test_validate_length(self):
        self.assertTrue(validate_length(4))
        self.assertTrue(validate_length(32))
        self.assertTrue(validate_length(10))
        self.assertFalse(validate_length(3))
        self.assertFalse(validate_length(33))
        self.assertFalse(validate_length(0))

    # 2. check_options_count 테스트
    def test_check_options_count(self):
        self.assertTrue(check_options_count(2))
        self.assertTrue(check_options_count(3))
        self.assertFalse(check_options_count(0))
        self.assertFalse(check_options_count(1))

    # 3. generate_password 테스트
    def test_generate_password(self):
        length = 12
        # Case: All options selected
        pwd = generate_password(length, True, True, True)
        self.assertEqual(len(pwd), length)
        self.assertTrue(any(c.islower() for c in pwd))
        self.assertTrue(any(c.isupper() for c in pwd))
        self.assertTrue(any(c.isdigit() for c in pwd))
        self.assertTrue(any(c in "!@#$%^&*" for c in pwd))

        # Case: Only lowercase (though spec says we need 2 more to activate button, 
        # the function itself should still work if called)
        pwd_simple = generate_password(length, False, False, False)
        self.assertEqual(len(pwd_simple), length)
        self.assertTrue(all(c.islower() for c in pwd_simple))

    # 4. JSON 저장 및 로드 테스트
    def test_json_storage(self):
        # Test saving and loading
        success = save_password_to_json(self.test_file, "Google", "password123")
        self.assertTrue(success)
        
        data = load_passwords_from_json(self.test_file)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["site"], "Google")
        self.assertEqual(data[0]["password"], "password123")

        # Test multiple entries
        save_password_to_json(self.test_file, "Naver", "naver456")
        data = load_passwords_from_json(self.test_file)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[1]["site"], "Naver")

        # Test non-existent file
        empty_data = load_passwords_from_json("non_existent.json")
        self.assertEqual(empty_data, [])

if __name__ == "__main__":
    # Custom runner to match the required output format: "통과: N개, 실패: M개"
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLogic)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    
    # Convert unittest results to the requested format
    # Note: unittest doesn't give easy access to individual test counts without a custom runner, 
    # but we can calculate it from the result object.
    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    passed_tests = total_tests - failed_tests
    
    print(f"\n테스트 결과 - 통과: {passed_tests}개, 실패: {failed_tests}개")
    
    if failed_tests == 0:
        exit(0)
    else:
        exit(1)
