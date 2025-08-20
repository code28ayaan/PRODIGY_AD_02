import customtkinter as ctk
from datetime import datetime, timedelta
import json
import os
from tkinter import messagebox
import threading
import time
from tkcalendar import DateEntry
from tkinter import ttk
from PIL import Image, ImageTk

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Todo List")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        # Set dark theme as default
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#1a1a1a")  # Dark background
        
        # Initialize variables
        self.tasks = []
        self.theme_mode = "dark"
        
        # Load existing tasks
        self.load_tasks()
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)  # Main content area
        self.grid_rowconfigure(0, weight=1)
        
        # Create main content area
        self.create_main_content()
        
        # Create floating add button
        self.create_floating_button()
        
    def create_main_content(self):
        # Main content frame with solid background
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            self.main_frame, 
            text="☀️", 
            width=50, 
            height=30, 
            font=("Arial", 16),
            command=self.toggle_theme
        )
        self.theme_button.place(relx=0.95, rely=0.05, anchor="ne")
        
        # Tasks frame with transparent background
        self.tasks_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.tasks_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        
        # Configure grid for tile layout
        for i in range(4):  # 4 columns
            self.tasks_frame.grid_columnconfigure(i, weight=1)
        
        # Refresh tasks display
        self.refresh_tasks()
        
    def create_floating_button(self):
        # Floating add button (water drop style)
        self.floating_button = ctk.CTkButton(
            self,
            text="+",
            width=60,
            height=60,
            font=("Arial", 24, "bold"),
            command=self.show_add_task_window,
            fg_color="#4169E1",  # Royal blue
            hover_color="#1E90FF",
            corner_radius=30
        )
        # Position in bottom right
        self.floating_button.place(relx=0.95, rely=0.95, anchor="se")
        
    def get_priority_color(self, priority, completed=False):
        if completed:
            return "#2d5a2d"  # Dark green for completed tasks
        elif priority == "High":
            return "#1e3a8a"  # Dark blue for high priority
        elif priority == "Medium":
            return "#ea580c"  # Dark orange for medium priority
        else:
            return "#7c3aed"  # Dark purple for low priority
            
    def get_priority_text_color(self, completed=False):
        if completed:
            return "#a0a0a0"  # Light gray for completed tasks
        else:
            return "#ffffff"  # White for active tasks
            
    def create_task_card(self, task, index):
        # Calculate tile position (4 columns)
        row = index // 4
        col = index % 4
        
        # Task card frame with semi-transparent background
        card_frame = ctk.CTkFrame(
            self.tasks_frame,
            fg_color=self.get_priority_color(task["priority"], task["completed"]),
            width=200,
            height=150,
            corner_radius=10
        )
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        card_frame.grid_propagate(False)  # Maintain fixed size
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Add a semi-transparent overlay for better text readability
        overlay_frame = ctk.CTkFrame(
            card_frame,
            fg_color="transparent",
            corner_radius=10
        )
        overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Priority badge at top
        priority_badge = ctk.CTkLabel(
            overlay_frame,
            text=task["priority"],
            font=("Arial", 10, "bold"),
            text_color="#FFFFFF",
            fg_color="transparent"
        )
        priority_badge.grid(row=0, column=0, padx=5, pady=5, sticky="ne")
        
        # Checkbox for completion
        completed_var = ctk.BooleanVar(value=task["completed"])
        checkbox = ctk.CTkCheckBox(
            overlay_frame,
            text="",
            variable=completed_var,
            command=lambda: self.toggle_task_completion(index),
            fg_color=self.get_priority_text_color(task["completed"]),
            hover_color=self.get_priority_text_color(task["completed"])
        )
        checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        # Task details
        details_frame = ctk.CTkFrame(overlay_frame, fg_color="transparent")
        details_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        details_frame.grid_columnconfigure(0, weight=1)
        
        # Task description (truncated for tile view)
        desc_text = task["description"][:30] + "..." if len(task["description"]) > 30 else task["description"]
        desc_label = ctk.CTkLabel(
            details_frame,
            text=desc_text,
            font=("Arial", 12, "bold" if not task["completed"] else "normal"),
            text_color=self.get_priority_text_color(task["completed"])
        )
        desc_label.grid(row=0, column=0, sticky="w")
        
        # Priority and due date
        due_label = ctk.CTkLabel(
            details_frame,
            text=f"Priority: {task['priority']} | Due: {task['due_date']}",
            font=("Arial", 10),
            text_color=self.get_priority_text_color(task["completed"])
        )
        due_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(overlay_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        # Edit button
        edit_button = ctk.CTkButton(
            buttons_frame,
            text="Edit",
            width=50,
            height=25,
            command=lambda: self.edit_task(index),
            font=("Arial", 10)
        )
        edit_button.grid(row=0, column=0, padx=2)
        
        # Delete button
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Del",
            width=50,
            height=25,
            command=lambda: self.delete_task(index),
            font=("Arial", 10)
        )
        delete_button.grid(row=0, column=1, padx=2)
        
    def show_add_task_window(self):
        # Create floating add task window
        add_window = ctk.CTkToplevel(self)
        add_window.title("Add New Task")
        add_window.geometry("400x500")
        add_window.resizable(False, False)
        add_window.configure(fg_color="#2d2d2d")  # Dark theme
        add_window.grab_set()
        
        # Configure grid
        add_window.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            add_window,
            text="Add New Task",
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF"
        )
        title_label.grid(row=0, column=0, pady=20)
        
        # Task entry
        task_entry = ctk.CTkEntry(
            add_window, 
            placeholder_text="Enter task description...",
            font=("Arial", 14),
            width=300
        )
        task_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Priority dropdown
        priority_var = ctk.StringVar(value="Medium")
        priority_dropdown = ctk.CTkOptionMenu(
            add_window,
            values=["Low", "Medium", "High"],
            variable=priority_var,
            font=("Arial", 14),
            width=300
        )
        priority_dropdown.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Due date entry
        date_label = ctk.CTkLabel(
            add_window,
            text="Due Date:",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        )
        date_label.grid(row=3, column=0, pady=(20, 5), sticky="w", padx=20)
        
        due_date_entry = DatePickerFrame(add_window)
        due_date_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        # Add button
        def add_task_from_window():
            description = task_entry.get().strip()
            priority = priority_var.get()
            due_date = due_date_entry.get_date()
            
            if not description:
                messagebox.showwarning("Warning", "Please enter a task description!")
                return
                
            # Validate due date
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                    return
            
            task = {
                "description": description,
                "priority": priority,
                "due_date": due_date,
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "completed": False
            }
            
            self.tasks.append(task)
            self.save_tasks()
            self.refresh_tasks()
            add_window.destroy()
        
        add_button = ctk.CTkButton(
            add_window, 
            text="Add Task", 
            command=add_task_from_window,
            font=("Arial", 16, "bold"),
            width=300,
            height=40
        )
        add_button.grid(row=5, column=0, padx=20, pady=20)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            add_window, 
            text="Cancel", 
            command=add_window.destroy,
            font=("Arial", 14),
            width=300,
            height=35
        )
        cancel_button.grid(row=6, column=0, padx=20, pady=10)
        
    def edit_task(self, index):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            
            # Create edit dialog
            edit_window = ctk.CTkToplevel(self)
            edit_window.title("Edit Task")
            edit_window.geometry("400x300")
            edit_window.resizable(False, False)
            
            # Configure grid
            edit_window.grid_columnconfigure(0, weight=1)
            
            # Task description
            ctk.CTkLabel(edit_window, text="Task Description:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
            desc_entry = ctk.CTkEntry(edit_window, font=("Arial", 14))
            desc_entry.insert(0, task["description"])
            desc_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            
            # Priority
            ctk.CTkLabel(edit_window, text="Priority:", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=10, pady=(10, 5), sticky="w")
            priority_var = ctk.StringVar(value=task["priority"])
            priority_dropdown = ctk.CTkOptionMenu(
                edit_window,
                values=["Low", "Medium", "High"],
                variable=priority_var,
                font=("Arial", 14)
            )
            priority_dropdown.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
            
            # Due date
            ctk.CTkLabel(edit_window, text="Due Date (YYYY-MM-DD):", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=10, pady=(10, 5), sticky="w")
            due_entry = ctk.CTkEntry(edit_window, font=("Arial", 14))
            due_entry.insert(0, task["due_date"])
            due_entry.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
            
            # Save button
            def save_changes():
                new_desc = desc_entry.get().strip()
                new_priority = priority_var.get()
                new_due = due_entry.get().strip()
                
                if not new_desc:
                    messagebox.showwarning("Warning", "Please enter a task description!")
                    return
                    
                if new_due:
                    try:
                        datetime.strptime(new_due, "%Y-%m-%d")
                    except ValueError:
                        messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                        return
                
                self.tasks[index]["description"] = new_desc
                self.tasks[index]["priority"] = new_priority
                self.tasks[index]["due_date"] = new_due
                
                self.save_tasks()
                self.refresh_tasks()
                edit_window.destroy()
            
            save_button = ctk.CTkButton(
                edit_window,
                text="Save Changes",
                command=save_changes,
                font=("Arial", 14)
            )
            save_button.grid(row=6, column=0, padx=10, pady=20)
            
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
            if result:
                del self.tasks[index]
                self.save_tasks()
                self.refresh_tasks()
                
    def toggle_task_completion(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.save_tasks()
            self.refresh_tasks()
            
    def refresh_tasks(self):
        # Clear existing widgets
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
            
        # Sort tasks: incomplete first, then by priority, then by due date
        sorted_tasks = sorted(self.tasks, key=lambda x: (
            x["completed"],  # False comes first
            {"High": 0, "Medium": 1, "Low": 2}[x["priority"]],
            x["due_date"] if x["due_date"] != "No due date" else "9999-12-31"
        ))
        
        # Create task cards
        for i, task in enumerate(sorted_tasks):
            self.create_task_card(task, i)

    def toggle_theme(self):
        if self.theme_mode == "light":
            self.theme_mode = "dark"
            self.theme_button.configure(text="☀️")
            ctk.set_appearance_mode("dark")
            # Keep background image for dark theme
            # Update title color
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == "My Todo List":
                    widget.configure(text_color="#FFFFFF")
        else:
            self.theme_mode = "light"
            self.theme_button.configure(text="🌙")
            ctk.set_appearance_mode("light")
            # Keep background image for light theme
            # Update title color
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == "My Todo List":
                    widget.configure(text_color="#000000")
        
        # Refresh tasks to update card colors
        self.refresh_tasks()
 
    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=2)
            
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r") as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []

class DatePickerFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.date_var = ctk.StringVar()
        self.create_widgets()
        
    def create_widgets(self):
        # Manual entry
        self.date_entry = ctk.CTkEntry(
            self,
            placeholder_text="Due date (YYYY-MM-DD)",
            font=("Arial", 14),
            textvariable=self.date_var
        )
        self.date_entry.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        
        # Calendar button
        self.calendar_button = ctk.CTkButton(
            self,
            text="📅",
            width=40,
            command=self.show_calendar
        )
        self.calendar_button.grid(row=0, column=1, padx=(0, 5), pady=5)
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            self,
            text="✕",
            width=40,
            command=self.clear_date
        )
        self.clear_button.grid(row=0, column=2, padx=0, pady=5)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        
    def show_calendar(self):
        # Create calendar window
        calendar_window = ctk.CTkToplevel(self)
        calendar_window.title("Select Date")
        calendar_window.geometry("300x250")
        calendar_window.resizable(False, False)
        calendar_window.grab_set()
        
        # Create calendar widget
        cal = DateEntry(
            calendar_window,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        cal.pack(padx=20, pady=20)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(calendar_window)
        buttons_frame.pack(pady=20)
        
        def select_date():
            selected_date = cal.get_date()
            self.date_var.set(selected_date.strftime("%Y-%m-%d"))
            calendar_window.destroy()
            
        def cancel():
            calendar_window.destroy()
        
        # Select button
        select_button = ctk.CTkButton(
            buttons_frame,
            text="Select",
            command=select_date
        )
        select_button.pack(side="left", padx=5)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=cancel
        )
        cancel_button.pack(side="left", padx=5)
        
    def clear_date(self):
        self.date_var.set("")
        
    def get_date(self):
        return self.date_var.get()
        
    def set_date(self, date):
        self.date_var.set(date)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = TodoApp()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop() 
