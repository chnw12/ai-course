from datetime import datetime, timedelta

def calculate_fee(entry_str: str, exit_str: str) -> int:
    try:
        fmt = "%H:%M"
        entry_time = datetime.strptime(entry_str, fmt)
        exit_time = datetime.strptime(exit_str, fmt)

        if exit_time < entry_time:
            exit_time += timedelta(days=1)

        # [수정된 야간 무료 로직]
        # 18:00부터 다음날 06:00까지 출차 시 무료
        # 시간/분까지 고려하여 정확히 06:00:00까지 무료로 처리
        # Python의 datetime 비교를 사용하여 더 직관적으로 수정
        
        # 야간 무료 시간대인지 확인하기 위해 기준 시각 설정
        # 18:00(오늘) ~ 06:00(내일)
        night_start = entry_time.replace(hour=18, minute=0, second=0, microsecond=0)
        night_end = entry_time.replace(hour=6, minute=0, second=0, microsecond=0)
        if night_end < night_start: # 자정을 넘기는 경우
            night_end += timedelta(days=1)

# 06시 00분 00초까지 포함하기 위해 hour <= 6 이 아니라, 
# 06시 00분 01초부터는 유료로 처리되도록 조건을 조정합니다.
# 가장 깔끔한 방법은 시간/분까지 비교하는 것입니다
        if exit_time.hour >= 18 or (exit_time.hour == 6 and exit_time.minute == 0 and exit_time.second == 0) or exit_time.hour < 6:
            return 0

        duration_minutes = int((exit_time - entry_time).total_seconds() / 60)

        if duration_minutes <= 30:
            return 0

        extra_minutes = duration_minutes - 30
        units_of_10 = (extra_minutes + 9) // 10
        fee = units_of_10 * 500

        if fee > 20000:
            fee = 20000

        return fee

    except ValueError as e:
        raise ValueError(f"Invalid time format. Use HH:MM. Error: {e}")


def get_duration_str(entry_str: str, exit_str: str) -> str:
    """주차 시간을 'H시간 M분' 형식으로 반환합니다."""
    fmt = "%H:%M"
    entry_time = datetime.strptime(entry_str, fmt)
    exit_time = datetime.strptime(exit_str, fmt)
    if exit_time < entry_time:
        exit_time += timedelta(days=1)
        
    diff = exit_time - entry_time
    hours, remainder = divmod(int(diff.total_seconds() / 60), 60)
    mins = remainder
    
    if hours > 0:
        return f"{hours}시간 {mins}분"
    else:
        return f"{mins}분"
