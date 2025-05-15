Budget Tracker Application Documentation

 1. Design Approach

 Architecture Overview
The Budget Tracker application is implemented as a Django web application with:
- Backend: Django 5.2.1 with Django's built-in template system
- Database: SQLite3 (development) with PostgreSQL support for production
- Authentication: Django's built-in authentication system
- Frontend: Django templates with HTML/CSS/JavaScript
- Deployment: Configured for both development and production environments

 Technology Stack
- Backend:
  - Django 5.2.1
  - Django Authentication System
  - Django ORM
  - Django Templates
  - SQLite3 (development)
  - PostgreSQL (production-ready)

- Frontend:
  - Django Templates
  - HTML/CSS/JavaScript
  - Bootstrap (based on template usage)
  - Chart.js (for budget visualization)

 Database Design
The application uses Django's ORM with the following models:
- User (Django's built-in User model)
- Category
  - name (CharField)
  - description (TextField)
  - user (ForeignKey to User)
- Transaction
  - user (ForeignKey to User)
  - category (ForeignKey to Category)
  - amount (DecimalField)
  - date (DateTimeField)
  - transaction_type (choices: INCOME/EXPENSE)
  - description (TextField)
- Budget
  - user (ForeignKey to User)
  - category (ForeignKey to Category)
  - amount (DecimalField)
  - month (DateField)
  - Methods: get_spent_amount(), get_remaining_amount()

 Application Structure
The application follows Django's MVT (Model-View-Template) pattern:
- Models: Defined in `home/models.py`
- Views: Implemented in `home/views.py`
- Templates: Located in `home/templates/`
- URLs: Configured in `core/urls.py`

 Key Features
1. User Authentication
   - Login/Register functionality
   - Session-based authentication
   - Protected routes with @login_required decorator

2. Transaction Management
   - Add/Edit/Delete transactions
   - Filter transactions by date, category, amount
   - Pagination (10 items per page)
   - Transaction categorization

3. Budget Management
   - Set monthly budgets by category
   - Track spending against budgets
   - Visual budget overview
   - Budget status calculation

4. Category Management
   - Create custom categories
   - Associate transactions with categories
   - User-specific categories

5. Dashboard
   - Monthly income/expense summary
   - Current month's transactions
   - Budget status overview
   - Category-wise spending analysis



2. Code Design Choices
Backend (Django)
Rationale for choosing Django:
- Built-in admin interface
- Robust authentication system
- Secure by default
- Rapid development capabilities
- Excellent documentation
- Built-in template system
- ORM for database operations

Database Choice
SQLite3 (development) with PostgreSQL support:
- SQLite3 for development simplicity
- PostgreSQL support for production scalability
- Django ORM abstraction for database operations
- Easy migration between databases

Authentication System
Django's built-in authentication:
- Session-based authentication
- Secure password hashing
- User model extension capability
- Login/Logout functionality
- Protected routes

URL Structure
RESTful-like URL patterns:
- `/` - Dashboard
- `/login/` - Login page
- `/register/` - Registration
- `/transactions/` - Transaction management
- `/add-transaction/` - Add new transaction
- `/manage-categories/` - Category management
- `/set-budget/` - Budget management
- `/budget-overview/` - Budget visualization
- `/pdf/` - Report generation



3. User Credentials


 Test User
- Username: testuser
- Password: testuser
- Role: Regular user with standard permissions

4. API Endpoints

 Authentication
- GET `/login/` - Login page
- POST `/login/` - Login form submission
- GET `/register/` - Registration page
- POST `/register/` - Registration form submission
- GET `/logout/` - Logout user

Transactions
- GET `/transactions/` - List transactions
  - Supports filtering by:
    - Date range
    - Category
    - Amount range
  - Pagination: 10 items per page
- POST `/add-transaction/` - Create transaction
- POST `/update-transaction/<id>/` - Update transaction
- POST `/delete-transaction/<id>/` - Delete transaction

 Categories
- GET `/manage-categories/` - List categories
- POST `/manage-categories/` - Create category

 Budgets
- GET `/set-budget/` - Budget management page
- POST `/set-budget/` - Create/update budget
- GET `/budget-overview/` - Budget visualization
  - Supports monthly view
  - Category-wise breakdown
  - Spending analysis

5. Setup Instructions

 Local Development
1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - SECRET_KEY
   - DEBUG=True
   - ALLOWED_HOSTS=localhost,127.0.0.1
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Start development server:
   ```bash
   python manage.py runserver
   ```





