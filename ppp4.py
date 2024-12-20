import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Task:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Worker:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def salary(self, task):
        # Return salary for a specific task (task price)
        return task.price

class HR:
    def __init__(self):
        self.tasks = []
        self.workers = []

    def add_task(self, name, price):
        self.tasks.append(Task(name, price))

    def add_worker(self, name):
        self.workers.append(Worker(name))

    def add_task_to_worker(self, worker_name, task_name):
        worker = next((w for w in self.workers if w.name == worker_name), None)
        task = next((t for t in self.tasks if t.name == task_name), None)
        if worker and task:
            worker.tasks.append(task)
            return True
        return False

    def get_worker_salary(self, worker_name):
        worker = next((w for w in self.workers if w.name == worker_name), None)
        if worker:
            return sum(task.price for task in worker.tasks)
        return -1

    def get_combined_salaries(self):
        return sum(worker.salary(task) for worker in self.workers for task in worker.tasks)

    def save_to_db(self):
        conn = sqlite3.connect('hr_manager.db')
        cursor = conn.cursor()

        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                price INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS worker_tasks (
                worker_id INTEGER,
                task_id INTEGER,
                FOREIGN KEY(worker_id) REFERENCES workers(id),
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
        ''')

        # Insert workers
        for worker in self.workers:
            cursor.execute('''
                INSERT OR IGNORE INTO workers (name) VALUES (?)
            ''', (worker.name,))

        # Insert tasks
        for task in self.tasks:
            cursor.execute('''
                INSERT OR IGNORE INTO tasks (name, price) VALUES (?, ?)
            ''', (task.name, task.price))

        # Assign tasks to workers
        for worker in self.workers:
            for task in worker.tasks:
                cursor.execute('''
                    INSERT OR IGNORE INTO worker_tasks (worker_id, task_id)
                    SELECT w.id, t.id FROM workers w, tasks t
                    WHERE w.name = ? AND t.name = ?
                ''', (worker.name, task.name))

        conn.commit()
        conn.close()

    def load_from_db(self):
        conn = sqlite3.connect('hr_manager.db')
        cursor = conn.cursor()

        # Clear current data
        self.workers.clear()
        self.tasks.clear()

        # Load workers
        cursor.execute('SELECT name FROM workers')
        worker_rows = cursor.fetchall()
        for row in worker_rows:
            worker = Worker(row[0])
            self.workers.append(worker)

        # Load tasks
        cursor.execute('SELECT name, price FROM tasks')
        task_rows = cursor.fetchall()
        for row in task_rows:
            task = Task(row[0], row[1])
            self.tasks.append(task)

        # Load worker-task assignments
        cursor.execute('''
            SELECT w.name, t.name FROM worker_tasks wt
            JOIN workers w ON wt.worker_id = w.id
            JOIN tasks t ON wt.task_id = t.id
        ''')
        assignments = cursor.fetchall()
        for worker_name, task_name in assignments:
            worker = next((w for w in self.workers if w.name == worker_name), None)
            task = next((t for t in self.tasks if t.name == task_name), None)
            if worker and task:
                worker.tasks.append(task)

        conn.close()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HR Manager")
        self.geometry("600x600")

        self.hr = HR()
        self.setup_ui()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")

        self.worker_tab = ttk.Frame(self.notebook)
        self.task_tab = ttk.Frame(self.notebook)
        self.assign_task_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.worker_tab, text="Workers")
        self.notebook.add(self.task_tab, text="Tasks")
        self.notebook.add(self.assign_task_tab, text="Assign Tasks")

        self.setup_worker_tab()
        self.setup_task_tab()
        self.setup_assign_task_tab()

        self.save_button = tk.Button(self, text="Save", command=self.save_data)
        self.save_button.pack(pady=10)

        self.load_button = tk.Button(self, text="Load", command=self.load_data)
        self.load_button.pack(pady=10)

    def setup_worker_tab(self):
        tk.Label(self.worker_tab, text="Worker Name:").grid(row=0, column=0, padx=5, pady=5)
        self.worker_name_entry = tk.Entry(self.worker_tab)
        self.worker_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.worker_tab, text="Add Worker", command=self.add_worker).grid(row=1, column=0, columnspan=2, pady=10)

        self.worker_listbox = tk.Listbox(self.worker_tab, width=40, height=10)
        self.worker_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def setup_task_tab(self):
        tk.Label(self.task_tab, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        self.task_name_entry = tk.Entry(self.task_tab)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.task_tab, text="Task Price:").grid(row=1, column=0, padx=5, pady=5)
        self.task_price_entry = tk.Entry(self.task_tab)
        self.task_price_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.task_tab, text="Add Task", command=self.add_task).grid(row=2, column=0, columnspan=2, pady=10)

        self.task_listbox = tk.Listbox(self.task_tab, width=40, height=10)
        self.task_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def setup_assign_task_tab(self):
        tk.Label(self.assign_task_tab, text="Select Worker:").grid(row=0, column=0, padx=5, pady=5)
        self.worker_task_dropdown = ttk.Combobox(self.assign_task_tab, state="readonly")
        self.worker_task_dropdown.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.assign_task_tab, text="Select Task:").grid(row=1, column=0, padx=5, pady=5)
        self.task_dropdown = ttk.Combobox(self.assign_task_tab, state="readonly")
        self.task_dropdown.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.assign_task_tab, text="Assign Task", command=self.assign_task).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.assign_task_tab, text="Calculate Salary", command=self.calculate_salary).grid(row=3, column=0, columnspan=2, pady=10)

        # Treeview to show workers, tasks, and salary
        self.assignment_table = ttk.Treeview(self.assign_task_tab, columns=("Worker", "Task", "Salary"), show="headings")
        self.assignment_table.grid(row=4, column=0, columnspan=2, pady=10)

        self.assignment_table.heading("Worker", text="Worker")
        self.assignment_table.heading("Task", text="Task")
        self.assignment_table.heading("Salary", text="Salary")

    def add_worker(self):
        name = self.worker_name_entry.get()
        if name:
            self.hr.add_worker(name)
            self.update_worker_listbox()
            self.worker_name_entry.delete(0, tk.END)
            self.update_worker_task_dropdown()
        else:
            messagebox.showerror("Error", "Enter a valid worker name")

    def add_task(self):
        name = self.task_name_entry.get()
        try:
            price = int(self.task_price_entry.get())
            if name and price >= 0:
                self.hr.add_task(name, price)
                self.update_task_listbox()
                self.update_task_dropdown()
                self.task_name_entry.delete(0, tk.END)
                self.task_price_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Invalid task details")
        except ValueError:
            messagebox.showerror("Error", "Price should be a number")

    def assign_task(self):
        selected_worker = self.worker_task_dropdown.get()
        selected_task = self.task_dropdown.get()
        if selected_worker and selected_task:
            if self.hr.add_task_to_worker(selected_worker, selected_task):
                self.update_worker_listbox()
                self.update_assignment_table_from_db()  # Refresh the table to reflect updated data
            else:
                messagebox.showerror("Error", "Worker or task not found")
        else:
            messagebox.showerror("Error", "Please select both a worker and a task")

    def calculate_salary(self):
        total_salary = self.hr.get_combined_salaries()
        messagebox.showinfo("Total Salary", f"Combined salary of all workers: {total_salary}")

    def update_worker_listbox(self):
        self.worker_listbox.delete(0, tk.END)
        for worker in self.hr.workers:
            self.worker_listbox.insert(tk.END, worker.name)
        self.update_worker_task_dropdown()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.hr.tasks:
            self.task_listbox.insert(tk.END, f"{task.name} - {task.price} currency")
        self.update_task_dropdown()

    def update_worker_task_dropdown(self):
        self.worker_task_dropdown["values"] = [worker.name for worker in self.hr.workers]

    def update_task_dropdown(self):
        self.task_dropdown["values"] = [task.name for task in self.hr.tasks]

    def update_assignment_table_from_db(self):
        # Clear existing rows in table
        for item in self.assignment_table.get_children():
            self.assignment_table.delete(item)

        for worker in self.hr.workers:
            for task in worker.tasks:
                salary = worker.salary(task)
                self.assignment_table.insert("", "end", values=(worker.name, task.name, salary))

    def save_data(self):
        self.hr.save_to_db()
        messagebox.showinfo("Success", "Data saved successfully")

    def load_data(self):
        self.hr.load_from_db()
        self.update_worker_listbox()
        self.update_task_listbox()
        self.update_assignment_table_from_db()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
