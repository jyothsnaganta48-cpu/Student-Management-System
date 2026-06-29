# Student-Management-System
The `student_management.py` file is a **complete command-line student records management system** with full CRUD (Create, Read, Update, Delete) capabilities. It manages student data in a structured, organized way with permanent storage.

### **Core Functionality**

Feature 

**Add Students** 
Create new student records with ID, name, email, phone, GPA, and automatic enrollment date
**View All Students** 
Display all records in a formatted table showing ID, name, email, phone, GPA, and enrollment date
**Search Students**
Find students by Student ID or by Name (partial matching supported)
**Update Information** 
Modify name, email, phone, or GPA for existing students with validation
**Delete Students** 
Remove student records (with confirmation to prevent accidental deletion)
**View Statistics**
See total student count, average GPA, highest GPA student, lowest GPA student
**Export to CSV** 
Save all records to a spreadsheet-compatible CSV file
**Auto-Save**
Records automatically save to `students.json` after each operation

### **How It Works**

User runs: python student_management.py <br>
    ↓ /
System loads existing students from students.json (if any) /
    ↓ /
Menu appears with 8 options /
    ↓ /
User selects action (add/view/search/update/delete/stats/export/exit) /
    ↓ /
System performs action with validation /
    ↓ /
Changes saved to students.json automatically /
    ↓ /
Repeat until user exits /

## **Run the application**
python student_management.py
