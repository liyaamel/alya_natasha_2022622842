import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Empty string for no password
    database="tasks_database.db"
)

cursor = connection.cursor()

# Create the tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        due_date TEXT,
        priority INTEGER
    )
''')
connection.commit()

def create_task():
    name = entry_name.get()
    due_date = entry_due_date.get()
    priority = entry_priority.get()

    cursor.execute("INSERT INTO tasks (name, due_date, priority) VALUES (%s, %s, %s)", (name, due_date, priority))
    connection.commit()
    messagebox.showinfo("Success", "Task created successfully!")
    refresh_task_list()


def read_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks_data = cursor.fetchall()
    
    tasks_listbox.delete(0, tk.END)
    for task in tasks_data:
        tasks_listbox.insert(tk.END, f"{task[1]} - Due: {task[2]} - Priority: {task[3]}")

def delete_task():
    selected_task_index = tasks_listbox.curselection()
    
    if selected_task_index:
        selected_task_id = selected_task_index[0] + 1  # Adding 1 because SQLite uses 1-based indexing
        cursor.execute("DELETE FROM tasks WHERE id = ?", (selected_task_id,))
        connection.commit()
        messagebox.showinfo("Success", "Task deleted successfully!")
        refresh_task_list()
    else:
        messagebox.showinfo("Error", "Please select a task to delete.")

def refresh_task_list():
    read_tasks()

# Create the main window
root = tk.Tk()
root.title("To-Do List")

# Entry widgets
label_name = tk.Label(root, text="Task Name:")
label_name.grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

label_due_date = tk.Label(root, text="Due Date:")
label_due_date.grid(row=1, column=0)
entry_due_date = tk.Entry(root)
entry_due_date.grid(row=1, column=1)

label_priority = tk.Label(root, text="Priority:")
label_priority.grid(row=2, column=0)
entry_priority = tk.Entry(root)
entry_priority.grid(row=2, column=1)

# Buttons for CRUD operations
button_create = tk.Button (root, text="Create Task", command=lambda:
create_task())   
button_create.grid(row=3, column=0)   

button_read = tk.Button(root, text="Read Tasks", command=lambda:
refresh_task_list())
button_read.grid(row=3, column=1)

button_delete = tk.Button(root, text="Delete Task", command=lambda: delete_task())
button_delete.grid(row=4, column=0)


# Listbox to display tasks
tasks_listbox = tk.Listbox(root, height=10, width=50)
tasks_listbox.grid(row=5, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()

# Close the database connection when the program exits
connection.close()
