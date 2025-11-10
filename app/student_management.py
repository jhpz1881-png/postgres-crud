"""
Student Database Management System:
This Python application connects to a PostgreSQL database and performs CRUD operations on the "students" table.

Author: Siqi Huang
Course: COMP3005
Student Number: 101284265
"""

import psycopg2
from psycopg2 import Error
from datetime import datetime


class StudentDatabase:
    # Encapsulates all DB operations: connect/disconnect, list/add/update/delete students.

    def __init__(self, host="localhost", database="schooldb", user="postgres", password="your_password"):
        
        # Initialize connection parameters for the PostgreSQL database.
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        
        # Establish a connection to the PostgreSQL database.
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Successfully connected to the database.")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):

        # Close the database connection.
        # It is important to close the connection after operations are completed.
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def getAllStudents(self):

        # Retrieve and display all student records from the database.
        try:
            cursor = self.connection.cursor()

            # Retrieve all records ordered by student ID
            query = "SELECT * FROM students ORDER BY student_id;"
            cursor.execute(query)
            students = cursor.fetchall()

            # Display results in a formatted table
            print("\n" + "=" * 80)
            print("All Student Records")
            print("=" * 80)
            print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Enrollment Date'}")
            print("-" * 80)
            for student in students:
                print(f"{student[0]:<5} {student[1]:<15} {student[2]:<15} {student[3]:<30} {student[4]}")
            print("=" * 80)
            print(f"Total {len(students)} record(s)\n")

            cursor.close()
            return students

        except Error as e:
            print(f"Error retrieving students: {e}")
            return []

    def addStudent(self, first_name, last_name, email, enrollment_date):
        
        # Insert a new student record into the database.
        try:
            cursor = self.connection.cursor()

            # Use parameterized SQL to prevent SQL injection
            query = """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s) RETURNING student_id;
            """
            cursor.execute(query, (first_name, last_name, email, enrollment_date))
            student_id = cursor.fetchone()[0]

            # Commit the transaction
            self.connection.commit()

            print("\nSuccessfully added student:")
            print(f"  ID: {student_id}")
            print(f"  Name: {first_name} {last_name}")
            print(f"  Email: {email}")
            print(f"  Enrollment Date: {enrollment_date}\n")

            cursor.close()
            return True

        except Error as e:
            print(f"\nError adding student: {e}\n")
            self.connection.rollback()
            return False

    def updateStudentEmail(self, student_id, new_email):
        
        # Update the email address for a student identified by student_id.
        try:
            cursor = self.connection.cursor()

            # Check if the student exists before updating
            check_query = "SELECT first_name, last_name, email FROM students WHERE student_id = %s;"
            cursor.execute(check_query, (student_id,))
            student = cursor.fetchone()

            if not student:
                print(f"\nStudent with ID {student_id} not found.\n")
                cursor.close()
                return False

            old_email = student[2]

            # Perform the update
            update_query = "UPDATE students SET email = %s WHERE student_id = %s;"
            cursor.execute(update_query, (new_email, student_id))
            self.connection.commit()

            print("\nEmail updated successfully:")
            print(f"  Student: {student[0]} {student[1]} (ID: {student_id})")
            print(f"  Old Email: {old_email}")
            print(f"  New Email: {new_email}\n")

            cursor.close()
            return True

        except Error as e:
            print(f"\nError updating email: {e}\n")
            self.connection.rollback()
            return False

    def deleteStudent(self, student_id):
        
        # Delete a student record from the database by ID.
        try:
            cursor = self.connection.cursor()

            # Check if the student exists before deleting
            check_query = "SELECT first_name, last_name, email FROM students WHERE student_id = %s;"
            cursor.execute(check_query, (student_id,))
            student = cursor.fetchone()

            if not student:
                print(f"\nStudent with ID {student_id} not found.\n")
                cursor.close()
                return False

            # Delete the student record
            delete_query = "DELETE FROM students WHERE student_id = %s;"
            cursor.execute(delete_query, (student_id,))
            self.connection.commit()

            print("\nSuccessfully deleted student:")
            print(f"  ID: {student_id}")
            print(f"  Name: {student[0]} {student[1]}")
            print(f"  Email: {student[2]}\n")

            cursor.close()
            return True

        except Error as e:
            print(f"\nError deleting student: {e}\n")
            self.connection.rollback()
            return False


def display_menu():
    
    # Display the main menu for user interaction.
    print("\n" + "=" * 60)
    print("Student Database Management System")
    print("=" * 60)
    print("1. View All Students")
    print("2. Add New Student")
    print("3. Update Student Email")
    print("4. Delete Student")
    print("5. Exit")
    print("=" * 60)


def main():
    """
    Main function that runs the interactive command-line menu.
    Users can select one of the CRUD operations from the menu.
    """
    # Configure your PostgreSQL connection here
    db = StudentDatabase(
        host="localhost",
        database="schooldb",
        user="postgres",
        password="123456"
    )

    db.connect()

    # If connection fails, exit the program
    if not db.connection:
        print("Unable to connect to the database. Exiting.")
        return

    # Main interactive loop
    while True:
        display_menu()
        choice = input("\nSelect an option (1–5): ").strip()

        if choice == '1':
            db.getAllStudents()

        elif choice == '2':
            print("\nAdd New Student")
            print("-" * 40)
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            enrollment_date = input("Enrollment Date (YYYY-MM-DD): ").strip()

            if first_name and last_name and email and enrollment_date:
                db.addStudent(first_name, last_name, email, enrollment_date)
            else:
                print("\nAll fields are required.\n")

        elif choice == '3':
            print("\nUpdate Student Email")
            print("-" * 40)
            try:
                student_id = int(input("Student ID: ").strip())
                new_email = input("New Email: ").strip()
                if new_email:
                    db.updateStudentEmail(student_id, new_email)
                else:
                    print("\nEmail cannot be empty.\n")
            except ValueError:
                print("\nPlease enter a valid student ID.\n")

        elif choice == '4':
            print("\nDelete Student")
            print("-" * 40)
            try:
                student_id = int(input("Student ID: ").strip())
                confirm = input(f"Confirm delete student {student_id}? (y/n): ").strip().lower()
                if confirm == 'y':
                    db.deleteStudent(student_id)
                else:
                    print("\nOperation cancelled.\n")
            except ValueError:
                print("\nPlease enter a valid student ID.\n")

        elif choice == '5':
            print("\nThank you for using the system!")
            break

        else:
            print("\nInvalid choice. Please enter 1–5.\n")

    # Disconnect from the database before exiting
    db.disconnect()


if __name__ == "__main__":
    main()
