import flet as ft
import logic
import os

# 파일 경로 설정
PASSWORD_FILE = "passwords.json"

def main(page: ft.Page):
    page.title = "비밀번호 생성기 & 관리자"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.window_height = 750
    page.padding = 20
    page.scroll = "auto"

    # --- 상태 변수 ---
    state = {
        "current_password": "",
        "is_password_generated": False
    }

    # --- UI 컴포넌트 선언 ---
    
    # 1. 홈페이지 이름 입력
    site_name_input = ft.TextField(label="홈페이지 이름", hint_text="예: Google, Naver", expand=True)

    # 2. 길이 입력
    length_input = ft.TextField(
        label="비밀번호 길이", 
        value="12", 
        width=150
    )
    length_error_text = ft.Text("", color="red", size=12)

    # 3. 옵션 체크박스
    upper_check = ft.Checkbox(label="대문자 (A-Z)", value=False)
    number_check = ft.Checkbox(label="숫자 (0-9)", value=False)
    special_check = ft.Checkbox(label="특수문자 (!@#$%^&*)", value=False)
    lower_check = ft.Checkbox(label="소문자 (a-z)", value=True, read_only=True)

    # 4. 결과 표시
    password_display = ft.TextField(label="생성된 비밀번호", read_only=True, text_size=16)
    
    # 5. 버튼들
    btn_generate = ft.ElevatedButton(
        "생성", 
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREY_400)
    )
    btn_regenerate = ft.ElevatedButton(
        "다시 만들기", 
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE),
        visible=False
    )
    btn_save = ft.ElevatedButton(
        "저장", 
        disabled=True,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREY_400)
    )
    btn_list = ft.ElevatedButton(
        "목록 보기", 
        icon=ft.icons.LIST
    )
    btn_copy = ft.IconButton(
        icon=ft.icons.COPY
    )

    # --- 로직 함수 구현 ---

    def update_button_states(e=None):
        try:
            length_val = int(length_input.value)
            is_len_valid = logic.validate_length(length_val)
        except ValueError:
            is_len_valid = False
            length_val = 0

        if length_val != 0 and not is_len_valid:
            length_error_text.value = "길이는 4~32 사이여야 합니다."
        else:
            length_error_text.value = ""
        
        checked_options = sum([upper_check.value, number_check.value, special_check.value])
        is_options_valid = logic.check_options_count(checked_options)

        can_generate = is_len_valid and is_options_valid
        btn_generate.disabled = not can_generate
        btn_generate.style.bgcolor = ft.colors.BLUE if can_generate else ft.colors.GREY_400
        
        btn_save.disabled = not state["is_password_generated"]
        btn_save.style.bgcolor = ft.colors.BLUE if state["is_password_generated"] else ft.colors.GREY_400
        page.update()

    def generate_action(e):
        try:
            length_val = int(length_input.value)
        except ValueError:
            length_val = 0

        if not logic.validate_length(length_val):
            page.snack_bar = ft.SnackBar(ft.Text("비밀번호 길이를 4~32 사이로 설정해주세요!"))
            page.snack_bar.open = True
            page.update()
            return

        new_pwd = logic.generate_password(
            length=length_val,
            use_upper=upper_check.value,
            use_number=number_check.value,
            use_special=special_check.value
        )
        
        state["current_password"] = new_pwd
        state["is_password_generated"] = True
        password_display.value = new_pwd
        
        btn_regenerate.visible = True
        btn_regenerate.disabled = False
        btn_regenerate.style.bgcolor = ft.colors.BLUE
        
        btn_save.disabled = False
        btn_save.style.bgcolor = ft.colors.BLUE
        page.update()

    def save_action(e):
        if not site_name_input.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("홈페이지 이름을 입력해주세요!"))
            page.snack_bar.open = True
            page.update()
            return

        success = logic.save_password_to_json(PASSWORD_FILE, site_name_input.value, state["current_password"])
        if success:
            page.snack_bar = ft.SnackBar(ft.Text("성공적으로 저장되었습니다!"))
            site_name_input.value = ""
        else:
            page.snack_bar = ft.SnackBar(ft.Text("저장에 실패했습니다."))
        page.snack_bar.open = True
        page.update()

    def copy_action(e):
    # --- 팝업 기능 ---
    def create_list_item(item):
        site = item["site"]
        pwd = item["password"]
        pwd_text = ft.Text("*" * len(pwd), weight="bold")
        
        def toggle_visibility(e):
            if pwd_text.value == "*" * len(pwd):
                pwd_text.value = pwd
                e.control.icon = ft.icons.visibility
            else:
                pwd_text.value = "*" * len(pwd)
                e.control.icon = ft.icons.visibility_off
        dialog.update()

        return ft.ListTile(
            leading=ft.Icon(ft.icons.LOCK_PERSON),
            title=ft.Text(site),
            subtitle=pwd_text,
            trailing=ft.IconButton(icon=ft.icons.visibility_off, on_click=toggle_visibility)
        )

    def show_list_dialog(e):
        items = logic.load_passwords_from_json(PASSWORD_FILE)
        list_view = ft.ListView(expand=True, spacing=10, padding=10)
        
        if not items:
            list_view.controls.append(ft.Text("저장된 비밀번호가 없습니다.", text_align="center"))
        else:
            for item in items:
                list_view.controls.append(create_list_item(item))

        dialog = ft.AlertDialog(
            title=ft.Text("저장된 비밀번호 목록"),
            content=ft.Container(
                content=list_view,
                height=400,
                width=400,
            ),
            actions=[
                ft.TextButton("닫기", on_click=lambda _: close_dialog())
            ],
        )
        
        def close_dialog():
            dialog.open = False
            page.update()

        page.dialog = dialog
        dialog.open = True
        page.update()

    # 연결 (Event Binding)
    length_input.on_change = update_button_states
    upper_check.on_change = update_button_states
    number_check.on_change = update_button_states
    special_check.on_change = update_button_states
    btn_generate.on_click = generate_action
    btn_regenerate.on_click = generate_action
    btn_save.on_click = save_action
    btn_list.on_click = show_list_dialog
    btn_copy.on_click = copy_action

    # 레이아웃 구성
    page.add(
        ft.Column(
            [
                ft.Text("비밀번호 생성기", size=30, weight="bold", color=ft.colors.BLUE),
                ft.Divider(),
                
                ft.Text("1. 정보 입력", size=18, weight="bold"),
                site_name_input,
                ft.Row([length_input, length_error_text], alignment=ft.MainAxisAlignment.START),
                
                ft.Text("2. 옵션 선택", size=18, weight="bold"),
                lower_check,
                upper_check,
                number_check,
                special_check,
                
                ft.Divider(),
                
                ft.Text("3. 생성 결과", size=18, weight="bold"),
                ft.Row([
                    password_display,
                    btn_copy
                ]),
                
                ft.Row([
                    btn_generate,
                    btn_regenerate,
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Row([
                    btn_save,
                    btn_list,
                ], alignment=ft.MainAxisAlignment.CENTER),
                
            ],
            spacing=15,
        )
    )

    update_button_states()

if __name__ == "__main__":
    ft.run(main)

    if state["current_password"]:
            page.set_clipboard(state["current_password"])
            page.snack_bar = ft.SnackBar(ft.Text("클립보드에 복사되었습니다!"))
            page.snack_bar.open = True
            page.update()
