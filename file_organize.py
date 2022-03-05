from pathlib import Path
import shutil
import os
import json
import sys
import fire
# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, "frozen", False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


config = {
    "filetypes": {
        "图片": [
            "png", "jpg", "jfif", "webp", "jpeg", "bmp", "tiff", "gif", "raw", "psd",
        ],
        "文档": ["doc", "docx", "ppt", "pptx", "csv", "xls", "xlsx", "pdf", "txt"],
        "视频": ["mp4", "mpeg", "mkv", "srt"],
        "代码": ["html", "css", "js", "py", "cpp", "c", "go", "java"],
        "音频": ["mp3", "wav", "ogg"],
        "压缩包": ["zip", "tar", "rar", "7z"],
    }
}

config_file_path = Path().home() / ".folder_organize"
config_file_path.mkdir(exist_ok=True)
config_file = config_file_path / "config.json"

if not config_file.exists():
    with open(config_file,"w",encoding="utf-8") as writer:
        json.dump(config, writer, ensure_ascii=False,indent=4)

def get_config():
    if config_file.exists():
        with open(config_file.as_posix(),"r",encoding="utf-8") as reader:
            config = json.load(reader)
    return config["filetypes"]

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
        shutil.move(src, dst)
    except Exception as e:
        msg = f"{src} -> {dst} error: {e}"
        print(msg)
    return msg


def organize(dir :Path):
    filetypes = get_config()
    error_msg = []
    files = []
    # A list to store all the files in the PATH
    # All the files will go to the organized folder
    dest = dir / "Organized"
    # Make the folder only if it does not exists
    dest.mkdir(exist_ok=True)
    # iterate every file and directory and store only the files in the 'files' list
    for i in dir.iterdir():
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
                _msg = move_safe(str(file.resolve()), str(destf))
                if _msg:
                    error_msg.append(_msg)

        if done != 1:
            # if the file was not present in the dictionary the make Others folder  and move the file there
            destf = dest / "其他"
            destf.mkdir(exist_ok=True)
            _msg = move_safe(str(file.resolve()), str(destf))
            if _msg:
                error_msg.append(_msg)
    return dest, error_msg


def restore(dir: Path) -> list:
    """_summary_
    将目标路径中的所有文件提取到当前目录，并删除目标路径
    eg: /dir1/dir2/files...
    result /dir1/files...
    Args:
        dir (_type_): 待处理的路径
    """
    err_msgs = []
    if not dir.exists():
        return []
    parent_path = dir.parent
    for item in dir.rglob("*"):
        if item.is_file():
            _msg = move_safe(item.as_posix(), (parent_path / item.name).as_posix())
            if _msg:
                err_msgs.append(_msg)
    return err_msgs

class Command(object):
    def organize(self,dir: str):
        organize(Path(dir))
    def collect(self,dir: str):
        restore(Path(dir))

if __name__ == "__main__":
    fire.Fire(Command)