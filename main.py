from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel
from pathlib import Path
import time
from file_organize import restore, organize,config_file
import subprocess
import platform
import os

window = Tk()
window.title("文件分类器-V1.0 by somenzz")
PATH = StringVar()


def selectPath():
    path_ = askdirectory()
    print(path_)
    PATH.set(path_)


def organize_click():
    dir = Path(PATH.get())
    if str(dir).strip() == "" or str(dir).strip() == ".":
        return
    if not dir.exists():
        showinfo(f"{dir} 路径不存在！")
        return
    if len(list(dir.parents)) < 3:
        #比较危险，提示
        confirm = askokcancel(title="提醒", message=f"确认将{dir}中的文件分类吗？")
        if not confirm:
            return

    showinfo(f"开始分类存放")
    dest, error_msgs = organize(dir)
    PATH.set(dest)
    err_msgs = "\n".join(error_msgs)
    showinfo(f"已分类存放至 {dest}")
    if err_msgs:
        showinfo(err_msgs)

def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = "%dx%d+%d+%d" % (
        width,
        height,
        (screenwidth - width) / 2,
        (screenheight - height) / 2,
    )
    root.geometry(size)
    root.update()


def restore_click():
    dir = Path(PATH.get())
    if str(dir).strip() == "" or str(dir).strip() == ".":
        return
    if not dir.exists():
        showinfo(f"{dir} 路径不存在！")
        return
    confirm = askokcancel(title="提醒", message=f"确认将{dir}中的所有文件移动到{dir.parent}吗")
    if not confirm:
        return

    showinfo("开始文件归集")
    error_msgs = restore(dir)
    err_msgs = "\n".join(error_msgs)
    showinfo(f"已归集至 {dir.parent}")
    PATH.set(dir.parent.as_posix())
    if err_msgs:
        showinfo(err_msgs)


def editconfig():
    if platform.system() == "Darwin":
        subprocess.call(["open","-e", config_file.as_posix()])
    elif platform.system() == "Windows":
        os.startfile(config_file.as_posix())
    else:## Linux
        subprocess.call(["xdg-open", config_file.as_posix()])

Button(window, padx=20, text="配置文件", command=editconfig).grid(row=0, column=0)
Label(window, text="目标路径:").grid(row=1, column=0)
Entry(window, textvariable= PATH, width=35).grid(row=1, column=1)
Button(window, text="路径选择", command=selectPath).grid(row=1, column=2)
Button(window, padx=20, text="分类存放", command=organize_click).grid(row=2, column=0)
Button(window, padx=20, text="文件归集", command=restore_click).grid(row=2, column=1)
Label(window, text="操作记录：", anchor=NW, padx=8, pady=10).grid(row=3, column=0)



def clear():
    status.delete(0.0, END)  # 清楚text中的内容，0.0为删除全部


Button(window, padx=20, text="清空", command=clear).grid(row=3, column=1)
status = Text(window, width=60, height=10, padx=8)
status.grid(row=4, column=0, columnspan=3)


scroll = Scrollbar()
scroll.grid(row=4, column=2, sticky=S + N)
# 两个控件关联
scroll.config(command=status.yview)
status.config(yscrollcommand=scroll.set)


def showinfo(result):
    realtime = time.strftime("%Y-%m-%d %H:%M:%S")
    status.insert(END, f"{realtime} {result}\n")  # 显示在text框里面


center_window(window, 518, 300)
window.mainloop()
