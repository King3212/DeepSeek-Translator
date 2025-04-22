import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import time
from openai import OpenAI

class DeepSeekTranslatorApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("DeepSeek Translator")
        self.root.geometry("1200x800")  # 增大窗口尺寸
        
        # 设置更大的默认字体
        self.default_font = ('Arial', 14)
        self.root.option_add('*Font', self.default_font)
        # API Key
        self.api_key = ""
        
        # 创建主框架和画布用于滚动
        self.create_scrollable_interface()
        
        # Create UI elements
        self.create_widgets()
        
        # 绑定鼠标滚轮事件
        self.bind_mouse_wheel()
        
    def create_scrollable_interface(self):
        """创建可滚动的界面"""
        # 创建主框架容器
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建画布
        self.canvas = tk.Canvas(self.main_container)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        self.scrollbar = ttk.Scrollbar(self.main_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置画布
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # 创建内部框架用于放置所有部件
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
    def bind_mouse_wheel(self):
        """绑定鼠标滚轮事件"""
        # 绑定鼠标滚轮到画布
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # 对于Linux系统，需要绑定Button-4和Button-5
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)
        
    def _on_mousewheel(self, event):
        """Windows和Mac的鼠标滚轮处理"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _on_mousewheel_linux(self, event):
        """Linux的鼠标滚轮处理"""
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        
    def read_config(self):
        """读取配置文件以获取API密钥"""
        home_dir = os.path.expanduser('~')
        file_path = os.path.join(home_dir, '.translator', 'config.txt')

        # 检查目录是否存在，如果不存在则创建
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.api_key = f.read()

    def create_widgets(self):
        self.read_config() # Read API key from config file

        # 设置更大的字体样式
        big_font = ('Arial', 14, 'bold')
        title_font = ('Arial', 16, 'bold')
        
        # Styling
        style = ttk.Style()
        style.configure('.', font=big_font)  # 设置所有部件的默认字体
        style.configure('TLabel', padding=10, font=big_font)
        style.configure('TButton', padding=10, font=big_font)
        style.configure('TEntry', padding=8, font=big_font)
        style.configure('TLabelframe.Label', font=title_font)
        
        # Main frame (现在使用inner_frame而不是root)
        main_frame = ttk.Frame(self.inner_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # API Key Section
        api_frame = ttk.LabelFrame(main_frame, text="API Configuration", padding="15")
        api_frame.pack(fill=tk.X, pady=10)

        # 配置列的权重，使第1列可以伸缩
        api_frame.columnconfigure(1, weight=1)  # 让中间的Entry列占据所有额外空间

        ttk.Label(api_frame, text="DeepSeek API Key:").grid(row=0, column=0, sticky=tk.W)

        # Entry组件设置为sticky="ew"以水平填充
        self.api_entry = ttk.Entry(api_frame, width=60, show="*", font=big_font)
        self.api_entry.insert(0, self.api_key)  # Pre-fill with existing API key
        self.api_entry.grid(row=0, column=1, sticky=tk.EW, padx=10)

        update_btn = ttk.Button(api_frame, text="Update API Key", command=self.update_api_key)
        update_btn.grid(row=0, column=2, padx=10)
        
        # File Selection Section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="15")
        file_frame.pack(fill=tk.X, pady=10)
        
        # Input File
        ttk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W)
        self.input_file_entry = ttk.Entry(file_frame, width=60, font=big_font)
        self.input_file_entry.grid(row=0, column=1, sticky=tk.EW, padx=10)
        ttk.Button(file_frame, text="Browse...", command=self.select_input_file).grid(row=0, column=2, padx=10)
        
        # Output File
        ttk.Label(file_frame, text="Output File:").grid(row=1, column=0, sticky=tk.W)
        self.output_file_entry = ttk.Entry(file_frame, width=60, font=big_font)
        self.output_file_entry.grid(row=1, column=1, sticky=tk.EW, padx=10)
        ttk.Button(file_frame, text="Browse...", command=self.select_output_file).grid(row=1, column=2, padx=10)
        
        # Language Selection
        lang_frame = ttk.LabelFrame(main_frame, text="Translation Settings", padding="15")
        lang_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(lang_frame, text="Target Language:").grid(row=0, column=0, sticky=tk.W)
        self.language_var = tk.StringVar(value="Chinese")
        self.language_menu = ttk.Combobox(lang_frame, textvariable=self.language_var, 
                                        values=["Chinese", "English", "French", "German", "Spanish", "Japanese", "Korean"],
                                        font=big_font)
        self.language_menu.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, pady=20)
        
        # Translate Button (使用更大的按钮)
        translate_btn = ttk.Button(main_frame, text="Translate", command=self.translate_file, style='Big.TButton')
        style.configure('Big.TButton', font=('Arial', 14, 'bold'), padding=15)
        translate_btn.pack(pady=20)
        
        # Status Label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(fill=tk.X, pady=10)
        status_label.configure(font=big_font)
        
        # Configure grid weights
        file_frame.grid_columnconfigure(1, weight=1)

    # 其他方法保持不变...
    def update_api_key(self):
        self.api_key = self.api_entry.get()
        # Save API key to config file
        home_dir = os.path.expanduser('~')
        file_path = os.path.join(home_dir, '.translator', 'config.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(self.api_key)

        if self.api_key:
            messagebox.showinfo("Success", "API Key updated successfully!")
        else:
            messagebox.showwarning("Warning", "API Key cannot be empty!")
    
    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, file_path)
            
            # Auto-generate output filename
            if not self.output_file_entry.get():
                dir_name = os.path.dirname(file_path)
                base_name = os.path.basename(file_path)
                name, ext = os.path.splitext(base_name)
                output_path = os.path.join(dir_name, f"{name}_translated{ext}")
                self.output_file_entry.delete(0, tk.END)
                self.output_file_entry.insert(0, output_path)
    
    def select_output_file(self):
        initial_file = self.output_file_entry.get() or "translated.txt"
        file_path = filedialog.asksaveasfilename(
            title="Select Output File",
            initialfile=initial_file,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, file_path)
    
    def translate_text(self, client, text, target_language="Chinese"):
        """使用DeepSeek API翻译文本"""
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate the following text into {target_language}."},
                    {"role": "user", "content": text},
                ],
                stream=False,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            messagebox.showerror("Translation Error", f"翻译出错: {e}")
            return None
    
    def translate_file(self):
        """翻译文件内容并保存到输出文件"""
        input_file = self.input_file_entry.get()
        output_file = self.output_file_entry.get()
        target_language = self.language_var.get()
        
        # Validate inputs
        if not input_file:
            messagebox.showerror("Error", "Please select an input file!")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please select an output file!")
            return
        
        if not self.api_key:
            messagebox.showerror("Error", "Please enter your DeepSeek API Key!")
            return
        
        # Check if input file exists
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"Input file {input_file} does not exist!")
            return
        
        # Initialize client
        client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        
        # Read file content
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            return
        
        if not content:
            messagebox.showwarning("Warning", "File is empty!")
            return
        
        # Split content into chunks
        chunk_size = 2000  # Adjust based on API limits
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        total_chunks = len(chunks)
        translated_chunks = []
        
        self.status_var.set(f"Translating {total_chunks} chunks...")
        self.progress["maximum"] = total_chunks
        self.progress["value"] = 0
        self.root.update()
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            self.status_var.set(f"Translating chunk {i+1}/{total_chunks}...")
            self.progress["value"] = i + 1
            self.root.update()
            
            translated = self.translate_text(client, chunk, target_language)
            if translated:
                translated_chunks.append(translated)
            else:
                messagebox.showerror("Error", "Translation failed!")
                return
            
            # Avoid rate limiting
            time.sleep(1)
        
        # Combine results
        translated_content = "\n".join(translated_chunks)
        
        # Write output file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            self.status_var.set(f"Translation complete! Saved to {output_file}")
            messagebox.showinfo("Success", "Translation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write output file: {e}")
            self.status_var.set("Error writing output file")

# 运行应用程序
if __name__ == "__main__":
    root = tk.Tk()

    # 在Windows上设置DPI感知，使字体在高分辨率屏幕上更清晰
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = DeepSeekTranslatorApp(root)
    root.mainloop()
