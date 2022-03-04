from pathlib import Path
import shutil
import os
import json
import sys

#生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

config = None
with open(resource_path("config/config.json")) as reader:
    config = json.load(reader)

filetypes = config['filetypes']

def move_safe(src, dst):
    """_summary_
    如果移动出错则记录错误消息，不退出程序
    Args:
        src (_type_): _description_
        dst (_type_): _description_

    Returns:
        _type_: _description_
    """
    msg = ""
    try:
        shutil.move(src,dst)
    except Exception as e:
        msg = f"{src} -> {dst} error: {e}"
        print(msg)
    return msg



def organize(dir):
    error_msg = []
    PATH = Path(dir)
    files = []
    # A list to store all the files in the PATH
    # All the files will go to the organized folder
    dest = PATH / "自动分类的目录"
    # Make the folder only if it does not exists
    dest.mkdir(exist_ok=True)
    # iterate every file and directory and store only the files in the 'files' list
    for i in PATH.iterdir():
        if i.is_file():
            files.append(i)

    # traverse on every file check the file type and move it to the corresponding folder
    for file in files:
        # done flag tells that the file belong to a dictionary value
        done = 0
        # iterate over the keys and check if the file belong to the particular key
        for k in filetypes.keys():
            # Check if the file extention is in the values of the key
            if file.suffix[1:] in filetypes[k]:
                done = 1
                # make a new folder with `key name` and move the file there
                destf = dest / f"{k}"
                destf.mkdir(exist_ok=True)
                src = f"{file.resolve()}"
                dst = f"{destf}" 
                _msg = move_safe(src,dst)
                if _msg:
                    error_msg.append(_msg)

        if done != 1:
            # if the file was not present in the dictionary the make Others folder  and move the file there
            destf = dest / "Others"
            destf.mkdir(exist_ok=True)
            _msg = move_safe(str(file.resolve()), str(destf))
            if _msg:
                error_msg.append(_msg)
    return dest, error_msg


def restore(dir):
    """_summary_
    将目标路径中的所有文件提取到当前目录，并删除目标路径
    eg: /dir1/dir2/files...
    result /dir1/files...
    Args:
        dir (_type_): 待处理的路径
    """
    err_msgs = []
    p = Path(dir)
    if not p.exists():
        return
    parent_path = p.parent
    done = True
    for root,_,files in os.walk(p):
        for f in files:
            src = f"{root}/{f}"
            dst = f"{parent_path}/{f}"
            _msg = move_safe(src,dst)
            if _msg:
                err_msgs.append(_msg)
    if done:
        print(f"为了确保安全，你可以手动删除 {dir}")
    return err_msgs

if __name__ == '__main__':
    organize("/Users/aaron/Downloads")