import tkinter as tk
from tkinter import messagebox
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class User:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

class Admin(User):
    def __init__(self, user_id, username, master):
        super().__init__(user_id, username, "admin")
        self.master = master
        master.title("Admin Dashboard")
        self.create_widgets()

    def create_widgets(self):
        # Basic Admin functionalities - you'll expand on these
        tk.Label(self.master, text="Admin Actions", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.master, text="Add New User", command=self.add_user_window).pack(pady=5)
        tk.Button(self.master, text="Update Student Record", command=self.update_student_window).pack(pady=5)
        tk.Button(self.master, text="Delete Student Record", command=self.delete_student_window).pack(pady=5)
        tk.Button(self.master, text="Generate Insights", command=self.generate_insights_window).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.logout).pack(pady=10)

    def add_user_window(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New User")

        tk.Label(add_window, text="User ID:").grid(row=0, column=0, padx=5, pady=5)
        user_id_entry = tk.Entry(add_window)
        user_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        username_entry = tk.Entry(add_window)
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        password_entry = tk.Entry(add_window, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Role (admin/student):").grid(row=3, column=0, padx=5, pady=5)
        role_entry = tk.Entry(add_window)
        role_entry.grid(row=3, column=1, padx=5, pady=5)

        add_button = tk.Button(add_window, text="Add User",
                                command=lambda: self._add_user(user_id_entry.get(), username_entry.get(),
                                                               password_entry.get(), role_entry.get(), add_window))
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def _add_user(self, user_id, username, password, role, window):
        try:
            with open('users.txt', 'a', newline='') as users_file:
                writer = csv.writer(users_file)
                writer.writerow([user_id, username, role.lower()])
            with open('passwords.txt', 'a', newline='') as passwords_file:
                writer = csv.writer(passwords_file)
                writer.writerow([username, password])
            messagebox.showinfo("Success", f"User '{username}' added successfully.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding user: {e}")

    def update_student_window(self):
        # Create a new window for updating student records
        update_window = tk.Toplevel(self.master)
        update_window.title("Update Student Record")
        tk.Label(update_window, text="This functionality will be implemented here.").pack(padx=20, pady=20)

    def delete_student_window(self):
        # Create a new window for deleting student records
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Delete Student Record")
        tk.Label(delete_window, text="This functionality will be implemented here.").pack(padx=20, pady=20)

    def generate_insights_window(self):
        insights_window = tk.Toplevel(self.master)
        insights_window.title("Generated Insights")

        try:
            grades_df = pd.read_csv('grades.txt', header=None, names=['student_id', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5'])
            average_grades = grades_df[['sub1', 'sub2', 'sub3', 'sub4', 'sub5']].mean()

            tk.Label(insights_window, text="Average Grades per Subject:", font=("Arial", 12, "bold")).pack(pady=5)
            for subject, avg in average_grades.items():
                tk.Label(insights_window, text=f"{subject}: {avg:.2f}").pack()

            eca_df = pd.read_csv('eca.txt', header=None)
            eca_activities = eca_df.iloc[:, 1:].values.flatten()
            active_students_eca = pd.Series(eca_activities).value_counts().head(5)

            tk.Label(insights_window, text="\nMost Active ECAs:", font=("Arial", 12, "bold")).pack(pady=5)
            for activity, count in active_students_eca.items():
                tk.Label(insights_window, text=f"{activity}: {count} participants").pack()

            # Basic Grade Visualization (Bar Chart)
            fig, ax = plt.subplots()
            average_grades.plot(kind='bar', ax=ax)
            ax.set_title('Average Grades')
            ax.set_ylabel('Average Mark')
            canvas = FigureCanvasTkAgg(fig, master=insights_window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(pady=10)

        except FileNotFoundError:
            tk.Label(insights_window, text="Error: One or more data files not found.").pack()
        except Exception as e:
            tk.Label(insights_window, text=f"Error generating insights: {e}").pack()

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        login_gui = LoginGUI(root)
        root.mainloop()

class Student(User):
    def __init__(self, user_id, username, master):
        super().__init__(user_id, username, "student")
        self.master = master
        self.student_id = user_id
        master.title("Student Dashboard")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Student Actions", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.master, text="Update Profile Information", command=self.update_profile_window).pack(pady=5)
        tk.Button(self.master, text="View Details", command=self.view_details_window).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.logout).pack(pady=10)

    def update_profile_window(self):
        update_window = tk.Toplevel(self.master)
        update_window.title("Update Profile")
        tk.Label(update_window, text="This functionality will be implemented here.").pack(padx=20, pady=20)

    def view_details_window(self):
        details_window = tk.Toplevel(self.master)
        details_window.title("Your Details")

        try:
            with open('users.txt', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == str(self.student_id):
                        tk.Label(details_window, text="Personal Details:", font=("Arial", 12, "bold")).pack()
                        tk.Label(details_window, text=f"User ID: {row[0]}").pack()
                        tk.Label(details_window, text=f"Username: {row[1]}").pack()
                        break
                else:
                    tk.Label(details_window, text="Student details not found.").pack()

            with open('grades.txt', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == str(self.student_id):
                        tk.Label(details_window, text="\nExam Grades:", font=("Arial", 12, "bold")).pack()
                        subjects = ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"]
                        for i, mark in enumerate(row[1:]):
                            tk.Label(details_window, text=f"{subjects[i]}: {mark}").pack()
                        break
                else:
                    tk.Label(details_window, text="Grades not found.").pack()

            with open('eca.txt', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == str(self.student_id):
                        tk.Label(details_window, text="\nECA Participation:", font=("Arial", 12, "bold")).pack()
                        for activity in row[1:]:
                            tk.Label(details_window, text=f"- {activity}").pack()
                        break
                else:
                    tk.Label(details_window, text="ECA details not found.").pack()

        except FileNotFoundError:
            tk.Label(details_window, text="Error: One or more data files not found.").pack()
        except Exception as e:
            tk.Label(details_window, text=f"Error viewing details: {e}").pack()

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        login_gui = LoginGUI(root)
        root.mainloop()

class LoginGUI:
    def __init__(self, master):
        self.master = master
        master.title("Student Management System Login")
        self.username_label = tk.Label(master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            with open('passwords.txt', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == username and row[1] == password:
                        with open('users.txt', 'r') as users_file:
                            users_reader = csv.reader(users_file)
                            for user_data in users_reader:
                                if user_data[1] == username:
                                    user_id = int(user_data[0])
                                    role = user_data[2]
                                    self.master.destroy()
                                    new_root = tk.Tk()
                                    if role == 'admin':
                                        admin_gui = Admin(user_id, username, new_root)
                                    elif role == 'student':
                                        student_gui = Student(user_id, username, new_root)
                                    new_root.mainloop()
                                    return
            messagebox.showerror("Login Failed", "Invalid username or password.")
        except FileNotFoundError:
            messagebox.showerror("Error", "passwords.txt not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Login error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    login_gui = LoginGUI(root)
    root.mainloop()

    import tkinter as tk
from tkinter import messagebox, ttk
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np  # For numerical operations

class User:
    def _init_(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

class Admin(User):
    def _init_(self, user_id, username, master):
        super()._init_(user_id, username, "admin")
        self.master = master
        master.title("Admin Dashboard")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Admin Actions", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.master, text="Add New User", command=self.add_user_window).pack(pady=5)
        tk.Button(self.master, text="Update Student Record", command=self.update_student_window).pack(pady=5)
        tk.Button(self.master, text="Delete Student Record", command=self.delete_student_window).pack(pady=5)
        tk.Button(self.master, text="Performance Analytics", command=self.show_analytics_dashboard).pack(pady=10)
        tk.Button(self.master, text="Logout", command=self.logout).pack(pady=10)

    def add_user_window(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New User")
        # (Same implementation as before)
        tk.Label(add_window, text="User ID:").grid(row=0, column=0, padx=5, pady=5)
        user_id_entry = tk.Entry(add_window)
        user_id_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(add_window, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        username_entry = tk.Entry(add_window)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(add_window, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        password_entry = tk.Entry(add_window, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(add_window, text="Role (admin/student):").grid(row=3, column=0, padx=5, pady=5)
        role_entry = tk.Entry(add_window)
        role_entry.grid(row=3, column=1, padx=5, pady=5)
        add_button = tk.Button(add_window, text="Add User",
                               command=lambda: self._add_user(user_id_entry.get(), username_entry.get(),
                                                            password_entry.get(), role_entry.get(), add_window))
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def _add_user(self, user_id, username, password, role, window):
        try:
            with open('users.txt', 'a', newline='') as users_file:
                writer = csv.writer(users_file)
                writer.writerow([user_id, username, role.lower()])
            with open('passwords.txt', 'a', newline='') as passwords_file:
                writer = csv.writer(passwords_file)
                writer.writerow([username, password])
            messagebox.showinfo("Success", f"User '{username}' added successfully.")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding user: {e}")

    def update_student_window(self):
        update_window = tk.Toplevel(self.master)
        update_window.title("Update Student Record")
        tk.Label(update_window, text="This functionality will be implemented here.").pack(padx=20, pady=20)

    def delete_student_window(self):
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Delete Student Record")
        tk.Label(delete_window, text="This functionality will be implemented here.").pack(padx=20, pady=20)

    def show_analytics_dashboard(self):
        analytics_window = tk.Toplevel(self.master)
        analytics_window.title("Performance Analytics Dashboard")

        notebook = ttk.Notebook(analytics_window)

        grade_trends_tab = ttk.Frame(notebook)
        self.display_grade_trends(grade_trends_tab)
        notebook.add(grade_trends_tab, text="Grade Trends")

        eca_impact_tab = ttk.Frame(notebook)
        self.analyze_eca_impact(eca_impact_tab)
        notebook.add(eca_impact_tab, text="ECA Impact")

        performance_alerts_tab = ttk.Frame(notebook)
        self.generate_performance_alerts(performance_alerts_tab)
        notebook.add(performance_alerts_tab, text="Performance Alerts")

        notebook.pack(expand=True, fill='both')

    def display_grade_trends(self, parent):
        try:
            grades_df = pd.read_csv('grades.txt', header=None, names=['student_id', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5'])
            users_df = pd.read_csv('users.txt', header=None, names=['user_id', 'username', 'role'])
            student_users = users_df[users_df['role'] == 'student']
            merged_df = pd.merge(grades_df, student_users, left_on='student_id', right_on='user_id', how='inner')

            fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
            subject_columns = ['sub1', 'sub2', 'sub3', 'sub4', 'sub5']
            merged_df[subject_columns].mean().plot(kind='bar', ax=axes)
            axes.set_title('Average Grade per Subject')
            axes.set_ylabel('Average Mark')
            axes.set_xlabel('Subject')
            axes.tick_params(axis='x', rotation=45)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(expand=True, fill='both', padx=10, pady=10)
            canvas.draw()

        except FileNotFoundError:
            tk.Label(parent, text="Error: grades.txt or users.txt not found.").pack(padx=10, pady=10)
        except pd.errors.EmptyDataError:
            tk.Label(parent, text="Error: No grade data available.").pack(padx=10, pady=10)
        except Exception as e:
            tk.Label(parent, text=f"Error displaying grade trends: {e}").pack(padx=10, pady=10)

    def analyze_eca_impact(self, parent):
        try:
            eca_df = pd.read_csv('eca.txt', header=None, names=['student_id'] + [f'activity{i+1}' for i in range(10)]) # Adjust number of activity columns as needed
            grades_df = pd.read_csv('grades.txt', header=None, names=['student_id', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5'])

            # Melt ECA data to have one row per student-activity
            eca_melted = pd.melt(eca_df, id_vars=['student_id'], value_name='activity')
            eca_melted = eca_melted[eca_melted['activity'].notna() & (eca_melted['activity'] != '')] # Remove NaN or empty activities

            # Calculate average grade per student
            grades_df['average_grade'] = grades_df[['sub1', 'sub2', 'sub3', 'sub4', 'sub5']].mean(axis=1)

            # Merge ECA and Grade data
            merged_df = pd.merge(eca_melted, grades_df[['student_id', 'average_grade']], on='student_id', how='left')

            # Calculate average grade for students involved in each ECA
            eca_performance = merged_df.groupby('activity')['average_grade'].mean().sort_values(ascending=False)

            fig, ax = plt.subplots(figsize=(10, 6))
            eca_performance.plot(kind='bar', ax=ax)
            ax.set_title('Average Academic Performance by ECA Involvement')
            ax.set_xlabel('Extracurricular Activity')
            ax.set_ylabel('Average Grade')
            ax.tick_params(axis='x', rotation=45, ha='right')
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(expand=True, fill='both', padx=10, pady=10)
            canvas.draw()

        except FileNotFoundError:
            tk.Label(parent, text="Error: eca.txt or grades.txt not found.").pack(padx=10, pady=10)
        except pd.errors.EmptyDataError:
            tk.Label(parent, text="Error: No ECA or grade data available.").pack(padx=10, pady=10)
        except Exception as e:
            tk.Label(parent, text=f"Error analyzing ECA impact: {e}").pack(padx=10, pady=10)

    def generate_performance_alerts(self, parent):
        try:
            grades_df = pd.read_csv('grades.txt', header=None, names=['student_id', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5'])
            users_df = pd.read_csv('users.txt', header=None, names=['user_id', 'username', 'role'])
            student_grades = pd.merge(grades_df, users_df[users_df['role'] == 'student'], left_on='student_id', right_on='user_id', how='inner')
            student_grades['average_grade'] = student_grades[['sub1', 'sub2', 'sub3', 'sub4', 'sub5']].mean(axis=1)

            threshold = 60  # Example threshold
            below_threshold = student_grades[student_grades['average_grade'] < threshold]

            tk.Label(parent, text=f"Students Performing Below {threshold}%:", font=("Arial", 12, "bold")).pack(pady=5)
            if not below_threshold.empty:
                for index, row in below_threshold.iterrows():
                    tk.Label(parent, text=f"- {row['username']} (Average: {row['average_grade']:.2f}%) - Consider academic support.").pack()
            else:
                tk.Label(parent, text("No students currently below the threshold.").pack())

        except FileNotFoundError:
            tk.Label(parent, text="Error: grades.txt or users.txt not found.").pack(padx=10, pady=10)
        except pd.errors.EmptyDataError:
            tk.Label(parent, text="Error: No student or grade data available.").pack(padx=10, pady=10)
        except Exception as e:
            tk.Label(parent, text=f"Error generating performance alerts: {e}").pack(padx=10, pady=10)

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        login_gui = LoginGUI(root)
        root.mainloop()

class Student(User):
    def _init_(self, user_id, username, master):
        super()._init_(user_id, username, "student")
        self.master = master
        self.student_id = user_id
        master.title("Student Dashboard")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Student Actions", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.master, text="Update Profile Information", command=self.update_profile_window).pack(pady=5)
        tk.Button(self.master, text="View Details", command=self.view_details_window).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.logout).pack(pady=10)

    def update_profile_window(self):
        update_window = tk.Toplevel(self.master)
        update_window.title("Update Profile")
        tk.Label(update_window, text="This functionality will be implemented here.").pack(padx=20, pady=20)

    def view_details_window(self):
        details_window = tk.Toplevel(self.master)
        details_window.title("Your Details")
        try:
            with open('users.txt', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == str(self.student_id):
                        tk.Label(details_window, text="Personal Details:", font=("Arial", 12, "bold")).pack()
                        tk.Label(details_window, text=f"User ID: {row[0]}").pack()
                        tk.Label(details_window, text=f"Username: {row[1]}").pack()
                        break
                else:
                    tk.Label(details_window, text="Student details not found.").pack()
            with open('grades.txt', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == str(self.student_id):
                        tk.Label(details_window, text="\nExam Grades:", font=("Arial", 12, "bold")).pack()
                        subjects = ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"]
                        for i, mark in enumerate(row[1:]):
                            tk.Label(details_window, text=f"{subjects[i]}: {mark}").pack()
                        break
                else:
                    tk.Label(details_window, text="Grades not found.").pack()
            with open('eca.txt', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == str(self.student_id):
                        tk.Label(details_window, text="\nECA Participation:", font=("Arial", 12, "bold")).pack()
                        for activity in row[1:]:
                            tk.Label(details_window, text=f"- {activity}").pack()
                        break
                else:
                    tk.Label(details_window, text="ECA details not found.").pack()
        except FileNotFoundError:
            tk.Label(details_window, text="Error: One or more data files not found.").pack()
        except Exception as e:
            tk.Label(details_window, text=f"Error viewing details: {e}").pack()

    def logout(self):
        self.master.destroy()
        root = tk.Tk()
        login_gui = LoginGUI(root)
        root.mainloop()

class LoginGUI:
    def _init_(self, master):
        self.master = master
        master.title("Student Management System Login")
        self.username_label = tk.Label(master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
