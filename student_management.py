import json
import csv
import os
from datetime import datetime
from typing import List, Optional, Dict


class Student:
    """Represents a student record."""
    
    def __init__(self, student_id: str, name: str, email: str, phone: str, gpa: float):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.phone = phone
        self.gpa = gpa
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self) -> Dict:
        """Convert student object to dictionary."""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'gpa': self.gpa,
            'enrollment_date': self.enrollment_date
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Student':
        """Create student object from dictionary."""
        student = Student(
            data['student_id'],
            data['name'],
            data['email'],
            data['phone'],
            data['gpa']
        )
        student.enrollment_date = data.get('enrollment_date', student.enrollment_date)
        return student
    
    def __str__(self) -> str:
        return (f"ID: {self.student_id} | Name: {self.name} | Email: {self.email} | "
                f"Phone: {self.phone} | GPA: {self.gpa} | Enrolled: {self.enrollment_date}")


class StudentManagementSystem:
    """Manages student records with CRUD operations."""
    
    def __init__(self, filename: str = 'students.json'):
        self.filename = filename
        self.students: List[Student] = []
        self.load_from_file()
    
    def load_from_file(self) -> None:
        """Load student records from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.students = [Student.from_dict(record) for record in data]
                print(f"✓ Loaded {len(self.students)} student records from {self.filename}")
            except json.JSONDecodeError:
                print(f"✗ Error reading {self.filename}. Starting with empty records.")
                self.students = []
        else:
            print(f"✓ Creating new student database: {self.filename}")
            self.students = []
    
    def save_to_file(self) -> None:
        """Save student records to JSON file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump([student.to_dict() for student in self.students], file, indent=2)
            print(f"✓ Records saved successfully to {self.filename}")
        except IOError as e:
            print(f"✗ Error saving to file: {e}")
    
    def export_to_csv(self, csv_filename: str = 'students.csv') -> None:
        """Export student records to CSV file."""
        if not self.students:
            print("✗ No students to export.")
            return
        
        try:
            with open(csv_filename, 'w', newline='') as file:
                fieldnames = ['student_id', 'name', 'email', 'phone', 'gpa', 'enrollment_date']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students:
                    writer.writerow(student.to_dict())
            print(f"✓ Records exported successfully to {csv_filename}")
        except IOError as e:
            print(f"✗ Error exporting to CSV: {e}")
    
    def add_student(self, student_id: str, name: str, email: str, phone: str, gpa: float) -> bool:
        """Add a new student record."""
        # Validate student ID uniqueness
        if self._student_id_exists(student_id):
            print(f"✗ Student ID {student_id} already exists.")
            return False
        
        # Validate inputs
        if not self._validate_inputs(name, email, phone, gpa):
            return False
        
        student = Student(student_id, name, email, phone, gpa)
        self.students.append(student)
        self.save_to_file()
        print(f"✓ Student '{name}' added successfully!")
        return True
    
    def view_all_students(self) -> None:
        """Display all student records."""
        if not self.students:
            print("✗ No students in the system.")
            return
        
        print("\n" + "="*100)
        print(f"{'STUDENT RECORDS':<100}")
        print("="*100)
        for idx, student in enumerate(self.students, 1):
            print(f"{idx}. {student}")
        print("="*100 + "\n")
    
    def search_student(self, query: str, search_type: str = 'id') -> List[Student]:
        """Search for students by ID or name."""
        results = []
        
        if search_type.lower() == 'id':
            results = [s for s in self.students if s.student_id.lower() == query.lower()]
        elif search_type.lower() == 'name':
            results = [s for s in self.students if query.lower() in s.name.lower()]
        
        if results:
            print("\n" + "="*100)
            print(f"{'SEARCH RESULTS':<100}")
            print("="*100)
            for idx, student in enumerate(results, 1):
                print(f"{idx}. {student}")
            print("="*100 + "\n")
        else:
            print(f"✗ No students found matching '{query}'.")
        
        return results
    
    def update_student(self, student_id: str) -> bool:
        """Update student information."""
        student = self._find_student_by_id(student_id)
        
        if not student:
            print(f"✗ Student with ID {student_id} not found.")
            return False
        
        print(f"\nCurrent Details: {student}")
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Email")
        print("3. Phone")
        print("4. GPA")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            new_name = input("Enter new name: ").strip()
            if new_name:
                student.name = new_name
                print(f"✓ Name updated to '{new_name}'")
            else:
                print("✗ Invalid name.")
                return False
        
        elif choice == '2':
            new_email = input("Enter new email: ").strip()
            if self._validate_email(new_email):
                student.email = new_email
                print(f"✓ Email updated to '{new_email}'")
            else:
                print("✗ Invalid email.")
                return False
        
        elif choice == '3':
            new_phone = input("Enter new phone: ").strip()
            if self._validate_phone(new_phone):
                student.phone = new_phone
                print(f"✓ Phone updated to '{new_phone}'")
            else:
                print("✗ Invalid phone number.")
                return False
        
        elif choice == '4':
            try:
                new_gpa = float(input("Enter new GPA (0-4.0): ").strip())
                if 0 <= new_gpa <= 4.0:
                    student.gpa = new_gpa
                    print(f"✓ GPA updated to {new_gpa}")
                else:
                    print("✗ GPA must be between 0 and 4.0")
                    return False
            except ValueError:
                print("✗ Invalid GPA format.")
                return False
        
        else:
            print("✗ Invalid choice.")
            return False
        
        self.save_to_file()
        return True
    
    def delete_student(self, student_id: str) -> bool:
        """Delete a student record."""
        student = self._find_student_by_id(student_id)
        
        if not student:
            print(f"✗ Student with ID {student_id} not found.")
            return False
        
        print(f"\nDeleting: {student}")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            self.students.remove(student)
            self.save_to_file()
            print(f"✓ Student '{student.name}' deleted successfully!")
            return True
        else:
            print("✗ Delete cancelled.")
            return False
    
    def get_statistics(self) -> None:
        """Display statistics about students."""
        if not self.students:
            print("✗ No students in the system.")
            return
        
        total_students = len(self.students)
        avg_gpa = sum(s.gpa for s in self.students) / total_students
        highest_gpa = max(self.students, key=lambda s: s.gpa)
        lowest_gpa = min(self.students, key=lambda s: s.gpa)
        
        print("\n" + "="*50)
        print(f"{'STATISTICS':<50}")
        print("="*50)
        print(f"Total Students: {total_students}")
        print(f"Average GPA: {avg_gpa:.2f}")
        print(f"Highest GPA: {highest_gpa.name} ({highest_gpa.gpa})")
        print(f"Lowest GPA: {lowest_gpa.name} ({lowest_gpa.gpa})")
        print("="*50 + "\n")
    
    def _find_student_by_id(self, student_id: str) -> Optional[Student]:
        """Find a student by ID."""
        for student in self.students:
            if student.student_id.lower() == student_id.lower():
                return student
        return None
    
    def _student_id_exists(self, student_id: str) -> bool:
        """Check if student ID already exists."""
        return self._find_student_by_id(student_id) is not None
    
    def _validate_inputs(self, name: str, email: str, phone: str, gpa: float) -> bool:
        """Validate all input fields."""
        if not name or len(name.strip()) < 2:
            print("✗ Name must be at least 2 characters long.")
            return False
        
        if not self._validate_email(email):
            return False
        
        if not self._validate_phone(phone):
            return False
        
        try:
            gpa = float(gpa)
            if not (0 <= gpa <= 4.0):
                print("✗ GPA must be between 0 and 4.0")
                return False
        except ValueError:
            print("✗ GPA must be a valid number.")
            return False
        
        return True
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format."""
        if '@' not in email or '.' not in email:
            print("✗ Invalid email format.")
            return False
        return True
    
    @staticmethod
    def _validate_phone(phone: str) -> bool:
        """Validate phone number format."""
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 10:
            print("✗ Phone number must have at least 10 digits.")
            return False
        return True


def main():
    """Main function to run the application."""
    system = StudentManagementSystem()
    
    while True:
        print("\n" + "="*50)
        print(f"{'STUDENT MANAGEMENT SYSTEM':<50}")
        print("="*50)
        print("1. Add a new student")
        print("2. View all students")
        print("3. Search for a student")
        print("4. Update student information")
        print("5. Delete a student")
        print("6. View statistics")
        print("7. Export to CSV")
        print("8. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            print("\n--- Add New Student ---")
            student_id = input("Enter Student ID: ").strip()
            name = input("Enter Name: ").strip()
            email = input("Enter Email: ").strip()
            phone = input("Enter Phone: ").strip()
            try:
                gpa = float(input("Enter GPA (0-4.0): ").strip())
                system.add_student(student_id, name, email, phone, gpa)
            except ValueError:
                print("✗ Invalid GPA format.")
        
        elif choice == '2':
            system.view_all_students()
        
        elif choice == '3':
            print("\n--- Search for a Student ---")
            print("1. Search by ID")
            print("2. Search by Name")
            search_choice = input("Enter your choice (1-2): ").strip()
            
            if search_choice == '1':
                student_id = input("Enter Student ID: ").strip()
                system.search_student(student_id, 'id')
            elif search_choice == '2':
                name = input("Enter Student Name: ").strip()
                system.search_student(name, 'name')
            else:
                print("✗ Invalid choice.")
        
        elif choice == '4':
            print("\n--- Update Student ---")
            student_id = input("Enter Student ID: ").strip()
            system.update_student(student_id)
        
        elif choice == '5':
            print("\n--- Delete Student ---")
            student_id = input("Enter Student ID: ").strip()
            system.delete_student(student_id)
        
        elif choice == '6':
            system.get_statistics()
        
        elif choice == '7':
            csv_filename = input("Enter CSV filename (default: students.csv): ").strip() or 'students.csv'
            system.export_to_csv(csv_filename)
        
        elif choice == '8':
            print("\n✓ Thank you for using Student Management System!")
            break
        
        else:
            print("✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
