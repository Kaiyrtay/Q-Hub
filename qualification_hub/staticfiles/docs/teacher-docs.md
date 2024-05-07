# Teacher Management Application

The Teacher Management Application is part of a Django-based project designed to manage teachers within an educational institution. It provides functionality for creating, updating, viewing, and deleting teacher records, along with displaying detailed information about individual teachers.

## Purpose

The primary purpose of the Teacher Management Application is to offer a structured system for managing teachers and their associated user accounts. It supports CRUD operations (Create, Read, Update, Delete) for managing teacher records and enforces role-based permissions to ensure secure access control.

## Key Features

- **Teacher Model**: Represents teachers in the system. It includes attributes like `user`, `department`, `role`, `hire_date`, `middle_name`, `phone_number`, `contact_email`, `subject_taught`, and `room_number`. The `Teacher` model has a one-to-one relationship with a `User` and a foreign key to a `Department`.

- **Role-Based Permissions**: The app uses mixins like `ManagerGroupRequiredMixin` to control access based on user roles, ensuring only authorized users can create or update teacher records.

- **CRUD Operations**: The app supports CRUD operations for managing teachers, using Django's generic class-based views. It includes creating new teachers, updating existing ones, and deleting teacher records along with associated user accounts.

- **Secure Deletion**: The `TeacherDeleteView` deletes both the `Teacher` record and the associated `User`, ensuring comprehensive clean-up. This operation requires manager-level permissions for added security.

## Structure

The Teacher Management Application consists of several key components:

- **Models**: The `Teacher` model defines the structure of teacher records, with attributes like `role`, `hire_date`, and `subject_taught`. It has relationships with the `User` and `Department` models.

- **Views**: The views manage interactions with the `Teacher` model, providing operations like listing, creating, updating, and deleting teachers. Role-based permissions are enforced through mixins like `ManagerGroupRequiredMixin`.

- **URLs**: The URL configuration maps views to specific endpoints, allowing users to access the app's functionality. Reverse_lazy is used to handle URL redirections after certain operations.

- **Templates**: The app includes templates for listing teachers, displaying detailed information, and managing form-based operations. These templates are customizable and visually consistent with the broader project.

## Dependencies

The Teacher Management Application relies on:

- **Django Framework**: The core framework for building web applications.
- **Django Auth Models**: Used for user-related operations, particularly for managing the associated `User` with each teacher.
- **Department Model**: Represents the department to which a teacher belongs.

## Contributing

Contributions are welcome! If you have suggestions for improvement or encounter issues, please create a pull request or open an issue in the project's GitHub repository.

## License

This project is licensed under the MIT License, allowing free use, modification, and distribution.

## Contact

For further information or assistance, contact Kaiyrtay at [kaiyrtaygabbassov@gmail.com](mailto:kaiyrtaygabbassov@gmail.com).
