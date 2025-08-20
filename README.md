# ✅ Todo List App (CustomTkinter GUI)
A modern, stylish, and responsive **Todo List desktop application** built using **Python**, **CustomTkinter**, and **tkcalendar**. This app features task creation, editing, prioritization, due dates, completion tracking, and theme switching (light/dark).


## 📦 Features

* 📝 **Task Management**
  * Add, edit, delete tasks
  * Mark tasks as completed/incomplete
  * Assign priorities (High, Medium, Low)
  * Set optional due dates

* 🌗 **Light/Dark Theme Toggle**
  * Switch between light and dark modes seamlessly

* 📅 **Date Picker**
  * Select due dates via a user-friendly calendar widget

* 💾 **Data Persistence**
  * All tasks are saved locally in a `tasks.json` file

* 🎨 **Modern UI**
  * Responsive grid layout
  * Color-coded task cards based on priority and completion

* 📦 **Floating Add Button**
  * Add tasks from any view with an easy-access "+" button


## 🖼️ UI Preview

![image alt](https://github.com/GITWithAkshay/PRODIGY_AD_02/blob/640237c61e032817551154172c3e5ac701c303c2/Screenshot%20(196).png)
![image alt](https://github.com/GITWithAkshay/PRODIGY_AD_02/blob/640237c61e032817551154172c3e5ac701c303c2/Screenshot%20(197).png)
![image alt](https://github.com/GITWithAkshay/PRODIGY_AD_02/blob/640237c61e032817551154172c3e5ac701c303c2/Screenshot%20(204).png)

## 🛠️ Tech Stack

| Component                 | Library/Tool           |
| ------------------------- | ---------------------- |
| GUI Framework             | `customtkinter`        |
| Date Picker               | `tkcalendar`           |
| JSON Storage              | Built-in `json` module |
| Calendar UI               | `DateEntry`            |
| Threading (optional)      | `threading` module     |
| Image Handling (optional) | `Pillow`               |

---

## 📂 Project Structure

```
📁 todo-app/
├── tasks.json               # Stored tasks
├── main.py                  # Main app script
├── README.md                # Project documentation
```

---

## 🧑‍💻 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/GITWithAkshay/tkinter-todo-app.git
cd tkinter-todo-app
```

### 2. Set up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the App

```bash
python main.py
```

---

## 💾 Data Format (`tasks.json`)

```json
[
  {
    "description": "Finish README",
    "priority": "High",
    "due_date": "2025-07-01",
    "created_date": "2025-06-28",
    "completed": false
  }
]
```

---

## ✨ Key Components Overview

| Component                       | Description                             |
| ------------------------------- | --------------------------------------- |
| `TodoApp`                       | Main application window                 |
| `create_task_card()`            | Renders task tiles in a responsive grid |
| `show_add_task_window()`        | Floating modal to add new tasks         |
| `edit_task()`                   | In-place task editing modal             |
| `DatePickerFrame`               | Integrated calendar + manual date input |
| `toggle_theme()`                | Switches between dark and light UI      |
| `save_tasks()` / `load_tasks()` | JSON-based local storage                |

---

## 🧠 Sorting Logic

Tasks are auto-sorted by:

1. **Completion Status**: Incomplete tasks appear first
2. **Priority**: High → Medium → Low
3. **Due Date**: Earliest first

## ⚙️ Customization Tips

* 🔧 **Change Default Theme**: In `__init__()`, modify:
  ```python
  ctk.set_appearance_mode("dark")
  ```

* 🎨 **Update Colors**: Change values in `get_priority_color()` and `get_priority_text_color()`
  
* 🧱 **Add More Fields**: Extend the `task` dictionary and GUI layout

## 🧪 Troubleshooting
| Issue                    | Fix                                        |
| ------------------------ | ------------------------------------------ |
| App crashes on calendar  | Ensure `tkcalendar` is installed           |
| Tasks not saving         | Check write permissions for `tasks.json`   |
| Theme colors not visible | Tweak `fg_color` or text colors in widgets |

## 📜 License
This project is open-source and free to use. Consider crediting if you reuse large portions of the code.

## 🙌 Acknowledgements
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) by Tom Schimansky
* [tkcalendar](https://github.com/j4321/tkcalendar)
* Python Standard Library ❤️
