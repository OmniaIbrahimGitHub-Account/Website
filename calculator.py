import tkinter as tk
from tkinter import messagebox

# Grade letter to GPA mapping
grade_map = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "D-": 0.7,
    "F": 0.0
}

class GPACalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Calculator")
        self.root.geometry("500x550")
        self.center_window()

        self.courses = []

        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.btn_bg = "#4a90e2"
        self.btn_fg = "#ffffff"
        self.entry_bg = "#ffffff"
        self.entry_fg = "#000000"
        self.error_fg = "#d9534f"

        self.create_widgets()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.root.configure(bg=self.bg_color)
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(pady=15)

        label_font = ("Helvetica", 14, "bold")
        entry_font = ("Helvetica", 14)
        btn_font = ("Helvetica", 14, "bold")
        result_font = ("Helvetica", 16, "bold")

        # Course Name
        tk.Label(frame, text="Course Name (optional):", bg=self.bg_color, fg=self.fg_color, font=label_font).grid(row=0, column=0, sticky="w", pady=5)
        self.course_name_entry = tk.Entry(frame, width=25, font=entry_font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.course_name_entry.grid(row=0, column=1, padx=10)

        # Grade
        tk.Label(frame, text="Grade (A, B+, 3.7, ...):", bg=self.bg_color, fg=self.fg_color, font=label_font).grid(row=1, column=0, sticky="w", pady=5)
        self.grade_entry = tk.Entry(frame, width=25, font=entry_font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.grade_entry.grid(row=1, column=1, padx=10)

        # Credit Hours
        tk.Label(frame, text="Credit Hours:", bg=self.bg_color, fg=self.fg_color, font=label_font).grid(row=2, column=0, sticky="w", pady=5)
        self.hours_entry = tk.Entry(frame, width=25, font=entry_font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.hours_entry.grid(row=2, column=1, padx=10)

        # Add Course Button
        self.add_btn = tk.Button(frame, text="Add Course", command=self.add_course, font=btn_font, bg=self.btn_bg, fg=self.btn_fg, activebackground="#357ABD")
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=15, sticky="we")

        # Listbox for courses
        self.listbox = tk.Listbox(self.root, width=60, height=10, font=entry_font, bg=self.entry_bg, fg=self.entry_fg, selectbackground="#4a90e2", activestyle="none")
        self.listbox.pack(pady=10)

        # Calculate GPA Button
        self.calc_btn = tk.Button(self.root, text="Calculate GPA", command=self.calculate_gpa, font=btn_font, bg=self.btn_bg, fg=self.btn_fg, activebackground="#357ABD")
        self.calc_btn.pack(pady=5, fill="x", padx=60)

        # Result Label
        self.result_label = tk.Label(self.root, text="", font=result_font, bg=self.bg_color, fg=self.fg_color)
        self.result_label.pack(pady=15)

        # Reset Button
        self.reset_btn = tk.Button(self.root, text="Reset All", command=self.reset_all, font=btn_font, bg="#d9534f", fg="white", activebackground="#c9302c")
        self.reset_btn.pack(pady=5, fill="x", padx=60)

    def add_course(self):
        name = self.course_name_entry.get().strip()
        grade = self.grade_entry.get().strip().upper()
        hours = self.hours_entry.get().strip()

        if not grade or not hours:
            messagebox.showerror("Error", "Please enter both Grade and Credit Hours.")
            return

        try:
            hours_val = float(hours)
            if hours_val <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Credit Hours must be a positive number.")
            return

        if grade in grade_map:
            grade_val = grade_map[grade]
        else:
            try:
                grade_val = float(grade)
                if grade_val < 0 or grade_val > 4:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Invalid grade. Enter a valid letter grade or a number between 0 and 4.")
                return

        self.courses.append((name, grade_val, hours_val))

        display_name = name if name else "(No name)"
        self.listbox.insert(tk.END, f"{display_name} - Grade: {grade} - Hours: {hours}")

        self.course_name_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)

    def calculate_gpa(self):
        if not self.courses:
            messagebox.showwarning("Warning", "No courses to calculate GPA.")
            return

        total_points = 0
        total_hours = 0

        for _, grade_val, hours_val in self.courses:
            total_points += grade_val * hours_val
            total_hours += hours_val

        gpa = total_points / total_hours if total_hours > 0 else 0

        self.result_label.config(text=f"Cumulative GPA: {gpa:.2f}\nTotal Credit Hours: {total_hours:.1f}")

    def reset_all(self):
        self.courses.clear()
        self.listbox.delete(0, tk.END)
        self.result_label.config(text="")
        self.course_name_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GPACalculator(root)
    root.mainloop()
