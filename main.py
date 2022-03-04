from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel
from pathlib import Path
import time
from file_organize import restore, organize

window = Tk()
window.title("文件分类器-V1.0")
path = StringVar()

def selectPath():
    path_ = askdirectory()
    print(path_)
    path.set(path_)


def organize_click():
    dir = path.get()
    if dir.strip() == "" or dir.strip() == ".":
        return
    if not Path(dir).exists():
        showinfo(f"{dir} 路径不存在！")
        return
    showinfo(f"正在整理 {dir}")
    dest, error_msgs = organize(dir)
    path.set(dest)
    err_msgs = "\n".join(error_msgs)
    showinfo(f"已完成，路径是：{dest}。\n{err_msgs}")


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
    p = Path(path.get())
    if not p.exists():
        # showinfo(text= f"{p} 路径不存在！")
        showinfo(f"{p} 路径不存在！")
        return

    if p.as_posix().strip() == "" or p.as_posix().strip() == ".":
        return

    confirm = askokcancel(title="提醒", message=f"确认将{p}中的所有文件移动到{p.parent}吗")
    if not confirm:
        return
    if not p.exists():
        showinfo(f"{p} 路径不存在！")
        return
    error_msgs = restore(p.as_posix())
    err_msgs = "\n".join(error_msgs)
    showinfo(f"已恢复\n{err_msgs}")


Label(window, text="目标路径:", pady=10).grid(row=0, column=0)
Entry(window, textvariable=path, width=40).grid(row=0, column=1)
Button(window, text="路径选择", command=selectPath).grid(row=0, column=2)
Button(window, padx=20, text="整理", command=organize_click).grid(row=1, column=0)
Button(window, padx=20, text="恢复", command=restore_click).grid(row=1, column=1)
Button(window, padx=20, text="关闭", command=window.quit).grid(row=1, column=2)
Label(window, text="状态：", anchor=NW, padx=8, pady=10).grid(row=2, column=0)


def clear():
    status.delete(0.0, END)  # 清楚text中的内容，0.0为删除全部


Button(window, padx=20, text="清空", command=clear).grid(row=2, column=1)
status = Text(window, width=60, height=10, padx=8)
status.grid(row=3, column=0, columnspan=3)

# N
scroll = Scrollbar()
scroll.grid(row=3, column=2, sticky=S + N)
# 两个控件关联
scroll.config(command=status.yview)
status.config(yscrollcommand=scroll.set)


def showinfo(result):
    realtime = time.strftime("%Y-%m-%d %H:%M:%S ")
    status.insert(INSERT, f"{realtime} - {result}\n")  # 显示在text框里面


center_window(window, 530, 300)
window.mainloop()
