# Manager Management Application
The Manager Management Application is part of a Django-based project designed to manage department managers within an educational institution. It allows for creating, updating, viewing, and deleting manager instances, as well as displaying detailed information about each manager and their associated user account.

## Purpose
The primary purpose of the Manager Management Application is to provide a structured system for managing department managers. It supports CRUD operations (Create, Read, Update, Delete) for manager management, with role-based permissions to ensure that only authorized users can perform specific actions.

## Key Features
- **Manager Model**: Represents department managers in the system. Key attributes include `user`, `department`, `role`, `appointed_date`, `middle_name`, `phone_number`, and `contact_email`. The `Manager` model has a one-to-one relationship with a `User` and belongs to a `Department`.

- **Role-Based Permissions**: The application uses mixins to control access based on user roles. `StaffRequiredMixin` ensures that only staff-level users can create or update managers, while `OwnerOrStaffRequiredMixin` restricts certain operations to either the owner or staff members.

- **CRUD Operations**: The app supports CRUD operations for managing managers, using Django's generic class-based views. This includes creating new manager instances, updating existing ones, and deleting managers.

- **Manager Relationships**: Managers are linked to departments through a foreign key, establishing the department association. The app provides detailed views that offer additional context, such as related user information.

- **Secure Deletion**: The deletion of a manager also deletes the associated `User`, ensuring a comprehensive clean-up. This operation requires staff-level permissions for added security.

## Structure
The Manager Management Application consists of several components:

- **Models**: The `Manager` model represents department managers. It uses field types like `OneToOneField`, `ForeignKey`, and `CharField`.

- **Views**: The views manage interactions with the `Manager` model, allowing users to create, update, list, and delete managers. Role-based permissions are enforced through mixins.

- **URLs**: The URL configuration maps the views to specific endpoints, providing access to the app's functionality. It uses Django's reverse_lazy for URL management and redirects after specific operations.

- **Templates**: The app includes templates for listing managers, displaying detailed information, and managing form-based operations. These templates are customizable and designed to be visually consistent with the broader project.

## Dependencies
The Manager Management Application relies on:

- **Django Framework**: The core framework for building web applications.
- **Django Auth Models**: Used for user-related operations, particularly for managing user information associated with managers.
- **Departments Module**: Establishes relationships between managers and their respective departments.
- **Core Mixins**: Custom mixins like `StaffRequiredMixin` and `OwnerOrStaffRequiredMixin` for permission control and access checks.

## Contributing
Contributions are welcome! If you have suggestions for improvement or find any issues, please create a pull request or open an issue in the project's GitHub repository.

## License
This project is licensed under the MIT License, allowing free use, modification, and distribution.

## Contact
For further information or assistance, contact Kaiyrtay at [kaiyrtaygabbassov@gmail.com](mailto:kaiyrtaygabbassov@gmail.com).
