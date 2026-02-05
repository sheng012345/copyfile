#文件内容：
from cx_Freeze import setup, Executable
# 定义要打包的可执行文件，设置base为Win32GUI来隐藏控制台窗口
executables = [Executable("backup_tool.py", base="Win32GUI", icon="zqs.ico")] #不显示cmd窗口
#文件名：wifi8.py，运行时不显示cmd窗口：base="Win32GUI"，设置图标： icon="huayuanyoumei.ico"
setup(
    name="备份指定目录的指定类型文件",
    version="1.0",
    description="备份指定目录的指定类型文件",
    executables=executables
)