import tkinter as tk
import sys
import os
import threading

def run_sub(): os.system('py windows\\subjects.py')
def run_fac(): os.system('py windows\\faculty.py')
def run_stud(): os.system('py windows\\student.py')
def run_sch(): os.system('py windows\\scheduler.py')
def run_tt_s(): os.system('py windows\\timetable_stud.py')
def run_tt_f(): os.system('py windows\\timetable_fac.py')

ad = tk.Tk()
ad.geometry('500x430')

ad.title('Administrator')

tk.Label(
    ad,
    text='A D M I N I S T R A T O R',
    font=('Consolas', 20, 'bold'),
    pady=10
).pack()

tk.Label(
    ad,
    text='You are the Administrator',
    font=('Consolas', 12, 'italic'),
).pack(pady=9)

modify_frame = tk.LabelFrame(text='Modify', font=('Consolas'), padx=20)
modify_frame.place(x=50, y=100)

tk.Button(
    modify_frame,
    text='Subjects',
    font=('Consolas'),
    command=run_sub
).pack(pady=20)

tk.Button(
    modify_frame,
    text='Faculties',
    font=('Consolas'),
    command=run_fac
).pack(pady=20)

tk.Button(
    modify_frame,
    text='Students',
    font=('Consolas'),
    command=run_stud
).pack(pady=20)

tt_frame = tk.LabelFrame(text='Timetable', font=('Consolas'), padx=20)
tt_frame.place(x=250, y=100)

tk.Button(
    tt_frame,
    text='Schedule Periods',
    font=('Consolas'),
    command=run_sch
).pack(pady=20)

tk.Button(
    tt_frame,
    text='View Section-Wise',
    font=('Consolas'),
    command=run_tt_s
).pack(pady=20)

tk.Button(
    tt_frame,
    text='View Faculty-wise',
    font=('Consolas'),
    command=run_tt_f
).pack(pady=20)


tk.Button(
    ad,
    text='Quit',
    font=('Consolas'),
    command=ad.destroy
).place(x=220, y=360)

ad.mainloop()