# Student Management Application

The Student Management Application is part of a Django-based project designed to manage students within an educational institution. It provides functionalities for creating, updating, viewing, and deleting student records, along with displaying detailed information about individual students.

## Purpose

The primary purpose of the Student Management Application is to offer a structured system for managing students and their associated user accounts. It supports CRUD operations (Create, Read, Update, Delete) for student management, with role-based permissions ensuring secure access control.

## Key Features

- **Student Model**: Represents students in the system. Key attributes include `user`, `department`, `role`, `enrollment_date`, `graduation_date`, `middle_name`, `phone_number`, `contact_email`, and `major`. The `Student` model has a one-to-one relationship with a `User` and belongs to a `Department`.

- **Role-Based Permissions**: The app uses mixins like `ManagerGroupRequiredMixin` to control access based on user roles, ensuring that only authorized users can create or update student records.

- **CRUD Operations**: The app supports CRUD operations for managing students, using Django's generic class-based views. This includes creating new students, updating existing ones, and deleting student records along with associated user accounts.

- **Secure Deletion**: The `StudentDeleteView` deletes both the `Student` record and the associated `User`, ensuring comprehensive clean-up. This operation requires manager-level permissions for added security.

## Structure

The Student Management Application consists of several key components:

- **Models**: The `Student` model defines the structure of student records. It uses field types like `OneToOneField`, `ForeignKey`, and `CharField` to represent core attributes and establish relationships.

- **Views**: The views manage interactions with the `Student` model, allowing users to create, update, list, and delete students. Role-based permissions are enforced through mixins like `ManagerGroupRequiredMixin`.

- **URLs**: The URL configuration maps views to specific endpoints, allowing users to access the app's functionality. Reverse_lazy is used to handle URL redirections after specific operations.

- **Templates**: The app includes templates for listing students, displaying detailed information, and managing form-based operations. These templates are customizable and designed to maintain visual consistency with the broader project.

## Dependencies

The Student Management Application relies on:

- **Django Framework**: The core framework for building web applications.
- **Django Auth Models**: Used for user-related operations, particularly for managing the associated `User` with each student.
- **Department Model**: Represents the department to which a student belongs.
- **Core Mixins**: Custom mixins for enforcing role-based permissions and access control.

## Contributing

Contributions are welcome! If you have suggestions for improvement or encounter issues, please create a pull request or open an issue in the project's GitHub repository.

## License

This project is licensed under the MIT License, allowing free use, modification, and distribution.

## Contact

For further information or assistance, contact Kaiyrtay at [kaiyrtaygabbassov@gmail.com](mailto:kaiyrtaygabbassov
