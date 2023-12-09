# author: PES2UG23CS368 Nathan Matthew Paul
# author: PES2UG23CS371 Navneet Nayak
# author: PES2UG23CS3XX Nevin Mathew Thomas
# author: PES2UG23CS390 Nilay Srivastava
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2023

import threading
import simpleaudio as sa
from tkinter import *
from tkinter import ttk

def play_sound_async():
    wave_obj = sa.WaveObject.from_wave_file("key.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

class Window:

    def __init__(self):
        self.window = Tk()
        self.window.configure(background="gray25")
        self.window.geometry("720x480")
        self.window.resizable(False, False)
        self.frame = ttk.Frame(self.window, padding=10)
        self.frame.grid()
        self.window.grid_columnconfigure((0,1), weight=1)
        self.window.grid_rowconfigure((0,1, 2, 3, 4), weight=1)
        self.restarted = False
        self.setup()

    def setup(self):

        self.misspelled = 0
        self.spelled = 1
        self.total_time = 41
        self.accuracy = 0
        self.wpm = 0
        self.write_able = True
        self.cursor_blink = True

        self.type_time = self.total_time - 1

        text = "python is python is python is python is python is python is python is" 
        self.title_label = Label(self.window, text="py-typer", font=("roboto condensed", 66), fg="#ebc934", background="gray25")
        self.title_label.place(rely=0.05, relx=0.01, anchor=W)

        self.untyped_text = Label(self.window, text=text, font=("roboto condensed", 61), background="gray25", fg="gray60")
        self.untyped_text.place(relx=0.5, rely=0.5, anchor=W)

        self.typed_text = Label(self.window, text="", font=("roboto condensed", 61), fg="#ebc934", background="gray25")
        self.typed_text.place(relx=0.5, rely=0.5, anchor=E)

        self.time_label = Label(self.window, text=self.type_time, font=("roboto condensed", 30), fg="#ebc934", background="gray25")
        self.time_label.grid(row=1, column=2, sticky=S)

        self.accuracy_label = Label(self.window, text=self.accuracy, font=("roboto condensed", 30), fg="#ebc934", background="gray25")
        self.accuracy_label.grid(row=1, column=3, sticky=S)

        self.wpm_label = Label(self.window, text=self.wpm, font=("roboto condensed", 30), fg="#ebc934", background="gray25")
        self.wpm_label.grid(row=1, column=4, sticky=S)

        self.cursor_label = Label(self.window, text="||", background="gray25", fg="gray60", font=("roboto", 20), wraplength=1)
        self.cursor_label.place(relx=0.499, rely=0.51, anchor=CENTER)

        self.calculate_accuracy()
        self.calculate_wpm()
        self.cursor_blinking()
        
        self.window.bind('<KeyPress>', self.key_press)

    def restart(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.restarted = True
        self.setup()

    def main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        results_label = Label(self.window, text=self.wpm + "  " + self.accuracy, font=("roboto", 80, "bold"), background="gray25", fg="#ebc934")
        results_label.place(relx=0.5, rely=0.4, anchor=CENTER)

        restart_button = Button(self.window, text="Restart",font=("roboto", 30), background="gray25", command=self.restart, highlightbackground="gray25", fg="#ebc934")
        restart_button.place(rely=0.6, relx=0.5, anchor=CENTER)

        mode_button = Button(self.window, text="Mode", font=("roboto", 30), highlightbackground="gray25", fg="#ebc934", background="gray25", bg="blue")
        mode_button.place(rely=0.8, relx=0.5, anchor=CENTER)

    def key_press(self,event):
        if not self.restarted :
            if self.spelled == 1:
                self.countdown()
        if not self.write_able:
            return 
        if event.char == self.untyped_text.cget('text')[:1]:
            sound_thread = threading.Thread(target=play_sound_async)
            sound_thread.start()
            self.typed_text.configure(text=self.typed_text.cget('text') + event.char)
            self.untyped_text.configure(text=self.untyped_text.cget('text')[1:])
            self.spelled += 1
            if len(self.untyped_text.cget('text')) < 1:
                self.main_menu()
        else:
            self.misspelled += 1
        self.calculate_accuracy()

    def countdown(self):
        if self.type_time > 0:
            self.type_time -= 1
            try:
                self.time_label.configure(text=self.type_time)
            except TclError: pass
            self.window.after(1000, self.countdown)
        else:
            self.write_able = False
            self.main_menu()

    def calculate_accuracy(self):
        self.accuracy = str(int((self.spelled / (self.spelled + self.misspelled)) * 100)) + "%"
        try:
            self.accuracy_label.configure(text=self.accuracy)
        except TclError: pass

    def calculate_wpm(self):
        try:
            words_typed = len(self.typed_text.cget('text').split())
            elapsed_time = self.total_time - self.type_time
            self.wpm = str(int((words_typed / elapsed_time) * 60)) + " WPM"
            self.wpm_label.configure(text=self.wpm)
        except TclError:
            pass
        self.window.after(1000, self.calculate_wpm)

    def plot_graph(self):
        pass

    def modes(self):
        pass

    def cursor_blinking(self):
        if self.cursor_blink:
            try: self.cursor_label.configure(text="")
            except TclError: pass 
            self.cursor_blink = False
        else:
            try: self.cursor_label.configure(text="||")
            except TclError: pass
            self.cursor_blink = True
        self.window.after(500, self.cursor_blinking)
        
window = Window()
window.window.mainloop()
