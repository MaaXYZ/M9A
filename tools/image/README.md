# Image Tools For M9A

本文件夹内工具用于对来自 [重返未来1999中文维基](https://res1999.huijiwiki.com/) 的物品列表图片进行一系列处理以支持 M9A 识别掉落物品后上报功能。  
相关图片版权由深蓝互动所有。

<!-- markdownlint-disable MD024 -->

## 1. 图片缩放脚本（resize.py）

### 基本用法

```bash
python resize.py 输入图片/文件夹 输出图片/文件夹 [--width 宽度] [--height 高度]
```

### 参数说明

- 输入图片/文件夹: 要处理的单张图片或包含多张图片的文件夹
- 输出图片/文件夹: 处理后的图片保存位置
- --width: 目标宽度（默认值：120）
- --height: 目标高度（默认值：120）

### 使用示例

```bash
# 将单张图片缩放为120x120像素（默认大小）
python resize.py input.jpg output.jpg

# 将单张图片缩放为自定义大小
python resize.py input.jpg output.jpg --width 150 --height 150

# 批量处理文件夹中的所有图片（缩放为120x120）
python resize.py 输入文件夹/ 输出文件夹/

# 批量处理文件夹中的图片并指定尺寸
python resize.py 输入文件夹/ 输出文件夹/ --width 200 --height 200
```

## 2. 图片裁剪脚本（crop.py）

### 基本用法

```bash
python crop.py 输入图片/文件夹 输出图片/文件夹 [裁剪选项]
```

### 裁剪选项（必选）

- --box LEFT TOP WIDTH HEIGHT: 指定裁剪区域的左上角坐标及宽高
- --center --size WIDTH HEIGHT: 从图片中心裁剪指定大小
- --percent LEFT TOP RIGHT BOTTOM: 从各边缘按百分比裁剪

### 使用示例

```bash
# 裁剪指定区域（从坐标100,100开始，宽300高300）
python crop.py input.jpg output.jpg --box 100 100 300 300

# 从中心裁剪
python crop.py input.jpg output.jpg --center --size 300 300

# 按百分比裁剪（从各边缘裁剪10%）
python crop.py input.jpg output.jpg --percent 10 10 10 10

# 批量处理文件夹中的图片
python crop.py 输入文件夹/ 输出文件夹/ --box 100 100 400 300
```

## 3. 图片透明转绿色脚本（transparency2green.py）

### 基本用法

```bash
python transparency2green.py 输入图片/文件夹 输出图片/文件夹 [选项]
```

### 可选参数

- --color R,G,B: 指定替换透明区域的颜色（默认为纯绿色：0,255,0）
- --threshold 阈值: 透明度阈值，小于此值的像素将被替换（默认：128）
- --force-png: 强制输出为PNG格式以保持质量

### 使用示例

```bash
# 基本用法（将单个图片的透明部分替换为绿色）
python transparency2green.py input.png output.png

# 指定自定义绿色（较浅的绿色）
python transparency2green.py input.png output.png --color 50,200,50

# 调整透明度阈值（值越高，会有更多半透明像素被替换）
python transparency2green.py input.png output.png --threshold 200

# 处理整个文件夹中的图片
python transparency2green.py 输入文件夹/ 输出文件夹/

# 强制所有输出为PNG格式（推荐用于保持质量）
python transparency2green.py 输入文件夹/ 输出文件夹/ --force-png
```
