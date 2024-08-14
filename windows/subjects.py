import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

# inputs in this window
subcode = subname = subtype = None

'''
    LIST OF FUNCTIONS USED FOR VARIOUS FUNCTIONS THROUGH TKinter INTERFACE
        * create_treeview()
        * update_treeview()
        * parse_data()
        * update_data()
        * remove_data()
'''

# create treeview (call this function once)
def create_treeview():
    tree['columns'] = ('one', 'two', 'three')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=70, stretch=tk.NO)
    tree.column("two", width=300, stretch=tk.NO)
    tree.column("three", width=60, stretch=tk.NO)

    tree.heading('#0', text="")
    tree.heading('one', text="code")
    tree.heading('two', text="Name")
    tree.heading('three', text="Type")



# update treeview (call this function after each update)
def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.execute("SELECT * FROM SUBJECTS")
    for row in cursor:
        # print(row[0], row[1], row[2])
        if row[2] == 'T':
            t = 'Theory'
        elif row[2] == 'P':
            t = 'Practical'
        tree.insert(
            "",
            0,
            values=(row[0],row[1],t)
        )
    tree.place(x=500, y=100)


# Parse and store data into database and treeview upon clcicking of the add button
def parse_data():
    subcode = str(subcode_entry.get())
    subname = str(subname_entry.get("1.0", tk.END)).upper().rstrip()
    subtype = str(radio_var.get()).upper()

    if subcode=="":
        subcode = None
    if subname=="":
        subname = None

    if subcode is None or subname is None:
        messagebox.showerror("Bad Input", "Please fill up Subject Code and/or Subject Name!")
        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)
        return

    conn.execute(f"REPLACE INTO SUBJECTS (SUBCODE, SUBNAME, SUBTYPE)\
        VALUES ('{subcode}','{subname}','{subtype}')")
    conn.commit()
    update_treeview()
    
    subcode_entry.delete(0, tk.END)
    subname_entry.delete("1.0", tk.END)


# update a row in the database
def update_data():
    subcode_entry.delete(0, tk.END)
    subname_entry.delete("1.0", tk.END)
    try:
        # print(tree.selection())
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time to update!")
            return

        row = tree.item(tree.selection()[0])['values']
        subcode_entry.insert(0, row[0])
        subname_entry.insert("1.0", row[1])
        if row[2][0] == "T":
            R1.select()
        elif row[2][0] == "P":
            R2.select()

        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{row[0]}'")
        conn.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return

# remove selected data from databse and treeview
def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror("Bad Select", "Please select a subject from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{tree.item(i)['values'][0]}'")
        conn.commit()
        tree.delete(i)
        update_treeview()



# main
if __name__ == "__main__":  

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS SUBJECTS\
    (SUBCODE CHAR(10) NOT NULL PRIMARY KEY,\
    SUBNAME CHAR(50) NOT NULL,\
    SUBTYPE CHAR(1) NOT NULL)')


    '''
        TKinter WINDOW SETUP WITH WIDGETS
            * Label(1-6)
            * Entry(1)
            * Text(1)
            * Radiobutton(1-2)
            * Treeview(1)
            * Button(1-2)
    '''

    # TKinter Window
    subtk = tk.Tk()
    subtk.geometry('1000x450')
    subtk.title('Add/Update Subjects')

    # Label1
    tk.Label(
        subtk,
        text='List of Subjects',
        font=('Consolas', 20, 'bold')
    ).place(x=600, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Add/Update Subjects',
        font=('Consolas', 20, 'bold')
    ).place(x=100, y=50)

    # Label3
    tk.Label(
        subtk,
        text='Add information in the following prompt!',
        font=('Consolas', 10, 'italic')
    ).place(x=100, y=85)

    # Label4
    tk.Label(
        subtk,
        text='Subject code:',
        font=('Consolas', 15)
    ).place(x=100, y=150)

    # Entry1
    subcode_entry = tk.Entry(
        subtk,
        font=('Consolas', 15),
        width=11
    )
    subcode_entry.place(x=270, y=150)
    
    # Label5
    tk.Label(
        subtk,
        text='Subject Name:',
        font=('Consolas', 15)
    ).place(x=100, y=200)

    # Text
    subname_entry = tk.Text(
        subtk,
        font=('Consolas', 10),
        width=17,
        height=3,
        wrap=tk.WORD
    )
    subname_entry.place(x=270, y=200)

    # Label6
    tk.Label(
        subtk,
        text='Subject Type:',
        font=('Consolas', 15)
    ).place(x=100, y=270)

    # RadioButton variable to store RadioButton Status
    radio_var = tk.StringVar()

    # RadioButton1
    R1 = tk.Radiobutton(
        subtk,
        text='Theory',
        font=('Consolas', 12),
        variable=radio_var,
        value="T"
    )
    R1.place(x=270, y=270)
    R1.select()

    # RadioButton2
    R2 = tk.Radiobutton(
        subtk,
        text='Practical',
        font=('Consolas', 12),
        variable=radio_var,
        value="P"
    )
    R2.place(x=270, y=300)
    R2.select()

    # RadioButton3
    R3 = tk.Radiobutton(
        subtk,
        text='online',
        font=('Consolas', 12),
        variable=radio_var,
        value="O"
    )
    R3.place(x=270, y=330)
    R3.select()


    # Button1
    B1 = tk.Button(
        subtk,
        text='Add Subject',
        font=('Consolas', 12),
        command=parse_data
    )
    B1.place(x=150,y=350)

    # Button2
    B2 = tk.Button(
        subtk,
        text='Update Subject',
        font=('Consolas', 12),
        command=update_data
    )
    B2.place(x=410,y=350)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        subtk,
        text='Delete Subject(s)',
        font=('Consolas', 12),
        command=remove_data
    )
    B3.place(x=650,y=350)

    # looping Tkiniter window
    subtk.mainloop()
    conn.close() # close database ad=fter all operations