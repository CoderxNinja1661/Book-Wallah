#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <limits>

using namespace std;

class Student {
private:
    int rollNo;
    string name;
    string className;
    int year;
    float totalMarks;
    char grade;

public:
    // Constructor
    Student() : rollNo(0), year(0), totalMarks(0.0), grade(' ') {}
    
    // Get student data from user
    void getData() {
        cout << "\n--- Enter Student Details ---" << endl;
        
        // Roll Number input with validation
        cout << "Enter Roll Number: ";
        while (!(cin >> rollNo) || rollNo <= 0) {
            cout << "Invalid input! Enter positive integer: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
        
        cin.ignore(); // Clear input buffer
        
        // Name input
        cout << "Enter Name: ";
        getline(cin, name);
        
        // Class input
        cout << "Enter Class: ";
        getline(cin, className);
        
        // Year input with validation
        cout << "Enter Year: ";
        while (!(cin >> year) || year < 2000 || year > 2030) {
            cout << "Invalid year! Enter between 2000-2030: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
        
        // Marks input with validation
        cout << "Enter Total Marks (out of 500): ";
        while (!(cin >> totalMarks) || totalMarks < 0 || totalMarks > 500) {
            cout << "Invalid marks! Enter between 0-500: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
        
        calculateGrade();
    }
    
    // Display student data
    void showData() const {
        cout << left << setw(10) << rollNo 
             << setw(20) << name 
             << setw(15) << className 
             << setw(8) << year 
             << setw(12) << totalMarks 
             << setw(8) << grade << endl;
    }
    
    // Modify student data
    void modifyData() {
        cout << "\n--- Modify Student Details ---" << endl;
        cout << "Current Data:" << endl;
        showHeader();
        showData();
        
        cin.ignore();
        cout << "\nEnter New Name (press enter to keep current: " << name << "): ";
        string newName;
        getline(cin, newName);
        if (!newName.empty()) name = newName;
        
        cout << "Enter New Class (press enter to keep current: " << className << "): ";
        string newClass;
        getline(cin, newClass);
        if (!newClass.empty()) className = newClass;
        
        cout << "Enter New Year (press enter to keep current: " << year << "): ";
        string yearInput;
        getline(cin, yearInput);
        if (!yearInput.empty()) {
            try {
                year = stoi(yearInput);
            } catch (...) {
                cout << "Invalid year entered. Keeping current value." << endl;
            }
        }
        
        cout << "Enter New Total Marks (press enter to keep current: " << totalMarks << "): ";
        string marksInput;
        getline(cin, marksInput);
        if (!marksInput.empty()) {
            try {
                totalMarks = stof(marksInput);
                calculateGrade();
            } catch (...) {
                cout << "Invalid marks entered. Keeping current value." << endl;
            }
        }
        
        cout << "Student record updated successfully!" << endl;
    }
    
    // Calculate grade based on marks
    void calculateGrade() {
        float percentage = (totalMarks / 500) * 100;
        
        if (percentage >= 90) grade = 'A';
        else if (percentage >= 80) grade = 'B';
        else if (percentage >= 70) grade = 'C';
        else if (percentage >= 60) grade = 'D';
        else grade = 'F';
    }
    
    // Getters
    int getRollNo() const { return rollNo; }
    string getName() const { return name; }
    string getClassName() const { return className; }
    int getYear() const { return year; }
    float getTotalMarks() const { return totalMarks; }
    char getGrade() const { return grade; }
    
    // Static function to display table header
    static void showHeader() {
        cout << left << setw(10) << "Roll No" 
             << setw(20) << "Name" 
             << setw(15) << "Class" 
             << setw(8) << "Year" 
             << setw(12) << "Total Marks" 
             << setw(8) << "Grade" << endl;
        cout << string(75, '-') << endl;
    }
    
    // Write student data to file
    void writeToFile(ofstream &file) const {
        file << rollNo << "," << name << "," << className << "," 
             << year << "," << totalMarks << "," << grade << endl;
    }
    
    // Read student data from file
    bool readFromFile(ifstream &file) {
        string line;
        if (getline(file, line)) {
            size_t pos = 0;
            string token;
            vector<string> tokens;
            
            // Parse CSV line
            while ((pos = line.find(',')) != string::npos) {
                token = line.substr(0, pos);
                tokens.push_back(token);
                line.erase(0, pos + 1);
            }
            tokens.push_back(line);
            
            if (tokens.size() == 6) {
                rollNo = stoi(tokens[0]);
                name = tokens[1];
                className = tokens[2];
                year = stoi(tokens[3]);
                totalMarks = stof(tokens[4]);
                grade = tokens[5][0];
                return true;
            }
        }
        return false;
    }
};

class StudentManager {
private:
    vector<Student> students;
    const string filename = "students.txt";

public:
    // Display main menu
    void displayMenu() {
        cout << "\n========== STUDENT MANAGEMENT SYSTEM ==========" << endl;
        cout << "1. Add Student" << endl;
        cout << "2. Display All Students" << endl;
        cout << "3. Search Student" << endl;
        cout << "4. Modify Student" << endl;
        cout << "5. Delete Student" << endl;
        cout << "6. Save to File" << endl;
        cout << "7. Load from File" << endl;
        cout << "8. Exit" << endl;
        cout << "=============================================" << endl;
        cout << "Enter your choice (1-8): ";
    }
    
    // Add new student
    void addStudent() {
        Student newStudent;
        newStudent.getData();
        
        // Check if roll number already exists
        for (const auto& student : students) {
            if (student.getRollNo() == newStudent.getRollNo()) {
                cout << "Error: Student with Roll Number " << newStudent.getRollNo() << " already exists!" << endl;
                return;
            }
        }
        
        students.push_back(newStudent);
        cout << "\nStudent added successfully!" << endl;
    }
    
    // Display all students
    void displayAllStudents() {
        if (students.empty()) {
            cout << "\nNo students found in the database!" << endl;
            return;
        }
        
        cout << "\n========== ALL STUDENTS ==========" << endl;
        Student::showHeader();
        
        for (const auto &student : students) {
            student.showData();
        }
        
        cout << "\nTotal Students: " << students.size() << endl;
    }
    
    // Search for student
    void searchStudent() {
        if (students.empty()) {
            cout << "\nNo students to search!" << endl;
            return;
        }
        
        int choice;
        cout << "\n--- Search Student ---" << endl;
        cout << "1. Search by Roll Number" << endl;
        cout << "2. Search by Name" << endl;
        cout << "Enter your choice: ";
        cin >> choice;
        
        bool found = false;
        
        switch (choice) {
            case 1: {
                int rollNo;
                cout << "Enter Roll Number to search: ";
                cin >> rollNo;
                
                cout << "\nSearch Results:" << endl;
                Student::showHeader();
                
                for (const auto &student : students) {
                    if (student.getRollNo() == rollNo) {
                        student.showData();
                        found = true;
                        break;
                    }
                }
                break;
            }
                
            case 2: {
                string searchName;
                cout << "Enter Name to search: ";
                cin.ignore();
                getline(cin, searchName);
                
                cout << "\nSearch Results:" << endl;
                Student::showHeader();
                
                for (const auto &student : students) {
                    if (student.getName().find(searchName) != string::npos) {
                        student.showData();
                        found = true;
                    }
                }
                break;
            }
                
            default:
                cout << "Invalid choice!" << endl;
                return;
        }
        
        if (!found) {
            cout << "No student found matching the search criteria!" << endl;
        }
    }
    
    // Modify student record
    void modifyStudent() {
        if (students.empty()) {
            cout << "\nNo students to modify!" << endl;
            return;
        }
        
        int rollNo;
        cout << "Enter Roll Number of student to modify: ";
        cin >> rollNo;
        
        for (auto &student : students) {
            if (student.getRollNo() == rollNo) {
                student.modifyData();
                return;
            }
        }
        
        cout << "Student with Roll Number " << rollNo << " not found!" << endl;
    }
    
    // Delete student record
    void deleteStudent() {
        if (students.empty()) {
            cout << "\nNo students to delete!" << endl;
            return;
        }
        
        int rollNo;
        cout << "Enter Roll Number of student to delete: ";
        cin >> rollNo;
        
        for (auto it = students.begin(); it != students.end(); ++it) {
            if (it->getRollNo() == rollNo) {
                cout << "Deleting student: " << it->getName() << endl;
                students.erase(it);
                cout << "Student deleted successfully!" << endl;
                return;
            }
        }
        
        cout << "Student with Roll Number " << rollNo << " not found!" << endl;
    }
    
    // Save students to file
    void saveToFile() {
        ofstream file(filename);
        if (!file) {
            cout << "Error: Could not open file for writing!" << endl;
            return;
        }
        
        for (const auto &student : students) {
            student.writeToFile(file);
        }
        
        file.close();
        cout << "Data saved to file successfully! Total records: " << students.size() << endl;
    }
    
    // Load students from file
    void loadFromFile() {
        ifstream file(filename);
        if (!file) {
            cout << "No existing data file found. Starting with empty database." << endl;
            return;
        }
        
        students.clear(); // Clear current data
        Student student;
        int count = 0;
        
        while (student.readFromFile(file)) {
            students.push_back(student);
            count++;
        }
        
        file.close();
        cout << "Data loaded from file successfully! Loaded " << count << " records." << endl;
    }
    
    // Main application loop
    void run() {
        int choice;
        
        // Load existing data at startup
        loadFromFile();
        
        do {
            displayMenu();
            cin >> choice;
            
            switch (choice) {
                case 1: addStudent(); break;
                case 2: displayAllStudents(); break;
                case 3: searchStudent(); break;
                case 4: modifyStudent(); break;
                case 5: deleteStudent(); break;
                case 6: saveToFile(); break;
                case 7: loadFromFile(); break;
                case 8: 
                    cout << "Thank you for using Student Management System!" << endl;
                    break;
                default:
                    cout << "Invalid choice! Please try again." << endl;
            }
        } while (choice != 8);
    }
};

int main() {
    StudentManager manager;
    manager.run();
    return 0;
}