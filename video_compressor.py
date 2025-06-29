import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
from pathlib import Path

class VideoCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("동영상 크기 줄이기")
        self.root.geometry("600x400")
        
        self.input_file = ""
        self.output_file = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 파일 선택 섹션
        ttk.Label(main_frame, text="동영상 파일 선택:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.file_label = ttk.Label(file_frame, text="파일을 선택하세요", background="white", relief="sunken")
        self.file_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(file_frame, text="파일 선택", command=self.select_file).grid(row=0, column=1)
        
        file_frame.columnconfigure(0, weight=1)
        
        # 압축 설정 섹션
        ttk.Label(main_frame, text="압축 설정:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        
        settings_frame = ttk.Frame(main_frame)
        settings_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 품질 설정
        ttk.Label(settings_frame, text="품질:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.quality_var = tk.StringVar(value="medium")
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.quality_var, 
                                   values=["high", "medium", "low"], state="readonly", width=15)
        quality_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # 해상도 설정
        ttk.Label(settings_frame, text="해상도:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.resolution_var = tk.StringVar(value="original")
        resolution_combo = ttk.Combobox(settings_frame, textvariable=self.resolution_var,
                                      values=["original", "1920x1080", "1280x720", "854x480"], 
                                      state="readonly", width=15)
        resolution_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # 압축 버튼
        ttk.Button(main_frame, text="동영상 압축하기", command=self.compress_video, 
                  style="Accent.TButton").grid(row=4, column=0, columnspan=2, pady=20)
        
        # 진행률 표시
        ttk.Label(main_frame, text="진행률:", font=("Arial", 10)).grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 상태 라벨
        self.status_label = ttk.Label(main_frame, text="준비됨", font=("Arial", 10))
        self.status_label.grid(row=7, column=0, columnspan=2, pady=5)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def select_file(self):
        filetypes = [
            ("동영상 파일", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
            ("모든 파일", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="압축할 동영상 파일을 선택하세요",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file = filename
            self.file_label.config(text=os.path.basename(filename))
            
    def get_compression_settings(self):
        quality = self.quality_var.get()
        resolution = self.resolution_var.get()
        
        # 품질별 CRF 값 설정 (낮을수록 고품질)
        crf_values = {
            "high": "18",
            "medium": "23", 
            "low": "28"
        }
        
        settings = ["-crf", crf_values[quality]]
        
        # 해상도 설정
        if resolution != "original":
            settings.extend(["-vf", f"scale={resolution}"])
            
        return settings
        
    def compress_video(self):
        if not self.input_file:
            messagebox.showerror("오류", "압축할 동영상 파일을 선택하세요.")
            return
            
        # 출력 파일명 생성
        input_path = Path(self.input_file)
        output_filename = f"{input_path.stem}_compressed{input_path.suffix}"
        self.output_file = str(input_path.parent / output_filename)
        
        # 압축 스레드 시작
        self.compression_thread = threading.Thread(target=self.run_compression)
        self.compression_thread.daemon = True
        self.compression_thread.start()
        
    def run_compression(self):
        try:
            self.root.after(0, self.start_progress)
            
            # FFmpeg 명령어 구성
            cmd = ["ffmpeg", "-i", self.input_file]
            cmd.extend(self.get_compression_settings())
            cmd.extend(["-y", self.output_file])  # -y: 덮어쓰기 허용
            
            # FFmpeg 실행
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.root.after(0, self.compression_success)
            else:
                self.root.after(0, lambda: self.compression_error(stderr))
                
        except FileNotFoundError:
            self.root.after(0, lambda: self.compression_error("FFmpeg가 설치되어 있지 않습니다. FFmpeg를 설치해주세요."))
        except Exception as e:
            self.root.after(0, lambda: self.compression_error(str(e)))
            
    def start_progress(self):
        self.progress.start()
        self.status_label.config(text="압축 중...")
        
    def stop_progress(self):
        self.progress.stop()
        
    def compression_success(self):
        self.stop_progress()
        self.status_label.config(text="압축 완료!")
        
        # 파일 크기 비교
        original_size = os.path.getsize(self.input_file) / (1024 * 1024)  # MB
        compressed_size = os.path.getsize(self.output_file) / (1024 * 1024)  # MB
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        message = f"압축이 완료되었습니다!\n\n"
        message += f"원본 크기: {original_size:.1f} MB\n"
        message += f"압축 후 크기: {compressed_size:.1f} MB\n"
        message += f"크기 감소: {reduction:.1f}%\n\n"
        message += f"저장 위치: {self.output_file}"
        
        messagebox.showinfo("압축 완료", message)
        
    def compression_error(self, error_msg):
        self.stop_progress()
        self.status_label.config(text="압축 실패")
        messagebox.showerror("압축 오류", f"압축 중 오류가 발생했습니다:\n{error_msg}")

def main():
    root = tk.Tk()
    app = VideoCompressor(root)
    root.mainloop()

if __name__ == "__main__":
    main()