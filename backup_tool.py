import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import configparser

class BackupTool:
    def __init__(self, root):
        self.root = root
        self.root.title("文件备份工具")
        self.root.geometry("600x350")
        self.root.resizable(True, True)
        
        # 配置文件路径 - 存储在软件所在目录，确保打包后也能正常工作
        import os.path
        import sys
        if getattr(sys, 'frozen', False):
            # 打包后的环境 - 配置文件存储在exe文件同目录
            self.config_file = os.path.join(os.path.dirname(sys.executable), "backup_config.ini")
        else:
            # 开发环境
            self.config_file = os.path.join(os.path.dirname(__file__), "backup_config.ini")
        
        # 加载配置
        self.config = configparser.ConfigParser()
        self.load_config()
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        #self.title_label = tk.Label(self.main_frame, text="文件备份工具", font=("Arial", 16, "bold"))
        #self.title_label.pack(pady=10)
        
        # 源目录选择
        self.source_frame = tk.Frame(self.main_frame)
        self.source_frame.pack(fill=tk.X, pady=10)
        
        self.source_label = tk.Label(self.source_frame, text="备份源目录:", width=15)
        self.source_label.pack(side=tk.LEFT, padx=5)
        
        self.source_var = tk.StringVar(value=self.source_dir)
        self.source_entry = tk.Entry(self.source_frame, textvariable=self.source_var, width=40)
        self.source_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.source_button = tk.Button(self.source_frame, text="浏览", command=self.select_source_directory)
        self.source_button.pack(side=tk.RIGHT, padx=5)
        
        self.open_source_button = tk.Button(self.source_frame, text="打开", command=self.open_source_directory)
        self.open_source_button.pack(side=tk.RIGHT, padx=5)
        
        # 目标目录选择
        self.target_frame = tk.Frame(self.main_frame)
        self.target_frame.pack(fill=tk.X, pady=10)
        
        self.target_label = tk.Label(self.target_frame, text="备份目标目录:", width=15)
        self.target_label.pack(side=tk.LEFT, padx=5)
        
        self.target_var = tk.StringVar(value=self.target_dir)
        self.target_entry = tk.Entry(self.target_frame, textvariable=self.target_var, width=40)
        self.target_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.target_button = tk.Button(self.target_frame, text="浏览", command=self.select_target_directory)
        self.target_button.pack(side=tk.RIGHT, padx=5)
        
        self.open_target_button = tk.Button(self.target_frame, text="打开", command=self.open_target_directory)
        self.open_target_button.pack(side=tk.RIGHT, padx=5)
        
        # 文件后缀选择
        self.extension_frame = tk.Frame(self.main_frame)
        self.extension_frame.pack(fill=tk.X, pady=10)
        
        self.extension_label = tk.Label(self.extension_frame, text="文件后缀:", width=15)
        self.extension_label.pack(side=tk.LEFT, padx=5)
        
        self.extension_var = tk.StringVar(value=self.extensions)
        self.extension_entry = tk.Entry(self.extension_frame, textvariable=self.extension_var, width=40)
        self.extension_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 按钮框架
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=20, fill=tk.X)
        
        # 左侧占位
        self.left_space = tk.Frame(self.button_frame)
        self.left_space.pack(side=tk.LEFT, expand=True)
        
        # 备份按钮
        self.backup_button = tk.Button(self.button_frame, text="开始备份", command=self.start_backup, font=("微软雅黑", 12))
        # 绑定鼠标按下事件，当鼠标按下时立即更新状态栏文本
        self.backup_button.bind("<Button-1>", self.on_backup_button_press)
        self.backup_button.pack(side=tk.LEFT, padx=10)
        
        # 中间占位
        self.middle_space = tk.Frame(self.button_frame)
        self.middle_space.pack(side=tk.LEFT, expand=True)
        
        # 打开软件目录按钮
        self.open_software_dir_button = tk.Button(self.button_frame, text="打开软件目录", command=self.open_software_directory, font=("微软雅黑", 10))
        self.open_software_dir_button.pack(side=tk.RIGHT, padx=10)
        
        # 状态显示
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_label = tk.Label(self.main_frame, textvariable=self.status_var, fg="green")
        self.status_label.pack(pady=5)

        #----------------------------------------------------------------
        # 功能说明
        # 创建功能说明框架
        # 参数说明：
        # self.main_frame: 父容器，主框架
        # relief=tk.GROOVE: 边框样式，设置为凹槽样式
        # bd=1: 边框宽度，设置为1像素
        # pady=10: 内边距（垂直方向），设置为10像素
        # padx=10: 内边距（水平方向），设置为10像素
        self.info_frame = tk.Frame(self.main_frame, relief=tk.GROOVE, bd=1, pady=2, padx=2)
        
        # 放置功能说明框架到主框架中
        # 参数说明：
        # fill=tk.BOTH: 填充方式，水平和垂直方向都填充
        # expand=True: 扩展选项，允许框架扩展以填充可用空间
        # pady=3: 外边距（垂直方向），设置为3像素
        self.info_frame.pack(fill=tk.BOTH, expand=True, pady=3)
        
        #----------------------------------------------------------------
        # 使用Text组件替代Label组件，更好地支持多行文本显示
        # 创建Text组件作为功能说明标题
        # 参数说明：
        # self.info_frame: 父容器，功能说明框架
        # height=10: 文本框高度，设置为10行
        # wrap=tk.WORD: 文本换行方式，按单词换行
        # font=("微软雅黑", 10, "bold"): 字体设置，微软雅黑字体，10号大小，粗体
        # borderwidth=0: 边框宽度，设置为0，使文本框看起来像标签
        # bg=self.info_frame.cget("bg"): 背景颜色，与父容器背景颜色一致，
        self.info_title = tk.Text(self.info_frame, height=15, wrap=tk.WORD, font=("宋体", 10), borderwidth=0, bg=self.info_frame.cget("bg"))
        
        # 向Text组件中插入说明文本
        # 参数说明：
        # tk.END: 插入位置，在文本末尾插入
        # "功能说明\n备份指定目录下面的指定后缀的文件到指定目录下面，不包含子目录。\n文件名后缀：.txt,.docx,.pdf": 要插入的文本内容
        self.info_title.insert(tk.END, "功能说明：备份指定目录下面的指定后缀的文件到指定目录下面，不包含子目录。\n文件名后缀样式：.txt,.docx,.pdf")
        
        # 配置Text组件状态为禁用，使其不可编辑
        # 参数说明：
        # state=tk.DISABLED: 组件状态，禁用状态
        self.info_title.config(state=tk.DISABLED)
        
        # 放置Text组件到父容器中
        # 参数说明：
        # anchor=tk.W: 锚点，左对齐
        # fill=tk.X: 填充方式，水平方向填充
        # pady=5: 上下边距，设置为5像素
        self.info_title.pack(anchor=tk.W, fill=tk.X, pady=1)
        #----------------------------------------------------------------

        self.info_text = tk.Text(self.info_frame, height=6, wrap=tk.WORD, font=("Arial", 9))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        info_content = "备份指定目录下面的指定后缀的文件到指定目录下面，不包含子目录。\n"
        info_content += "文件名后缀：.txt,.docx,.pdf\n\n"
        info_content += "1. 选择要备份的源目录\n"
        info_content += "2. 选择备份文件的目标目录\n"
        info_content += "3. 输入要备份的文件后缀（多个后缀用逗号分隔）\n"
        info_content += "4. 点击'开始备份'按钮执行备份操作\n"
        info_content += "5. 备份后的文件会在文件名后添加日期和时间戳"
        
        self.info_text.insert(tk.END, info_content)
        self.info_text.config(state=tk.DISABLED)
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            if "Settings" in self.config:
                self.source_dir = self.config["Settings"].get("source_dir", "")
                self.target_dir = self.config["Settings"].get("target_dir", "")
                self.extensions = self.config["Settings"].get("extensions", ".txt,.docx,.pdf")
            else:
                self.source_dir = ""
                self.target_dir = ""
                self.extensions = ".txt,.docx,.pdf"
        else:
            self.source_dir = ""
            self.target_dir = ""
            self.extensions = ".txt,.docx,.pdf"
    
    def save_config(self):
        """保存配置文件"""
        self.config["Settings"] = {
            "source_dir": self.source_var.get(),
            "target_dir": self.target_var.get(),
            "extensions": self.extension_var.get()
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.config.write(f)
    
    def select_source_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_var.set(directory)
    
    def select_target_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.target_var.set(directory)
    
    def open_source_directory(self):
        """打开源目录"""
        source_dir = self.source_var.get()
        if source_dir and os.path.exists(source_dir):
            os.startfile(source_dir)
        else:
            messagebox.showinfo("提示", "请先选择有效的源目录")
    
    def open_target_directory(self):
        """打开目标目录"""
        target_dir = self.target_var.get()
        if target_dir and os.path.exists(target_dir):
            os.startfile(target_dir)
        else:
            messagebox.showinfo("提示", "请先选择有效的目标目录")
    
    def on_backup_button_press(self, event):
        """鼠标按下备份按钮时的处理"""
        # 当鼠标按下时立即更新状态栏文本为"开始备份"
        self.status_var.set("开始备份")
        self.root.update()
    
    def open_software_directory(self):
        """打开软件所在目录"""
        import sys
        if getattr(sys, 'frozen', False):
            # 打包后的环境
            software_dir = os.path.dirname(sys.executable)
        else:
            # 开发环境
            software_dir = os.path.dirname(__file__)
        
        if software_dir and os.path.exists(software_dir):
            os.startfile(software_dir)
        else:
            messagebox.showinfo("提示", "无法打开软件目录")
    
    def start_backup(self):
        source_dir = self.source_var.get()
        target_dir = self.target_var.get()
        extensions = self.extension_var.get()
        
        # 处理输入的目录路径，去除空格和引号
        source_dir = source_dir.strip().strip('"').strip("'")
        target_dir = target_dir.strip().strip('"').strip("'")
        
        # 验证输入
        if not source_dir:
            messagebox.showerror("错误", "请选择备份源目录")
            return
        
        if not target_dir:
            messagebox.showerror("错误", "请选择备份目标目录")
            return
        
        if not extensions:
            messagebox.showerror("错误", "请输入文件后缀")
            return
        
        # 处理文件后缀
        extension_list = [ext.strip() for ext in extensions.split(",")]
        
        # 检查目录是否存在
        if not os.path.exists(source_dir):
            messagebox.showerror("错误", "备份源目录不存在")
            return
        
        if not os.path.exists(target_dir):
            messagebox.showerror("错误", "备份目标目录不存在")
            return
        
        try:
            
            # 获取当前日期时间
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 备份文件
            backup_count = 0
            for filename in os.listdir(source_dir):
                # 只处理文件，不处理子目录
                if os.path.isfile(os.path.join(source_dir, filename)):
                    # 检查文件后缀
                    for ext in extension_list:
                        if filename.endswith(ext):
                            # 构建新文件名
                            name, ext = os.path.splitext(filename)
                            new_filename = f"{timestamp}_{name}{ext}"
                            
                            # 复制文件
                            source_path = os.path.join(source_dir, filename)
                            target_path = os.path.join(target_dir, new_filename)
                            shutil.copy2(source_path, target_path)
                            backup_count += 1
                            break
            
            # 保存配置
            self.save_config()
            
            self.status_var.set(f"备份完成，共备份 {backup_count} 个文件")
            
        except Exception as e:
            self.status_var.set("备份失败")
            messagebox.showerror("错误", f"备份过程中发生错误: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupTool(root)
    root.mainloop()