import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw

class NinePatchEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("나인패치 이미지 에디터")

        # 이미지 관련 변수
        self.img = None
        self.img_tk = None
        self.img_canvas = None
        self.stretch_region = [0, 0, 0, 0]
        self.padding_region = [0, 0, 0, 0]

        # UI 레이아웃 구성
        self.setup_ui()

        self.root.mainloop()

    def setup_ui(self):
        # 파일 열기 버튼
        tk.Button(self.root, text="이미지 선택", command=self.load_image).grid(row=0, column=0, columnspan=4, pady=10)

        # 이미지 표시용 캔버스
        self.img_canvas = tk.Canvas(self.root, width=500, height=500, bg="gray")
        self.img_canvas.grid(row=1, column=0, columnspan=4)

        # 슬라이드 바 구성
        labels = ["확장 x1", "확장 y1", "확장 x2", "확장 y2", "패딩 x1", "패딩 y1", "패딩 x2", "패딩 y2"]
        self.sliders = []

        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=2 + i, column=0, padx=5, pady=5)
            slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_preview)
            slider.grid(row=2 + i, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
            slider.config(length=600)  # 슬라이더 바 길이 두 배로 설정
            self.sliders.append(slider)

        # 저장 버튼
        tk.Button(self.root, text="9-patch 저장", command=self.save_nine_patch).grid(row=10, column=0, columnspan=4, pady=10)

    def load_image(self):
        # 파일 탐색기로 이미지 선택
        file_path = filedialog.askopenfilename(
            title="말풍선 이미지 선택",
            filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.bmp"), ("모든 파일", "*.*")]
        )
        if not file_path:
            return

        # 이미지 로드
        self.img = Image.open(file_path)
        self.img_tk = ImageTk.PhotoImage(self.img)

        # 캔버스 크기와 이미지 크기 동기화
        width, height = self.img.size
        self.img_canvas.config(width=width, height=height)
        self.img_canvas.create_image(0, 0, anchor="nw", image=self.img_tk)

        # 슬라이드 바의 범위 설정
        for i, slider in enumerate(self.sliders):
            if i % 2 == 0:  # x 좌표 슬라이더
                slider.config(to=width - 1)
            else:  # y 좌표 슬라이더
                slider.config(to=height - 1)

    def update_preview(self, _=None):
        if self.img is None:
            return

        # 슬라이더 값 가져오기
        values = [slider.get() for slider in self.sliders]
        self.stretch_region = values[:4]
        self.padding_region = values[4:]

        # 미리보기 업데이트
        preview_img = self.img.copy()
        draw = ImageDraw.Draw(preview_img)
        width, height = preview_img.size

        # 확장 영역
        x1, y1, x2, y2 = self.stretch_region
        draw.line([(x1, 0), (x2, 0)], fill="red", width=7)  # 상단
        draw.line([(0, y1), (0, y2)], fill="red", width=7)  # 왼쪽

        # 패딩 영역
        px1, py1, px2, py2 = self.padding_region
        draw.line([(px1, height - 1), (px2, height - 1)], fill="red", width=3)  # 하단
        draw.line([(width - 1, py1), (width - 1, py2)], fill="red", width=3)  # 오른쪽

        # 캔버스에 미리보기 이미지 갱신
        self.img_tk = ImageTk.PhotoImage(preview_img)
        self.img_canvas.create_image(0, 0, anchor="nw", image=self.img_tk)

    def save_nine_patch(self):
        if self.img is None:
            messagebox.showerror("오류", "이미지를 먼저 선택하세요.")
            return

        # 파일 저장 경로 선택
        output_path = filedialog.asksaveasfilename(
            title="출력 파일 저장",
            defaultextension=".9.png",
            filetypes=[("PNG 파일", "*.9.png"), ("모든 파일", "*.*")]
        )
        if not output_path:
            return

        # 1픽셀 테두리를 추가한 새로운 이미지 생성
        original_width, original_height = self.img.size
        nine_patch = Image.new("RGBA", (original_width + 2, original_height + 2), (0, 0, 0, 0))
        nine_patch.paste(self.img, (1, 1))

        # 9-patch 영역 표시
        draw = ImageDraw.Draw(nine_patch)

        # 확장 영역
        x1, y1, x2, y2 = self.stretch_region
        draw.line([(x1 + 1, 0), (x2 + 1, 0)], fill="black")
        draw.line([(0, y1 + 1), (0, y2 + 1)], fill="black")

        # 패딩 영역
        px1, py1, px2, py2 = self.padding_region
        draw.line([(px1 + 1, original_height + 1), (px2 + 1, original_height + 1)], fill="black")
        draw.line([(original_width + 1, py1 + 1), (original_width + 1, py2 + 1)], fill="black")

        # 결과 저장
        nine_patch.save(output_path, "PNG")
        messagebox.showinfo("완료", f"9-patch 이미지가 {output_path} 경로에 저장되었습니다.")


if __name__ == "__main__":
    NinePatchEditor()
