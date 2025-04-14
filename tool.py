# -*- coding: utf-8 -*-

import tkinter
from tkinter import filedialog, IntVar
from PIL import Image, ImageTk
import os
import json


def resize_img(w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片
    w, h = pil_image.size  # 获取图像的原始大小
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


def close_window():
    global root
    root.destroy()


def show_image_value(image_name):
    # 更新图片
    img_open = Image.open(image_name)
    global windowWidth, windowHeight
    img_open = resize_img(windowWidth, windowHeight, img_open)
    render = ImageTk.PhotoImage(img_open)
    global label_img
    label_img.image = render
    label_img.configure(image=render)

    # 更新按钮
    read_json()


def open_dir():
    selectDir = filedialog.askdirectory()  # 选择目录
    # print(selectDir)
    global image_root, image_lists, image_num
    image_root = selectDir
    image_lists = sorted(os.listdir(image_root))
    # 删除json，其他非图片的文件
    for name in image_lists:
        if name.split(".")[-1] not in ["jpg", "png", "jpeg", "gif", "bmp", "JPG", "PNG", "JPEG", "GIF", "BMP"]:
            image_lists.remove(name)

    # 显示
    if (len(image_lists) > 0):
        image_num = 0
        show_image_value(os.path.join(image_root, image_lists[image_num]))


def pre_image():
    # 显示
    global image_num, image_lists
    image_num = image_num - 1
    image_num = max(0, image_num)
    if (len(image_lists) > 0 and image_num >= 0 and image_num < len(image_lists)):
        show_image_value(os.path.join(image_root, image_lists[image_num]))


def write_json():
    global image_num, image_lists, image_root, var_dict, type_lists, global_dict
    out_json = {"image_name": image_lists[image_num]}
    for key, checkVar in var_dict.items():
        # print(key,checkVar ,type(checkVar)==int)
        out_json[key] = checkVar.get()
    print(out_json)
    global_dict[image_lists[image_num]] = out_json
    with open(os.path.join(image_root, image_lists[image_num][:-len(image_lists[image_num].split(".")[-1])] + "json"),
              "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False)

    # with open(image_root + "/results.json", "a+", encoding="utf-8") as f:
    #     json.dump(out_json, f, ensure_ascii=False)
    #     f.write('\r\n')


def read_json():
    global image_num, image_lists, image_root, var_dict, type_lists, checkbotton_dict
    full_name = os.path.join(image_root, image_lists[image_num][:-len(image_lists[image_num].split(".")[-1])] + "json")
    if os.path.exists(full_name):
        with open(full_name, "r", encoding="utf-8") as load_f:
            load_dict = json.load(load_f)
        for key, value in var_dict.items():
            # print("****",key,value,type(var_dict[key]))
            var_dict[key].set(load_dict[key])
            if var_dict[key].get() == 1:
                checkbotton_dict[key].select()
            else:
                checkbotton_dict[key].deselect()


    else:
        for key, value in var_dict.items():
            var_dict[key].set(0)
            checkbotton_dict[key].deselect()


def next_image():
    # 保存json
    global image_num, image_lists, image_root, root
    write_json()
    # 显示
    global image_num, image_lists, image_root

    image_num = image_num + 1
    image_num = min(len(image_lists) - 1, image_num)
    if (len(image_lists) > 0 and image_num >= 0 and image_num < len(image_lists)):
        show_image_value(os.path.join(image_root, image_lists[image_num]))


def save_images():
    result_file = open(image_root + '/results.json', 'a+', encoding='utf-8')
    f_list = os.listdir(image_root)
    # print f_list
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.json' and i != 'results.json':
            with open(image_root + '/' + i, "r", encoding="utf-8") as load_f:
                result_file.write(load_f.read() + '\r\n')
            os.remove(image_root + '/' + i)
    result_file.close()
    root.quit()


image_lists = []
image_root = []
image_num = -1
global_dict = {}

root = tkinter.Tk()
root.attributes("-topmost", False)
root.title('图像多标签分类工具      作者：whoosy')  # 窗口标题
root.resizable(True, True)  # 固定窗口大小

windowWidth = 1000  # 获得当前窗口宽
windowHeight = 500  # 获得当前窗口高
screenWidth, screenHeight = root.maxsize()  # 获得屏幕宽和高
geometryParam = '%dx%d+%d+%d' % (
    windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
root.geometry(geometryParam)  # 设置窗口大小及偏移坐标
root.wm_attributes('-topmost', 1)  # 窗口置顶

# 1创建主菜单
bigmenu = tkinter.Menu(root)
file_menu = tkinter.Menu(bigmenu)  # 创建空菜单
file_menu.add_command(label="打开目录", command=open_dir)
file_menu.add_command(label="退出", command=close_window)
bigmenu.add_cascade(label="文件", menu=file_menu)  # 将file_menu菜单添加到菜单栏

# 4将主餐单加入窗口
root.config(menu=bigmenu)

# 创建组件          垂直摆放:vertical   水平摆放：horizontal
panedwindow = tkinter.PanedWindow(root, orient='horizontal')
# 添加组件
label_img = tkinter.Label(panedwindow, width=70, height=50, compound='center', text=" ")
label_img.pack()

# 创建组件
labelframe = tkinter.LabelFrame(panedwindow, text='标签选择（支持多选）')
labelframe.pack()

# with open("labels.ini", "r", encoding="utf-8") as f:
#     lines = f.readlines()

# 读取labels.ini文件内容，并将每个标签与对应的数字键关联起来
label_mapping = {}
with open("labels.ini", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for index, line in enumerate(lines, start=1):
        label_mapping[str(index)] = line.strip()

# 创建一个函数，用于切换对应标签的选中状态
def toggle_label_selection(event):
    key_pressed = event.char  # 获取按键字符
    if key_pressed in label_mapping:
        label_name = label_mapping[key_pressed]
        # 切换对应标签的选中状态
        checkbotton_dict[label_name].toggle()

# 绑定数字键1, 2, 3到toggle_label_selection函数
root.bind('1', toggle_label_selection)
root.bind('2', toggle_label_selection)
root.bind('3', toggle_label_selection)

type_lists = [line.rstrip("\n") for line in lines]
var_dict = {}
checkbotton_dict = {}
for type_name in type_lists:
    checkVar = IntVar(value=0)
    var_dict[type_name] = checkVar

    checkbotton = tkinter.Checkbutton(labelframe, text=type_name, variable=checkVar)
    checkbotton_dict[type_name] = checkbotton
    checkbotton.pack(anchor="w")

root.bind('<Left>', lambda event: pre_image())  # 绑定左箭头键到上一张图片
root.bind('<Right>', lambda event: next_image())  # 绑定右箭头键到下一张图片

btn_before = tkinter.Button(panedwindow, text='上一张', command=lambda: pre_image(), width=5, height=1)
btn_after = tkinter.Button(panedwindow, text='下一张', command=lambda: next_image(), width=5, height=1)
save_after = tkinter.Button(panedwindow, text='保存并退出', command=lambda: save_images(), width=8, height=1)

btn_before.place(x=240, y=470, anchor='w')
btn_after.place(x=340, y=470, anchor='w')
save_after.place(x=500, y=470, anchor='w')

panedwindow.add(label_img)
panedwindow.add(labelframe)

# 填满整个界面
panedwindow.pack(fill='both', expand='yes')

root.mainloop()
