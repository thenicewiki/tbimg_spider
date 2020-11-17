from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.font as tf
import os
import time
import _thread
import re
import requests
import Spider
import subprocess


class Demo:
    def __init__(self):
        super().__init__()

        self.url_link = []
        self.url_img_link = []

        self.root = Tk()
        self.root.geometry("720x700")
        self.root.resizable(0, 0)
        self.root.title('A Spider')

        self.ft15 = tf.Font(size=15)
        self.ft12 = tf.Font(size=12)

        # 文字 (Label)
        text = Label(self.root, text='互联网信息爬取工具', font=self.ft15)
        text.pack(fill=Y, pady=15)

        self.url = StringVar()

        frame_entry = Frame(self.root)
        frame_entry.pack(fill=Y, pady=10)

        url_reset = Button(frame_entry, text='Url (R)', command=self.clear_url_entry)
        url_reset.grid(row=1, column=0)

        self.url_entry_line = Entry(frame_entry, textvariable=self.url)
        self.url_entry_line.grid(row=1, column=1, ipadx=150)

        button = Button(frame_entry, text="解析", command=self.hi)
        button.grid(row=1, column=2)

        button2 = Button(frame_entry, text="多链接", command=self.multiple_urls)
        button2.grid(row=1, column=3)

        self.g = LabelFrame(self.root, text="Consoles", padx=5, pady=5)
        self.g.pack(fill=BOTH)

        self.listbox = Listbox(self.g)
        self.listbox.pack(fill=BOTH, ipady=50)

        cmd_frame = Frame(self.root)
        cmd_frame.pack(fill=X, pady=10)

        self.cmd = StringVar()

        cmd_label = Label(cmd_frame, text='Command:   ')
        cmd_label.grid(row=1, column=0)
        self.cmdEntry = Entry(cmd_frame, textvariable=self.cmd)
        self.cmdEntry.grid(row=1, column=1, ipadx=20)
        cmd_tip = Button(cmd_frame, text='Commit', command=self.commit)
        cmd_tip.grid(row=1, column=3)

        self.mes = Label(cmd_frame, text="程序初始化完成...")
        self.mes.grid(row=1, column=4, padx=90)

        self.wait = Label(cmd_frame, text="")
        self.wait.grid(row=1, column=5)

        # self.text = Text(self.root, font = ft12)
        # self.text.pack(fill = Y)
        # self.text.insert(END, "Demo \n")

        button_frame = Frame(self.root)
        button_frame.pack(fill=Y, pady=15)

        button1 = Button(button_frame, text="获取图片链接", command=self.get_url)
        button2 = Button(button_frame, text="下载至本地", command=self.download)
        button3 = Button(button_frame, text="清空控制台", command=self.clear)
        button4 = Button(button_frame, text="打开下载目录", command=self.open_folder)

        button1.grid(row=1, column=0, ipadx=30, padx=1)
        button2.grid(row=1, column=1, ipadx=30, padx=1)
        button3.grid(row=1, column=2, ipadx=30, padx=1)
        button4.grid(row=1, column=3, ipadx=30, padx=1)

        self.separator = Frame(self.root, height=15, bg='green', relief=GROOVE)
        self.separator.pack(fill=X, padx=5, pady=5)

        # frame10
        frame10 = Frame(self.root)
        frame10.pack()
        # 容器框 （LabelFrame）
        self.group = LabelFrame(frame10, text="Hello", padx=5, pady=5)
        self.group.grid(pady=20)
        w = Label(self.group, text='本学习项目由  http://pegasu.cn  出品 \n\nGithub: https://github.com/pegasuswiki')
        w.pack()

        self.close_button = Button(self.root, text='退出程序', command=self.exit_editor)
        self.close_button.pack(fill=Y, ipadx=10, ipady=10)

        self.root.mainloop()

    def hi(self):
        text = self.url.get()
        if text == "":
            messagebox.showwarning('警告', '输入内容为空!')
            return

        # init
        self.url_link.clear()
        self.url_img_link.clear()
        self.listbox.delete(0, END)

        self.listbox.insert(END, "Date:  " + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
        self.url_link = re.findall('(h.+?\d+)', text)

        if self.url_link:
            self.listbox.insert(END, '您输入的链接地址为:')
            for url in self.url_link:
                self.listbox.insert(END, url)

            self.listbox.insert(END, '正在解析您的链接地址请稍后!')
            _thread.start_new_thread(self.get_img_url, ())
            # self.get_img_url()
            _thread.start_new_thread(self.check_img_url, ())

            self.listbox.yview_moveto(1)
        else:
            self.separator['bg'] = 'red'
            messagebox.showwarning('警告', '输入链接非法!\n请重新输入')
            self.url_entry_line.delete(0, 'end')

    def commit(self):
        self.mes['text'] = "Command \" %s \"Commited" % self.cmd.get()
        self.cmdEntry.delete(0, 'end')

    def clear(self):
        self.listbox.delete(0, END)
        print("Consoles had been cleaned!")
        self.mes['text'] = "   控制台已清空"
        self.separator['bg'] = "green"

    def download(self):
        self.mes['text'] = "内容正在下载至本地..."
        self.separator['bg'] = "yellow"
        _thread.start_new_thread(self.down_good, ())

    def down_good(self):
        num = 0
        if not os.path.exists('./images'):
            os.makedirs('./images')
        for link in self.url_img_link:
            response = requests.get(link)
            obj = response.content
            with open('./images/' + link[-10:-5] + '.jpg', 'wb') as file:
                file.write(obj)
            self.listbox.insert(END, '成功下载第 %d 张图片!' % (num + 1))
            self.listbox.yview_moveto(1)
            time.sleep(0.1)
            num += 1
        self.listbox.insert(END, '所有图片下载完成!')
        self.mes['text'] = "所有图片下载完成!"
        self.separator['bg'] = "green"
        self.listbox.insert(END, "当前时间:  " + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
        self.listbox.insert(END, '')
        self.listbox.yview_moveto(1)

    def open_folder(self):
        self.mes['text'] = "   下载目录已打开"
        self.separator['bg'] = "green"
        subprocess.Popen('./images')

    def get_url(self):
        self.show_url()
        self.mes['text'] = "成功获取连接地址！"
        self.separator['bg'] = "green"

    def input_delay(self):
        print('Waiting...')
        self.separator['bg'] = 'red'
        time.sleep(0.5)
        self.listbox.insert(END, "请重新输入...")
        self.listbox.insert(END, " ")

    def show_url(self):
        url_editor = Toplevel(self.root)
        url_editor.geometry("1100x360")
        url_editor.resizable(0, 0)

        url_editor.title('Url Clipboard')

        text_editor = Text(url_editor, font=self.ft15)
        text_editor.pack(fill=BOTH)
        for url in self.url_img_link:
            text_editor.insert(END, url+'\n')


        # show_frame = Frame(url_editor)
        # show_frame.pack(fill=Y)

        # copy = Button(show_frame, text="复制", command=lambda: self.clear_url(text_editor))
        # copy.grid(row=1, column=0)
        #
        # close = Button(show_frame, text="关闭", command=lambda: self.clear_url(text_editor))
        # close.grid(row=1, column=1)

    def clear_url(self, text_editor):
        text_editor.delete(0.0, END)
        messagebox.showinfo('提示', '链接地址已清空')

    def clear_url_entry(self):
        self.url_entry_line.delete(0, 'end')
    # def checkDownload(self):
    # while True:
    #     time.sleep(0.5)
    #     self.wait['text'] = "内容正在下载至本地."
    #     time.sleep(0.5)
    #     self.wait['text'] = "内容正在下载至本地.."
    #     time.sleep(0.5)
    #     self.wait['text'] = "内容正在下载至本地..."
    def multiple_urls(self):
        urls_editor = Toplevel(self.root)
        urls_editor.geometry("800x500")
        urls_editor.resizable(0, 0)
        urls_editor.title('Url Clipboard')

        text_editor = Text(urls_editor, font=self.ft15)
        text_editor.pack(fill=BOTH)

        mult_frame = Frame(urls_editor)
        mult_frame.pack(fill=Y)

        clear_button = Button(mult_frame, text="解析", command=lambda: self.get_clipboard(text_editor))
        clear_button.grid(row=1, column=1)

        clear_button = Button(mult_frame, text="清空", command=lambda: self.clear_url(text_editor))
        clear_button.grid(row=1, column=0)

    def get_clipboard(self, text_editor):
        self.listbox.delete(0, END)
        self.listbox.insert(END, "Date:  " + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
        self.url_link.clear()
        self.url_img_link.clear()
        text = text_editor.get(0.0, 'end')
        print(text)

        url = re.findall("(http.+?\d+)", text)
        self.url_link.extend(url)
        print(url)
        print(self.url_link)

        if self.url_link:
            self.listbox.insert(END, '您输入的链接地址为:')
            for url in self.url_link:
                self.listbox.insert(END, url)

            self.listbox.insert(END, '正在解析您的链接地址请稍后!')
            _thread.start_new_thread(self.get_img_url, ())
            _thread.start_new_thread(self.check_img_url, ())

            self.listbox.yview_moveto(1)
        else:
            self.separator['bg'] = 'red'
            messagebox.showwarning('警告', '输入链接非法!\n请重新输入')
            self.url_entry_line.delete(0, 'end')

    def get_img_url(self):
        self.url_img_link.extend(Spider.demo(self.url_link))

        print(self.url_img_link)

    def check_img_url(self):
        t = 0.2
        while True:
            if self.url_img_link:
                self.listbox.insert(END, '解析完成!')
                print(len(self.url_link))
                self.listbox.insert(END, '成功获取 %d 张图片' % len(self.url_img_link))
                self.listbox.insert(END, '总共用时间: %.2f 秒' % t)
                if t < 10:
                    self.listbox.insert(END, '网络质量: 良好')
                else:
                    self.listbox.insert(END, '网络质量: 一般')

                self.listbox.insert(END, '点击下方\"获取图片链接\"取得对应链接地址!')
                self.listbox.insert(END, '点击下方\"下载至本地\"下载至当前目录')
                self.listbox.insert(END, "当前时间:  " + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
                self.listbox.insert(END, "")
                self.listbox.yview_moveto(1)
                self.separator['bg'] = "green"
                break
            else:
                time.sleep(0.1)
                t += 0.1
                self.listbox.insert(END, '已用时 %.2f 秒' % t)
                if t > 20:
                    self.listbox.insert(END, '网页长时间未响应 请确认网络是否连通!')
                    self.listbox.yview_moveto(1)
                    break
                self.listbox.yview_moveto(1)

    def exit_editor(self):
        if messagebox.askokcancel("退出?", "确定退出吗?"):
            self.root.quit()


Demo()
# link = ['http://tieba.baidu.com/p/4178314700', 'https://tieba.baidu.com/p/7062767729']
# a = Spider.demo(link)
# print(a, len(a))
# print(len(a))

"""
爬取到的图片名称列表
爬取到的图片链接的列表
选择需要下载图片的列表
"""