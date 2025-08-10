import csv  #Imports CSV module to read and write employees CSV file
import os   #Imports OS module for interacting with the operating system (e.g., CSV file path, file checks)

class EmployeeManager:
    #class variables or class attributes to be used in the class in all methods 
    file_name = "employees.csv"
    employee_fields = ["ID", "Name", "Position", "Salary", "Email"]

    def __init__(self): # Initialize the EmployeeManager class
        # Create CSV file with headers' names (ID, Name, Position, Salary, Email) of emlopyees
        if not os.path.exists(self.file_name):
            with open(self.file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.employee_fields)
    
    # One Method to handle all employee_fields Validation (ID, Name, Position, Salary, Email) for adding or updating an employee and return error messages if any validation fails
    def validate_field(self, field_name, value):
        if field_name == "ID":
            if not value.isdigit(): # Check if Employee ID is a number
                return "Employee ID must be a number."
            if self.employee_exists(value): # Check if Employee ID already exists
                return "Employee with this ID already exists."

        elif field_name == "Name":
            if not value.strip(): # Check if Employee Name is not empty
                return "Name cannot be empty."
            if not value.replace(" ", "").isalpha(): # Check if Employee Name contains only letters
                return "Name must contain only letters."

        elif field_name == "Position": 
            if not value.strip(): # Check if Employee Position is not empty
                return "Position cannot be empty."

        elif field_name == "Salary":
            try:
                salary = float(value) # Check if Employee Salary is a number
                if salary <= 0: # Check if Employee Salary is greater than zero
                    return "Salary must be greater than zero."
            except ValueError: # If conversion to float fails, return error
                return "Salary must be a number."

        elif field_name == "Email":
            if "@" not in value or "." not in value: # Check if Employee Email contains '@' and '.'
                return "Invalid email format."

        return None  # No error, validation passed
    
    #A Method to check if Employee ID already exists in the CSV file
    def employee_exists(self, employee_id): 
        with open(self.file_name, mode="r", newline="") as file: # Open CSV file in read mode
            reader = csv.DictReader(file) # Create a reader object
            return any(row["ID"] == employee_id for row in reader) # Check if any row has the same Employee ID

    #A Method to add a new employee to the CSV file
    def add_employee(self):
        new_employee = {}
        for field in self.employee_fields: # Loop through each field to get user input
            while True: # Ask for input until valid input is provided
                value = input(f"Enter {field}: ") # Get user input for each field
                error = self.validate_field(field, value) # Validate the field
                if error:
                    print(f"{error}") # If validation fails, print error message and ask for input again
                else:
                    new_employee[field] = value # If validation passes, add the field to the new employee dictionary
                    break

        with open(self.file_name, mode="a", newline="") as file: # Open CSV file in append mode
            writer = csv.DictWriter(file, fieldnames=self.employee_fields) # Create a writer object with employee employee_fields
            writer.writerow(new_employee) # Write the new employee data to the CSV file
        print("Employee added successfully!")

    # A Method to view all employees in the CSV file
    def view_employees(self):
        with open(self.file_name, mode="r", newline="") as file: # Open CSV file in read mode
            reader = csv.DictReader(file) # Create a reader object
            employees = list(reader) # Convert reader to a list of dictionaries

        if not employees: # Check if there are no employees in the list
            print("No employees found.") 
        else: # Print the list of employees
            print("\n--- Employees List ---")
            for emp in employees: # Loop through each employee and print their details
                print(", ".join([f"{k}: {v}" for k, v in emp.items()]))

    # A Method to search for an employee by ID
    def search_employee(self):
        employee_id = input("Enter Employee ID to search: ") # Get user input for Employee ID
        with open(self.file_name, mode="r", newline="") as file: # Open CSV file in read mode
            reader = csv.DictReader(file)
            for emp in reader: # Loop through each employee in the CSV file
                if emp["ID"] == employee_id: # Check if Employee ID matches the input
                    print("\n--- Employee Found ---")
                    for k, v in emp.items(): # Print the employee's details
                        print(f"{k}: {v}")
                    return
        print("Employee not found.") # If no employee is found, print a message

    # A Method to update an existing employee's details
    def update_employee(self):
        employee_id = input("Enter Employee ID to update: ") # Get user input for Employee ID
        employees = [] # Initialize an empty list to store employees
        found = False # Flag to check if employee is found

        with open(self.file_name, mode="r", newline="") as file: # Open CSV file in read mode
            reader = csv.DictReader(file) # Create a reader object
            employees = list(reader) # Convert reader to a list of dictionaries

        for emp in employees: # Loop through each employee in the list
            if emp["ID"] == employee_id: # Check if Employee ID matches the input
                found = True # Set the flag to True
                print("Enter new details (leave blank to keep current value):") # Prompt user to enter new details
                for field in self.employee_fields[1:]:  # Skip ID field for update
                    new_value = input(f"{field} ({emp[field]}): ") # If user input is empty, keep the current value
                    if new_value.strip(): # Validate the new value for the field
                        error = self.validate_field(field, new_value) # If validation fails, print error message
                        if error:
                            print(f"{error} - keeping old value.") # If validation fails, keep the old value
                        else:
                            emp[field] = new_value # Update the employee's field with the new value
                break

        if not found:
            print("Employee with this ID is not found.") # If no employee is found, print a message that employee is not found
            return

        with open(self.file_name, mode="w", newline="") as file: # Open CSV file in write mode
            writer = csv.DictWriter(file, fieldnames=self.employee_fields) # Create a writer object with employee employee_fields
            writer.writeheader() # Write the header row
            writer.writerows(employees) # Write the updated employee data to the CSV file
        print("Employee updated successfully.") # Print a success message that employee is updated

    # A Method to delete an employee by ID
    def delete_employee(self):
        employee_id = input("Enter Employee ID to delete: ") # Get user input for Employee ID
        with open(self.file_name, mode="r", newline="") as file: # Open CSV file in read mode
            reader = csv.DictReader(file) # Create a reader object
            employees = [emp for emp in reader if emp["ID"] != employee_id] # Create a list of employees excluding the one to be deleted

        with open(self.file_name, mode="w", newline="") as file: # Open CSV file in write mode
            writer = csv.DictWriter(file, fieldnames=self.employee_fields) # Create a writer object with employee employee_fields
            writer.writeheader() # Write the header row
            writer.writerows(employees) # Write the updated employee data to the CSV file

        print("Employee deleted successfully.")


employee_management_system = EmployeeManager() # Initialize the EmployeeManager instance for object employee_management_system

while True: # Main loop for the Employee Management System to keep running until the user choose 6 to exit
    print("\n**************************************")
    print("--- Employee Management System Menu---")
    print("**************************************")
    print("1. Add Employee")
    print("2. View All Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Exit")
    print("**************************************")
            
    choice = input("Choose an option (1-6): ")
    if choice == "1":
        employee_management_system.add_employee()
    elif choice == "2":
        employee_management_system.view_employees()
    elif choice == "3":
        employee_management_system.search_employee()
    elif choice == "4":
        employee_management_system.update_employee()
    elif choice == "5":
        employee_management_system.delete_employee()
    elif choice == "6":
        print("Exiting The Program...\nGood Bye!")
        break
    else:
        print("Invalid choice. Please try again with an option (1-6).")  