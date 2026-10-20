import unittest
import sys
from calculator import calculate_fee

class TestCalculator(unittest.TestCase):
    def test_free_period(self):
        # TC-01: 30분 이내 무료
        self.assertEqual(calculate_fee("09:00", "09:20"), 0)
        # TC-02: 30분 경계값
        self.assertEqual(calculate_fee("09:00", "09:30"), 0)

    def test_extra_fee(self):
        # TC-03: 30분 초과 (31분 -> 500원)
        self.assertEqual(calculate_fee("09:00", "09:31"), 500)
        # TC-04: 60분 주차 (30분 무료 + 30분 유료 -> 3*500 = 1500원)
        self.assertEqual(calculate_fee("09:00", "10:00"), 1500)
        # TC-08: 45분 주차 (30분 무료 + 15분 -> 20분 부과 = 1000원)
        self.assertEqual(calculate_fee("10:00", "10:45"), 1000)

    def test_night_free(self):
        # TC-05: 18시 이후 출차 시 무료
        self.assertEqual(calculate_fee("17:00", "18:30"), 0)
        # TC-06: 06시 이전 출차 시 무료
        self.assertEqual(calculate_fee("05:00", "06:00"), 0)

    def test_max_fee(self):
        # 18시 이전인 09:00 ~ 15:00 주차 (최대 요금 확인)
        # 6시간 = 360분. (360-30)/10 = 33단위. 33 * 500 = 16500원.
        # 아, 2만원을 넘으려면 최소 460분(7시간 40분) 이상 주차해야 합니다.
        # 09:00 ~ 17:00 (8시간) -> (480-30)=450분 -> 45단위 -> 22500원 -> 20000원 제한 적용 확인
        self.assertEqual(calculate_fee("09:00", "17:00"), 20000)


    def test_next_day_exit(self):
        # 입차 23:00, 출차 01:00 (익일 출차, 01시는 06시 이전이므로 무료)
        self.assertEqual(calculate_fee("23:00", "01:00"), 0)

if __name__ == "__main__":
    print("=== 주차 요금 계산기 테스트 시작 ===")
    # verbosity=2를 통해 상세한 결과를 볼 수 있습니다.
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*30)
    print(f"테스트 결과 보고")
    print(f"총 테스트 실행: {result.testsRun} 건")
    print(f"성공(Pass): {result.testsRun - len(result.failures) - len(result.errors)} 건")
    print(f"실패(Fail): {len(result.failures)} 건")
    print(f"에러(Error): {len(result.errors)} 건")
    print("="*30)
    
    if not result.wasSuccessful():
        sys.exit(1)
    else:
        sys.exit(0)
