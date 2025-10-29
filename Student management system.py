import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import datetime

class StudentManagementSystem:
    def __init__(self):
        self.connection = None
        self.connect_to_database()
        self.create_gui()
    
    def connect_to_database(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Hari1661@',
                database='student_management'
            )
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def create_gui(self):
        """Create the main GUI window"""
        self.root = tk.Tk()
        self.root.title("Student Management System")
        self.root.geometry("900x600")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_add_tab(notebook)
        self.create_view_tab(notebook)
        self.create_search_tab(notebook)
        self.create_update_tab(notebook)
        self.create_stats_tab(notebook)
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_add_tab(self, notebook):
        """Create Add Student tab"""
        add_frame = ttk.Frame(notebook)
        notebook.add(add_frame, text="Add Student")
        
        # Title
        ttk.Label(add_frame, text="Add New Student", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Input fields
        input_frame = ttk.Frame(add_frame)
        input_frame.pack(pady=10)
        
        # Name
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Email
        ttk.Label(input_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.email_entry = ttk.Entry(input_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Phone
        ttk.Label(input_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.phone_entry = ttk.Entry(input_frame, width=30)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Course
        ttk.Label(input_frame, text="Course:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.course_entry = ttk.Entry(input_frame, width=30)
        self.course_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Grade
        ttk.Label(input_frame, text="Grade:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.grade_entry = ttk.Entry(input_frame, width=30)
        self.grade_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Address
        ttk.Label(input_frame, text="Address:").grid(row=5, column=0, padx=5, pady=5, sticky='ne')
        self.address_text = tk.Text(input_frame, width=30, height=4)
        self.address_text.grid(row=5, column=1, padx=5, pady=5)
        
        # Add button
        ttk.Button(add_frame, text="Add Student", command=self.add_student).pack(pady=10)
    
    def create_view_tab(self, notebook):
        """Create View Students tab"""
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="View Students")
        
        # Title and refresh button
        title_frame = ttk.Frame(view_frame)
        title_frame.pack(fill='x', pady=10)
        
        ttk.Label(title_frame, text="All Students", font=('Arial', 14, 'bold')).pack(side='left', padx=10)
        ttk.Button(title_frame, text="Refresh", command=self.load_students).pack(side='right', padx=10)
        
        # Treeview for students
        tree_frame = ttk.Frame(view_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Email', 'Phone', 'Course', 'Grade', 'Date', 'Address'), 
                                show='headings', yscrollcommand=scrollbar.set)
        
        # Define headings
        columns = [('ID', 50), ('Name', 120), ('Email', 150), ('Phone', 100), 
                  ('Course', 120), ('Grade', 80), ('Date', 100), ('Address', 200)]
        
        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Load initial data
        self.load_students()
    
    def create_search_tab(self, notebook):
        """Create Search Student tab"""
        search_frame = ttk.Frame(notebook)
        notebook.add(search_frame, text="Search Student")
        
        # Title
        ttk.Label(search_frame, text="Search Student", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Search options
        search_option_frame = ttk.Frame(search_frame)
        search_option_frame.pack(pady=10)
        
        self.search_var = tk.StringVar(value="name")
        ttk.Radiobutton(search_option_frame, text="Search by Name", variable=self.search_var, value="name").pack(side='left', padx=10)
        ttk.Radiobutton(search_option_frame, text="Search by Email", variable=self.search_var, value="email").pack(side='left', padx=10)
        ttk.Radiobutton(search_option_frame, text="Search by ID", variable=self.search_var, value="id").pack(side='left', padx=10)
        
        # Search input
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(pady=10)
        
        ttk.Label(search_input_frame, text="Search:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_input_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search_input_frame, text="Search", command=self.search_student).pack(side='left', padx=5)
        
        # Results treeview
        results_frame = ttk.Frame(search_frame)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.search_tree = ttk.Treeview(results_frame, columns=('ID', 'Name', 'Email', 'Phone', 'Course', 'Grade'), 
                                       show='headings', yscrollcommand=scrollbar.set)
        
        columns = [('ID', 50), ('Name', 120), ('Email', 150), ('Phone', 100), ('Course', 120), ('Grade', 80)]
        for col, width in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=width)
        
        self.search_tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.search_tree.yview)
    
    def create_update_tab(self, notebook):
        """Create Update Student tab"""
        update_frame = ttk.Frame(notebook)
        notebook.add(update_frame, text="Update Student")
        
        # Title
        ttk.Label(update_frame, text="Update Student Information", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Student ID input
        id_frame = ttk.Frame(update_frame)
        id_frame.pack(pady=10)
        
        ttk.Label(id_frame, text="Student ID:").pack(side='left', padx=5)
        self.update_id_entry = ttk.Entry(id_frame, width=20)
        self.update_id_entry.pack(side='left', padx=5)
        ttk.Button(id_frame, text="Load Student", command=self.load_student_for_update).pack(side='left', padx=5)
        
        # Update form
        self.update_form_frame = ttk.LabelFrame(update_frame, text="Student Details")
        self.update_form_frame.pack(pady=10, padx=20, fill='x')
        
        # Name
        ttk.Label(self.update_form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.update_name_entry = ttk.Entry(self.update_form_frame, width=30)
        self.update_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Email
        ttk.Label(self.update_form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.update_email_entry = ttk.Entry(self.update_form_frame, width=30)
        self.update_email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Phone
        ttk.Label(self.update_form_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.update_phone_entry = ttk.Entry(self.update_form_frame, width=30)
        self.update_phone_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Course
        ttk.Label(self.update_form_frame, text="Course:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.update_course_entry = ttk.Entry(self.update_form_frame, width=30)
        self.update_course_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Grade
        ttk.Label(self.update_form_frame, text="Grade:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.update_grade_entry = ttk.Entry(self.update_form_frame, width=30)
        self.update_grade_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Address
        ttk.Label(self.update_form_frame, text="Address:").grid(row=5, column=0, padx=5, pady=5, sticky='ne')
        self.update_address_text = tk.Text(self.update_form_frame, width=30, height=4)
        self.update_address_text.grid(row=5, column=1, padx=5, pady=5)
        
        # Update button
        ttk.Button(update_frame, text="Update Student", command=self.update_student).pack(pady=10)
    
    def create_stats_tab(self, notebook):
        """Create Statistics tab"""
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")
        
        # Title and refresh button
        title_frame = ttk.Frame(stats_frame)
        title_frame.pack(fill='x', pady=10)
        
        ttk.Label(title_frame, text="System Statistics", font=('Arial', 14, 'bold')).pack(side='left', padx=10)
        ttk.Button(title_frame, text="Refresh", command=self.display_statistics).pack(side='right', padx=10)
        
        # Statistics display
        self.stats_text = tk.Text(stats_frame, width=80, height=20, state='disabled')
        self.stats_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Load initial statistics
        self.display_statistics()
    
    def add_student(self):
        """Add a new student to the database"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        course = self.course_entry.get().strip()
        grade = self.grade_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        
        if not name or not email:
            messagebox.showwarning("Input Error", "Name and Email are required!")
            return
        
        enrollment_date = datetime.datetime.now().date()
        
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO students (name, email, phone, course, grade, enrollment_date, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, email, phone, course, grade, enrollment_date, address)
            
            cursor.execute(query, values)
            self.connection.commit()
            messagebox.showinfo("Success", f"Student {name} added successfully!")
            
            # Clear form
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.course_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)
            self.address_text.delete("1.0", tk.END)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding student: {e}")
        finally:
            cursor.close()
    
    def load_students(self):
        """Load all students into the treeview"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add data to treeview
            for student in students:
                self.tree.insert('', 'end', values=student)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving students: {e}")
        finally:
            cursor.close()
    
    def search_student(self):
        """Search for a student"""
        search_type = self.search_var.get()
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term!")
            return
        
        try:
            cursor = self.connection.cursor()
            
            if search_type == "id":
                cursor.execute("SELECT student_id, name, email, phone, course, grade FROM students WHERE student_id = %s", (search_term,))
            elif search_type == "name":
                cursor.execute("SELECT student_id, name, email, phone, course, grade FROM students WHERE name LIKE %s", (f"%{search_term}%",))
            elif search_type == "email":
                cursor.execute("SELECT student_id, name, email, phone, course, grade FROM students WHERE email LIKE %s", (f"%{search_term}%",))
            
            students = cursor.fetchall()
            
            # Clear existing data
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)
            
            if not students:
                messagebox.showinfo("Search Results", "No students found matching your criteria.")
                return
            
            # Add results to treeview
            for student in students:
                self.search_tree.insert('', 'end', values=student)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error searching students: {e}")
        finally:
            cursor.close()
    
    def load_student_for_update(self):
        """Load student data for updating"""
        student_id = self.update_id_entry.get().strip()
        
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID!")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
            
            if not student:
                messagebox.showwarning("Not Found", "Student not found!")
                return
            
            # Fill the form with current data
            self.update_name_entry.delete(0, tk.END)
            self.update_name_entry.insert(0, student[1])
            
            self.update_email_entry.delete(0, tk.END)
            self.update_email_entry.insert(0, student[2])
            
            self.update_phone_entry.delete(0, tk.END)
            self.update_phone_entry.insert(0, student[3] or "")
            
            self.update_course_entry.delete(0, tk.END)
            self.update_course_entry.insert(0, student[4] or "")
            
            self.update_grade_entry.delete(0, tk.END)
            self.update_grade_entry.insert(0, student[5] or "")
            
            self.update_address_text.delete("1.0", tk.END)
            self.update_address_text.insert("1.0", student[7] or "")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading student: {e}")
        finally:
            cursor.close()
    
    def update_student(self):
        """Update student information"""
        student_id = self.update_id_entry.get().strip()
        
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID!")
            return
        
        name = self.update_name_entry.get().strip()
        email = self.update_email_entry.get().strip()
        phone = self.update_phone_entry.get().strip()
        course = self.update_course_entry.get().strip()
        grade = self.update_grade_entry.get().strip()
        address = self.update_address_text.get("1.0", tk.END).strip()
        
        if not name or not email:
            messagebox.showwarning("Input Error", "Name and Email are required!")
            return
        
        try:
            cursor = self.connection.cursor()
            query = """
            UPDATE students 
            SET name = %s, email = %s, phone = %s, course = %s, grade = %s, address = %s
            WHERE student_id = %s
            """
            values = (name, email, phone, course, grade, address, student_id)
            
            cursor.execute(query, values)
            self.connection.commit()
            messagebox.showinfo("Success", "Student information updated successfully!")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating student: {e}")
        finally:
            cursor.close()
    
    def display_statistics(self):
        """Display basic statistics"""
        try:
            cursor = self.connection.cursor()
            
            # Total students
            cursor.execute("SELECT COUNT(*) FROM students")
            total_students = cursor.fetchone()[0]
            
            # Students by course
            cursor.execute("SELECT course, COUNT(*) FROM students WHERE course IS NOT NULL GROUP BY course")
            courses = cursor.fetchall()
            
            # Students by grade
            cursor.execute("SELECT grade, COUNT(*) FROM students WHERE grade IS NOT NULL GROUP BY grade")
            grades = cursor.fetchall()
            
            # Enable text widget for editing
            self.stats_text.config(state='normal')
            self.stats_text.delete('1.0', tk.END)
            
            # Insert statistics
            self.stats_text.insert(tk.END, f"Total Students: {total_students}\n\n")
            
            self.stats_text.insert(tk.END, "Students by Course:\n")
            for course, count in courses:
                self.stats_text.insert(tk.END, f"  {course}: {count}\n")
            
            self.stats_text.insert(tk.END, "\nStudents by Grade:\n")
            for grade, count in grades:
                self.stats_text.insert(tk.END, f"  {grade}: {count}\n")
            
            # Disable text widget
            self.stats_text.config(state='disabled')
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving statistics: {e}")
        finally:
            cursor.close()
    
    def on_closing(self):
        """Handle window closing"""
        self.close_connection()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Main program
if __name__ == "__main__":
    system = StudentManagementSystem()
    system.run()