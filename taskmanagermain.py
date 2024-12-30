import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import platform
import random

# Global variables
tasks = []
base_time_slice = 5000  # Base time slice in milliseconds (5 seconds)
is_running = False

FONT_STYLE = ("Arial", 12)
ACCENT_COLOR = "#3498DB"  # Change the hexadecimal value for the desired accent color

def on_entry_click(event):
    if event.widget.get() == event.widget.placeholder_text:
        event.widget.delete(0, tk.END)
        event.widget.config(fg="black")

def on_entry_leave(event):
    if event.widget.get() == "":
        event.widget.insert(0, event.widget.placeholder_text)
        event.widget.config(fg=PLACEHOLDER_COLOR)

def add_task():
    task = entry_task.get().strip()
    selected_date = cal.get_date()
    selected_time = time_picker.get()

    if not task or not selected_date or not selected_time:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        due_date = datetime.combine(selected_date, datetime.strptime(selected_time, "%I:%M %p").time()).strftime(
            "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showwarning(
            "Warning", "Invalid time format. Please use HH:MM AM/PM format for time.")
        return

    tasks.append((task, due_date))
    update_treeview()
    clear_entry_fields()

def remove_task():
    selected_task_index = tree.focus()
    if not selected_task_index:
        messagebox.showwarning("Warning", "Please select a task to remove.")
        return

    task_index = int(tree.item(selected_task_index, 'text')) - 1
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        update_treeview()
    else:
        messagebox.showwarning("Warning", "Invalid task index selected.")

def check_tasks():
    current_time = datetime.now()
    for task, due_date in tasks:
        due_datetime = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        if current_time > due_datetime:
            messagebox.showwarning("Alert", f"Task '{task}' is overdue!")
        elif current_time < due_datetime:
            messagebox.showinfo("Scheduled", f"Task '{task}' is scheduled for {due_date}")
    time_slice = base_time_slice + len(tasks) * 1000  # Adjust time slice based on the number of tasks

    if is_running and len(tasks) > 0:
        root.after(time_slice, check_tasks)  # Check again after 'time_slice' milliseconds

def start_scheduling():
    global is_running
    if not is_running and tasks:
        is_running = True
        check_tasks()

def update_treeview():
    tasks.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d %H:%M"))
    tree.delete(*tree.get_children())
    for i, (task, due_date) in enumerate(tasks, start=1):
        tree.insert("", 'end', text=str(i), values=(task, due_date))

def clear_entry_fields():
    entry_task.delete(0, tk.END)
    entry_task.insert(0, entry_task.placeholder_text)
    cal.set_date(datetime.now())
    time_picker.set(time_picker.placeholder_text)

def generate_random_task():
    task_names = ["Study", "Exercise/Work-Out", "Read a book", "Write", "Code", "Meditate","Cook","Skincare","Power Nap"]
    random_task = random.choice(task_names)
    entry_task.delete(0, tk.END)
    entry_task.insert(0, random_task)

root = tk.Tk()
root.title("TASK MANAGER")

# Set window to maximize
if platform.system() == 'Windows':
    root.state('zoomed')
elif platform.system() in ['Linux', 'Darwin']:  # Linux/MacOS
    root.attributes('-zoomed', True)  # Fullscreen for Linux/MacOS

# Add Background Image
background_image = Image.open("C:\\Users\\pauln\\Desktop\\image20.png")  # Replace "C:\\Users\\pauln\\Desktop\\image20.png" with your image file path
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
bg_image = ImageTk.PhotoImage(background_image)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Transparent Frames
entry_frame = tk.Frame(root, bg="", bd=0, highlightthickness=0)
entry_frame.pack(pady=10)
entry_task = tk.Entry(entry_frame, font=FONT_STYLE, width=22)
entry_task.placeholder_text = "Enter your task"
entry_task.insert(0, entry_task.placeholder_text)
entry_task.bind('<FocusIn>', on_entry_click)
entry_task.bind('<FocusOut>', on_entry_leave)
entry_task.pack(pady=5)

calendar_frame = tk.Frame(root, bg="", bd=0, highlightthickness=0)
calendar_frame.pack(pady=10)
cal = DateEntry(calendar_frame, font=FONT_STYLE, width=20, date_pattern="yyyy-mm-dd")
cal.placeholder_text = "Select Date"
cal.bind('<FocusIn>', on_entry_click)
cal.bind('<FocusOut>', on_entry_leave)
cal.set_date(datetime.now())
cal.pack(pady=5)

time_frame = tk.Frame(root, bg="", bd=0, highlightthickness=0)
time_frame.pack(pady=10)
time_picker = ttk.Combobox(time_frame, font=FONT_STYLE, width=20)
time_picker.placeholder_text = "Select Time"
time_picker['values'] = ['12:00 AM', '12:30 AM', '1:00 AM', '1:30 AM', '2:00 AM', '2:30 AM',
                         '3:00 AM', '3:30 AM', '4:00 AM', '4:30 AM', '5:00 AM', '5:30 AM',
                         '6:00 AM', '6:30 AM', '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM',
                         '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
                         '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM',
                         '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM',
                         '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM',
                         '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM']
time_picker.set(time_picker.placeholder_text)
time_picker.bind('<FocusIn>', on_entry_click)
time_picker.bind('<FocusOut>', on_entry_leave)
time_picker.pack(pady=5)

button_frame = tk.Frame(root, bg="", bd=0, highlightthickness=0)
button_frame.pack(pady=10)
add_button = tk.Button(button_frame, text="Add Task", command=add_task, font=FONT_STYLE, bg=ACCENT_COLOR, fg="white", width=15)
add_button.pack(pady=5)
remove_button = tk.Button(button_frame, text="Remove Task", command=remove_task, font=FONT_STYLE, bg=ACCENT_COLOR, fg="white", width=15)
remove_button.pack(pady=5)
start_button = tk.Button(button_frame, text="Start Scheduling", command=start_scheduling, font=FONT_STYLE, bg=ACCENT_COLOR, fg="white", width=15)
start_button.pack(pady=5)
random_task_button = tk.Button(root, text="Default Tasks", command=generate_random_task, font=FONT_STYLE, bg=ACCENT_COLOR,fg="white", width=15 )
random_task_button.pack(pady=5)

# Create a style for the treeview
style = ttk.Style()
style.configure("Custom.Treeview", background=root["bg"])  # Match the background with the root window

# Apply the style to the treeview
tree = ttk.Treeview(root, columns=('Task', 'Due Date'), show='headings', style="Custom.Treeview")

#tree = ttk.Treeview(root, columns=('Task', 'Due Date'), show='headings')
tree.heading('Task', text='Task')
tree.heading('Due Date', text='Due Date')
tree.column('Task', width=150, anchor='center')
tree.column('Due Date', width=150, anchor='center')
tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

root.mainloop()