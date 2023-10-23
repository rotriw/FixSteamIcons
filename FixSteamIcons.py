#-*- coding:utf-8 -*-
import httpx,os,configparser,threading


def DownloadIconData(url):
    return httpx.get(
        url
    ).content


def FixIcon(url_file,steam_path):
    #IDList是一个空值,需要允许空值的出现
    ini=configparser.ConfigParser(allow_no_value=True)
    with open(url_file,"r") as fp:
        ini.read_file(fp)

    #游戏id和图标文件名
    id=os.path.split(ini.get("InternetShortcut","URL"))[1]
    icon=os.path.split(ini.get("InternetShortcut","IconFile"))[1]

    #下载图标,这里可以偷个懒不用去https://steamdb.info/app/{id}解析出clienticon项
    data=DownloadIconData(f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{id}/{icon}")
    icon=os.path.join(steam_path,icon)
    with open(icon,"wb") as fp:
        fp.write(data)

    #把图标路径重定向到新的steam目录
    ini.set("InternetShortcut","IconFile",icon)
    #保留原本的等号两边没有空格
    with open(url_file,"w") as fp:
        ini.write(fp,space_around_delimiters=False)


if __name__=="__main__":
    print("此脚本帮助你修复重装steam后steam创建的游戏桌面快捷方式图标消失问题")
    print("方法来源https://www.bilibili.com/read/cv26845826")
    print("请先将需要恢复图标的快捷方式单独放到一个文件夹,建议复制而不是移动")

    print("\n")
    print("(示例: C:\\Users\\Administrator\\Desktop\\需要恢复图标的快捷方式们)")
    fix_path=input("请输入需要恢复图标的文件夹路径: ")

    print("\n")
    print("(示例: C:\\Program Files (x86)\\Steam\\)")
    steam_path=input("请输入steam的安装文件夹路径(绝对路径):")
    steam_path=os.path.join(steam_path,"steam\\games")

    for url_file in os.listdir(fix_path):
        threading.Thread(
            target=FixIcon,
            args=(os.path.join(fix_path,url_file),steam_path)
        ).start()

    print("\n")
    print("请稍等")