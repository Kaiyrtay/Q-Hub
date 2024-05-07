# Core Views and Mixins for Django Project

This module contains various views and mixins for a Django-based project. It encompasses user authentication (login, logout, and registration), search logic across multiple models, and custom permission mixins for role-based access control. Additionally, middleware is used to enforce permissions on specific routes.

## Key Features

### User Authentication

- **Login and Logout Views**: Handles user authentication, with support for login by username or email. The `login_view` authenticates users, while the `logout_view` logs them out and redirects to the home page.

- **User Registration**: The `RegisterView` allows user registration with different roles (e.g., student, teacher). It creates the appropriate user-related models upon successful registration.

### Search Logic

- **Search View**: The `search_view` implements search logic to find users, certificates, departments, and other entities based on a query parameter. It includes custom search handlers for specific cases, like searching by certificate number, department name, or user identifier.

### Custom Permission Mixins

- **SuperuserRequiredMixin**: Ensures that only superusers can access the associated view. Raises a `PermissionDenied` exception if the user does not meet the requirements.

- **StaffRequiredMixin**: Requires the user to be a staff member to access the view. Raises a `PermissionDenied` exception if not a staff member.

- **ManagerGroupRequiredMixin**: Requires the user to belong to the "Managers" group for access.

- **TeacherOrStudentRequiredMixin**: Grants access to users who are in the "Teachers" or "Students" group.

- **OwnerOrStaffRequiredMixin**: Allows access to either the owner of the object or a staff member.

- **ManagerOrOwnerRequiredMixin**: Grants access if the user is in the "Managers" group or is the owner of the object.

- **ManagerOrOwnerForCertificateRequiredMixin**: Ensures that the user is either in the "Managers" group or is the owner of the certificate (student_owner or teacher_owner).

### Middleware

- **StaffOnlyMiddleware**: Middleware that restricts access to specific URLs (like `/rosetta/`) to staff members only. Returns an `HttpResponseForbidden` if the user is not a staff member.

## Dependencies

The Core Views and Mixins module relies on:

- **Django Framework**: For core web framework functionality, including authentication, HTTP handling, and database operations.
- **Django Auth Models**: For user-related operations, particularly managing user groups and permissions.
- **Various Django Models**: To implement search logic across different apps (e.g., `Teacher`, `Student`, `Manager`, `Department`, `Faculty`, `Certificate`).
- **Core Mixins**: Custom mixins to enforce role-based permissions and access control.

## Contributing

Contributions are welcome! If you have suggestions for improvement or encounter issues, please create a pull request or open an issue in the project's GitHub repository.

## License

This project is licensed under the MIT License, allowing free use, modification, and distribution.

## Contact

For further information or assistance, contact Kaiyrtay at [kaiyrtaygabbassov@gmail.com](mailto:kaiyrtaygabbassov@gmail.com).
