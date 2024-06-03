import tkinter as tk
from PIL import Image, ImageTk
import random
import numpy as np
from tkinter import Tk, Label, Button, scrolledtext, filedialog, StringVar, PhotoImage
from os import path
from tkinter.ttk import Combobox

def clicked():
    global file, tk_emp_con
    file = filedialog.askopenfilename(filetypes=(("Image files", "*.bmp"), ("all files", "*.*")), initialdir=path.dirname(__file__))
    if file:
        lbl11.configure(text=file.split('/')[-1])
        file = file.split('/')[-1]
        emp_con = Image.open(file)
        emp_con = emp_con.resize((300, 200))
        tk_emp_con = ImageTk.PhotoImage(emp_con)

def select_text_file():
    global text_file_path
    text_file_path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")), initialdir=path.dirname(__file__))
    if text_file_path:
        lbl_text_file.configure(text=text_file_path.split('/')[-1])

def enable_raid():
    combobox_raid.configure(state='readonly')

def disable_raid():
    combobox_raid.configure(state='disabled')

def hiding():
    global image_for_ext, tk_image, lenmes, H

    def ext_pix(image):
        pixels = list(image.getdata())
        for i in range(len(pixels)):
            pixels[i] = list(pixels[i])
            for j in range(len(pixels[i])):
                pixels[i][j] = bin(pixels[i][j])[2:].zfill(8)
        return pixels

    if text_file_path:
        with open(text_file_path, 'r', encoding='utf-8') as f:
            secmes = f.read()

    if method_var.get() == 'LSB-R':
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)

        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)

        raid = int(raid_var.get())
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                r = list(pixels[i][j][-raid:])
                for k in range(len(r)):
                    if binary_secmes == '':
                        break
                    elif r[k] != binary_secmes[0]:
                        r[k] = binary_secmes[0]
                    binary_secmes = binary_secmes[1:]
                pixels[i][j] = pixels[i][j][:-raid] + ''.join(r)

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])

        image_LSB_R = Image.new('RGB', (width, height))
        image_LSB_R.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_LSB_R.save(save_path)

        image_for_ext = image_LSB_R
        image_LSB_R = image_LSB_R.resize((300, 200))
        tk_image = ImageTk.PhotoImage(image_LSB_R)

    elif method_var.get() == 'LSB-M':
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)

        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)

        raid = int(raid_var.get())
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                if binary_secmes == '':
                    break
                l = int(binary_secmes[:raid], 2)
                r = pixels[i][j]
                if l != int(r[-raid:], 2):
                    if raid != 1:
                        k1 = 0
                        while l != int(r[-raid:], 2):
                            r = bin(int(r, 2) + 1)[2:]
                            k1 += 1
                        r1 = r
                        r = pixels[i][j]
                        k2 = 0
                        while l != int(r[-raid:], 2) and not (bin(int(r, 2) - 1).startswith('-')):
                            r = bin(int(r, 2) - 1)[2:]
                            k2 += 1
                        r2 = r
                        R = [r1, r2]
                        if k1 > k2:
                            pixels[i][j] = r1
                        elif k1 < k2:
                            pixels[i][j] = r2
                        else:
                            pixels[i][j] = random.choice(R)
                    else:
                        pixels[i][j] = bin(int(pixels[i][j], 2) + random.choice([-1, 1]))[2:]
                binary_secmes = binary_secmes[raid:]

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])

        image_LSB_M = Image.new('RGB', (width, height))
        image_LSB_M.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_LSB_M.save(save_path)

        image_for_ext = image_LSB_M
        image_LSB_L = image_LSB_M.resize((300, 200))
        tk_image = ImageTk.PhotoImage(image_LSB_L)

    elif method_var.get() == 'Hamming Code':
        image = Image.open(file)
        width, height = image.size
        pixels = ext_pix(image)

        lenmes = len(secmes)
        binary_secmes = ''.join(format(ord(x), '08b') for x in secmes)

        H = np.array([list(format(i, '04b')) for i in range(1, 16)], dtype=int).T

        pr = False
        for i in range(len(pixels)):
            c = np.array(list(pixels[i][0][-5:] + pixels[i][1][-5:] + pixels[i][2][-5:]))
            c = np.array(list(map(int, c)))
            m = np.array(list(binary_secmes[:4]))
            m = np.array(list(map(int, m)))
            binary_secmes = binary_secmes[4:]
            while len(binary_secmes) < 4:
                binary_secmes += '0'
                pr = True
            if pr:
                break

            s = (H @ c + m) % 2

            I = 8 * s[0] + 4 * s[1] + 2 * s[2] + s[3]
            if I == 0:
                continue

            c_mod = c
            c_mod[I - 1] = not c_mod[I - 1]
            c_mod = ''.join(str(int(x)) for x in c_mod)

            pixels[i][0] = pixels[i][0][:-5] + c_mod[:5]
            c_mod = c_mod[5:]
            pixels[i][1] = pixels[i][1][:-5] + c_mod[:5]
            c_mod = c_mod[5:]
            pixels[i][2] = pixels[i][2][:-5] + c_mod[:5]
            c_mod = c_mod[5:]

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = int(pixels[i][j], 2)
            pixels[i] = tuple(pixels[i])

        image_Hem = Image.new('RGB', (width, height))
        image_Hem.putdata(pixels)
        save_path = filedialog.asksaveasfilename(defaultextension=".bmp")
        if save_path:
            image_Hem.save(save_path)

        image_for_ext = image_Hem
        image_Hem = image_Hem.resize((300, 200))
        tk_image = ImageTk.PhotoImage(image_Hem)

def extraction():
    global image_for_ext, tk_image, lenmes, H

    def ext_pix(image):
        pixels = list(image.getdata())
        for i in range(len(pixels)):
            pixels[i] = list(pixels[i])
            for j in range(len(pixels[i])):
                pixels[i][j] = bin(pixels[i][j])[2:].zfill(8)
        return pixels

    if method_var.get() == 'LSB-R' or method_var.get() == 'LSB-M':
        raid = int(raid_var.get())
        image = image_for_ext
        pixels = ext_pix(image)
        secmes = ''
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                secmes += pixels[i][j][-raid:]
        chunks = [secmes[i:i + 8] for i in range(0, len(secmes), 8)]
        mes = ''.join(chr(int(chunk, 2)) for chunk in chunks)
        mes = mes[:lenmes]

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("all files", "*.*")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(mes)

    elif method_var.get() == 'Hamming Code':
        image = image_for_ext
        pixels = ext_pix(image)
        m_all = ''
        for i in range(len(pixels)):
            c = np.array(list(pixels[i][0][-5:] + pixels[i][1][-5:] + pixels[i][2][-5:]))
            c = np.array(list(map(int, c)))
            s = (H @ c) % 2

            m = s
            m_all += ''.join(str(int(x)) for x in m)
        chunks = [m_all[i:i + 8] for i in range(0, len(m_all), 8)]
        mes = ''.join(chr(int(chunk, 2)) for chunk in chunks)
        mes = mes[:lenmes]

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("all files", "*.*")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(mes)

window = Tk()
window.title("Steganography")
window.geometry('450x200')

# Add image file
bg = PhotoImage(file="fon.png")

# Show image using label
label1 = Label(window, image=bg)
label1.place(x=0, y=0)
# lbl = Label(window, text="")
# lbl.grid(column=0, row=0)
lbl11 = Label(window, text="Файл не выбран")
lbl11.grid(column=2, row=0)
btn = Button(window, text="Контейнер", command=clicked)
btn.grid(column=1, row=0)
lbl7 = Label(window, text="Метод:")
lbl7.grid(column=0, row=1)

method_var = StringVar()
combobox_method = Combobox(window, textvariable=method_var)
combobox_method['values'] = ("LSB-R", "LSB-M", "Hamming Code")
combobox_method.grid(column=1, row=1)

lbl8 = Label(window, text="Рейт внедрения:")
lbl8.grid(column=0, row=2)
raid_var = StringVar()
combobox_raid = Combobox(window, textvariable=raid_var, state='disabled')
combobox_raid['values'] = (1, 2, 3)
combobox_raid.grid(column=1, row=2)

lbl_text_file = Label(window, text="Файл не выбран")
lbl_text_file.grid(column=2, row=3)
btn_select_text_file = Button(window, text="Сообщение", command=select_text_file)
btn_select_text_file.grid(column=1, row=3)

btn2 = Button(window, text="Внести", command=hiding)
btn2.grid(column=0, row=4)

btn3 = Button(window, text="Извлечь", command=extraction)
btn3.grid(column=1, row=4)

combobox_method.bind("<<ComboboxSelected>>", lambda event: enable_raid() if method_var.get() in ['LSB-R', 'LSB-M'] else disable_raid())

window.mainloop()