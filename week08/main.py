import tkinter as tk
from tkinter import ttk, messagebox
from calculator import calculate_fee, get_duration_str

class ParkingSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("주차 요금 관리 시스템")
        self.root.geometry("600x500")

        # 데이터 저장 리스트: [{"entry": "09:00", "exit": "10:00", "duration": "1시간 0분", "fee": 1500}, ...]
        self.payment_list = []

        self.setup_ui()

    def setup_ui(self):
        # --- 1. 입력 영역 ---
        input_frame = tk.LabelFrame(self.root, text="요금 계산 입력", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="입차 시각 (HH:MM):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_entry_time = tk.Entry(input_frame, width=10)
        self.entry_entry_time.grid(row=0, column=1, padx=5, pady=5)
        self.entry_entry_time.insert(0, "09:00")

        tk.Label(input_frame, text="출차 시각 (HH:MM):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_exit_time = tk.Entry(input_frame, width=10)
        self.entry_exit_time.grid(row=0, column=3, padx=5, pady=5)
        self.entry_exit_time.insert(0, "10:00")

        self.btn_calculate = tk.Button(input_frame, text="계산 및 추가", command=self.add_payment, bg="#e1e1e1")
        self.btn_calculate.grid(row=0, column=4, padx=10, pady=5)

        # --- 2. 목록 영역 (Treeview) ---
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("entry", "exit", "duration", "fee")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("entry", text="입차 시각")
        self.tree.heading("exit", text="출차 시각")
        self.tree.heading("duration", text="주차 시간")
        self.tree.heading("fee", text="요금")

        self.tree.column("entry", width=100, anchor="center")
        self.tree.column("exit", width=100, anchor="center")
        self.tree.column("duration", width=120, anchor="center")
        self.tree.column("fee", width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)

        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # --- 3. 삭제 버튼 영역 ---
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.btn_delete = tk.Button(btn_frame, text="선택 항목 삭제", command=self.delete_selected, fg="red")
        self.btn_delete.pack(side="right")

        # --- 4. 합계 영역 ---
        self.lbl_total_sum = tk.Label(self.root, text="오늘의 총 합계: 0원", font=("맑은 고딕", 14, "bold"), pady=10)
        self.lbl_total_sum.pack()

    def add_payment(self):
        entry = self.entry_entry_time.get().strip()
        exit_t = self.entry_exit_time.get().strip()

        try:
            # 요금 계산 (calculator.py 사용)
            fee = calculate_fee(entry, exit_t)
            duration = get_duration_str(entry, exit_t)

            # 데이터 저장
            payment_data = {
                "entry": entry,
                "exit": exit_t,
                "duration": duration,
                "fee": fee
            }
            self.payment_list.append(payment_data)

            # Treeview에 추가 (요금은 콤마 포함)
            self.tree.insert("", "end", values=(
                payment_data["entry"],
                payment_data["exit"],
                payment_data["duration"],
                f"{payment_data['fee']:,}원"
            ))

            self.update_total_sum()
            
        except ValueError as e:
            messagebox.showerror("입력 오류", str(e))

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("알림", "삭제할 항목을 선택해주세요.")
            return

        if messagebox.askyesno("확인", "정말로 이 항목을 삭제하시겠습니까?"):
            for item in selected_item:
                # Treeview에서 인덱스 찾아 실제 데이터 리스트에서도 삭제
                index = self.tree.index(item)
                self.payment_list.pop(index)
                self.tree.delete(item)
            
            self.update_total_sum()

    def update_total_sum(self):
        total = sum(item["fee"] for item in self.payment_list)
        self.lbl_total_sum.config(text=f"오늘의 총 합계: {total:,}원")

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingSystemApp(root)
    root.mainloop()
