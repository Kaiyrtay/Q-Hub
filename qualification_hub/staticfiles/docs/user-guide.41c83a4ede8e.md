# Qualification Hub - User Guide

Welcome to Qualification Hub! This user guide is designed to help you understand how to use the system effectively. It covers the following topics:

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [System Requirements](#system-requirements)
   - [Installation](#installation)
3. [User Roles and Permissions](#user-roles-and-permissions)
4. [Certificate Management](#certificate-management)
   - [Creating a Certificate](#creating-a-certificate)
   - [Viewing Certificates](#viewing-certificates)
   - [Updating a Certificate](#updating-a-certificate)
   - [Deleting a Certificate](#deleting-a-certificate)
5. [Search Functionality](#search-functionality)
6. [Authentication and Authorization](#authentication-and-authorization)
7. [Troubleshooting](#troubleshooting)
8. [Contact Information](#contact-information)

## Introduction

Qualification Hub is a Django-based platform for managing and tracking educational qualifications, certificates, and related information. It supports various user roles, including teachers, students, managers, and administrators, providing tools for managing certificates and other functionalities.

## Getting Started

### System Requirements

To use Qualification Hub, ensure you have the following:

- A web browser (e.g., Chrome, Firefox, Safari, Edge)
- A stable internet connection

### Installation

If you are setting up Qualification Hub locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Kaiyrtay/Thesis-project.git
   ```

2. Navigate to the project directory and install dependencies:

   ```bash
   cd qualification-hub
   pip install -r requirements.txt
   ```

3. Run migrations to set up the database:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run custom code to create group and assign permissions:
   ```bash
   python manage.py create_groups_and_permissions
   ```

## User Roles and Permissions

Qualification Hub has different user roles with varying levels of permissions:

- Owner: Superuser with full access to the system.
- Admin: Staff member with access to managers, departments, and faculties.
- Manager: Can manage teachers and students.
- Teacher: Can manage certificates.
- Student: Can access certificates.
- Guest: Non-authenticated users with read-only access to public information.
  Each role has specific permissions, ensuring a secure and organized system.

## Certificate Management

Qualification Hub allows you to create, view, update, and delete certificates.

### Creating a Certificate

- Navigate to the "Create Certificate" page.
- Fill in the required fields, including certificate name, organization, and certificate number.
- Click "Submit" to create the certificate.

### Viewing Certificates

- Navigate to the "Certificates" page to view a list of certificates.
- Click on a certificate to view its details.

### Updating a Certificate

- Navigate to the certificate detail page.
- Click "Edit" or "Update" to modify certificate information.
- Make the necessary changes and click "Submit" to save.

### Deleting a Certificate

- Navigate to the certificate detail page.
- Click "Delete" and confirm to remove the certificate from the system.

## Search Functionality

You can search for various items in Qualification Hub, including certificates, users, and departments.

- Use the search bar to enter a query.
- The system will display relevant results based on your query.

## Authentication and Authorization

Qualification Hub uses Django's authentication system for user login, logout, and registration.

- Login: Enter your username and password to log in.
- Logout: Click "Logout" to log out of the system.
- Register: If you are a new user, you can register for an account with the appropriate permissions.

## Troubleshooting

If you encounter issues, here are some common solutions:

- Cannot log in: Check your username and password for typos. If you forgot your password, use the "Forgot Password" option.
- Certificate not found: Ensure the certificate exists and you're authorized to view it.
- Access denied: You might not have the required permissions. Contact an administrator for assistance.

## Contact Information

For further questions or support, contact the Qualification Hub team at kaiyrtaygabbassov@gmail.com.
