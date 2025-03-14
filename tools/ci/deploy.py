import os
import json
import shutil

# 这些需要自己设置
title = "MFW-PyQt6"  # 标题栏
resource_name = "M9A"  # 你的資源名称
url = "https://github.com/MaaXYZ/M9A"  # 你的項目地址

# 这些不需要修改

config_name = "default"
resource_path = os.path.join(".")
config_path = os.path.join(".", "config", "maa_pi_config.json")
print(f"title: {title}")
print(f"resource_name: {resource_name}")
print(f"url: {url}")

config_data = {
    "MainWindow": {"Title": title},
    "program": {"resource_exist": True},
    "Maa": {
        "maa_config_list": {
            resource_name: {
                config_name: config_path,
            }
        },
        "Maa_config_name": config_name,
        "Maa_config_path": config_path,
        "maa_resource_list": {resource_name: resource_path},
        "Maa_resource_name": resource_name,
        "Maa_resource_path": resource_path,
    },
}


mfw_config_path = os.path.join(".", "install", "config", "config.json")
print(f"mfw_config_path: {mfw_config_path}")
os.makedirs(os.path.dirname(mfw_config_path), exist_ok=True)
with open(mfw_config_path, "w", encoding="utf-8") as f:
    json.dump(config_data, f, ensure_ascii=False, indent=4)


# 移动資源文件到 bundles 目录
source_path = os.path.join(".", "assets")
destination_path = os.path.join(".", "install")
print(f"Copying from {source_path} to {destination_path}")
shutil.copytree(
    source_path,
    destination_path,
    dirs_exist_ok=True,
    ignore=shutil.ignore_patterns("MaaCommonAssets"),
)

pi_config = {
    "adb": {
        "adb_path": "",
        "address": "",
        "input_method": 0,
        "screen_method": 0,
        "config": {},
    },
    "win32": {
        "hwnd": 0,
        "input_method": 0,
        "screen_method": 0,
    },
    "controller": {"name": ""},
    "gpu": -1,
    "resource": "",
    "task": [],
    "finish_option": 0,
    "finish_option_res": 0,
    "finish_option_cfg": 0,
    "run_before_start": "",
    "run_after_finish": "",
    "emu_path": "",
    "emu_wait_time": 10,
    "exe_path": "",
    "exe_wait_time": 10,
    "exe_parameter": "",
}
install_config_path = os.path.join(".", "install", "config", "maa_pi_config.json")
os.makedirs(os.path.dirname(install_config_path), exist_ok=True)

print(f"Creating config file at {install_config_path}")
with open(install_config_path, "w", encoding="utf-8") as f:
    json.dump(pi_config, f, ensure_ascii=False, indent=4)

# interface 部分
new_data = {"url": url, "name": resource_name}
interface_json_path = os.path.join(".", "install", "interface.json")
# 打印 interface_json_path 以调试
print(f"interface_json_path: {interface_json_path}")

with open(interface_json_path, "r", encoding="utf-8") as f:
    interface_data = json.load(f)

interface_data.update(new_data)

with open(interface_json_path, "w", encoding="utf-8") as f:
    json.dump(interface_data, f, ensure_ascii=False, indent=4)
