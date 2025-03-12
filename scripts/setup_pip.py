# -*- coding: utf-8 -*-
"""
安装pip和依赖库的脚本

该脚本用于嵌入式Python环境中，执行以下操作:
1. 下载并安装pip
2. 从requirements.txt中读取并安装依赖库
"""

import os
import sys
import urllib.request
import subprocess


def install_pip():
    """下载并安装pip"""
    print("正在设置pip...")

    # 下载get-pip.py
    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_path = os.path.join(os.path.dirname(__file__), "get-pip.py")

    print(f"正在下载 {get_pip_url}...")
    urllib.request.urlretrieve(get_pip_url, get_pip_path)

    # 安装pip
    print("正在安装pip...")
    subprocess.check_call([sys.executable, get_pip_path, "--no-warn-script-location"])

    # 删除get-pip.py
    os.unlink(get_pip_path)

    print("pip已成功安装!")


def install_requirements():
    """从requirements.txt安装依赖库"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

    if not os.path.exists(requirements_path):
        print(f"警告: {requirements_path} 不存在，无法安装依赖库")
        return

    print(f"正在从 {requirements_path} 安装依赖库...")
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                requirements_path,
                "--no-warn-script-location",
            ]
        )
        print("所有依赖库安装完成!")
    except subprocess.CalledProcessError as e:
        print(f"警告: 安装依赖库时出错: {e}")
        print("某些库可能需要手动安装")


def main():
    """主函数"""
    # 安装pip
    install_pip()

    # 安装依赖库
    install_requirements()


if __name__ == "__main__":
    main()
