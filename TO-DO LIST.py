from asyncio import tasks
from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task(task_field=None, the_cursor=None):
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('error', 'field is empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into task values (?)', (task_string ,))
        list_update()
        task_field.delete(0, 'end')
def list_update(task_listbox=None):
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task(the_cursor=None, task_listbox=None):
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title = ?', (the_value))
    except:
        messagebox.showinfo('error', 'no task selected. cannot delete.')

def delete_all_tasks(the_cursor=None, task=None):
    message_box = messagebox.askyesno('delete all', 'are you sure?')
    if message_box == True:
        while(len(tasks) != 0):
            task.pop()
        the_cursor.execute('delete from tasks')
        list_update()
def clear_list(task_listbox=None):
    task_listbox.delete(0, 'end')

def close(guiwindow=None):
    print(tasks)
    guiwindow.destroy()

def retrieve_database(if__name=None, the_cursor=None, guiwindow=None):
    while(len(tasks) != 0):
        tasks.pop()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

if__name__ =="__main__":
    guiwindow = Tk()
    guiwindow.title("To-Do List ")
    guiwindow.geometry("665x400+550+250")
    guiwindow.resizeable(bg = "#BSESCF")

    the_connection = sql.connect('listoftasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

functions_frame = Frame(guiwindow, bg = "#8EESEE")

functions_frame.pack(side = "top", expand = True, fill = "both")

task_lable1 = Lable( functions_frame,text = "To-Do List \n Enter the task title:",
    font = ("aria1", "14", "bold"),
    background = "#8EESEE",
    foreground = "#FF6103"
)
task_lable.place(x = 20, y = 30)

task_field = Entry(
    functions_frame,
    font = ("aria1", "14"),
    width = 42,
    foreground = "black",
    background = "white",
)
task_field.place(x = 180, y = 30)

add_button =Button(
    functions_frame,
    text = "Add",
    width = 15,
    bg='#D4AC0D',font=("aria1", "14", "bold"),
    command = add_task,

)
del_button = Button(
    functions_frame,
    text = "Remove",
    width = 15,
    bg= '#D4AC0D', font=("aria1", "14", "bold"),
    command = delete_task,
)
del_all_button =Button(
    functions_frame,
    text = "Delete All",
    width = 15,
    font=("aria1", "14", "bold"),
    bg='#D4AC0D',
    command = delete_all_tasks
)

exit_button = Button(
    functions_frame,
    text = "Exit / close",
    width = 52,
    bg='#D4AC0D', font=("aria1", "14", "bold"),
    command = close
)
add_button.place(x = 18, y = 80)
del_button.place(x = 240, y = 80)
del_all_button.place(x = 460, y = 80)
exit_button.place(x = 17, y = 330)

task_listbox = Listbox(
    functions_frame,
    width = 70,
    height = 9,
    font="bold",
    selectmode = 'SINGLE',
    background = "WHITE",
    foreground = "BLACK",
    selectbackground = "#FF8C00",
    selectforeground = "BLACK"
)
task_listbox.place(x = 17, y = 140)

retrieve_database()
list_update()
guiwindow.mainloop()
the_connection.commit()
the_cursor.close











