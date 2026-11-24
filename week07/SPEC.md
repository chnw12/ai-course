기술
Python 3.10 이상, Flet 1.0. 다른 패키지는 쓰지 않는다. 파이썬에 들어 있는 모듈(random, json 등)은 쓸 수 있다.
Flet은 1.0에서 문법이 크게 바뀌었다. 아래 코드는 화면 파일 main.py의 시작 코드(뼈대)이고, Flet 1.0에서 동작을 확인한 것이다. main.py는 이 뼈대를 그대로 가져와 넓혀서 만든다. 계산 파일 logic.py에는 뼈대가 없고 처음부터 만든다.
뼈대에 나온 Flet 문법만 쓴다. 뼈대에 없는 Flet 클래스, 인자, 속성은 쓰지 않는다. 기억하고 있는 Flet 문법은 옛 버전의 것이므로 쓰지 않는다.
특히 다음은 Flet 1.0에 없으므로 쓰면 오류가 난다: ft.app(...), ft.colors, ft.alignment.center, ft.ElevatedButton, Button(text=...), page.window_width, ft.UserControl, TextField(error_text=...)