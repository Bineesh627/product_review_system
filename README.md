# Product Review System API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A RESTful API for managing products and reviews with role-based authentication.

## Features
- **Product Management**
  - Admin users can add, edit, and manage products in the catalog
  - Regular users can only view product information
  - Products should include essential details like name, description, and price
  - Product catalog should be browsable by all users

- **User System**
  - Implement user authentication with role-based access
  - Distinguish between admin users (can manage products) and regular users (can
only review)
  - Only authenticated regular users can submit reviews

- **Review System**
  - Regular users can submit reviews for products posted by admins
  - Reviews should include both ratings and feedback
  - All users can view reviews for any product
  - The system should prevent duplicate reviews from the same user for the same product
  - Product ratings should be aggregated to show overall product quality

- **Data Retrieval**
  - Provide endpoints to fetch product information along with associated reviews
  - Calculate and display average ratings for products
  - Ensure efficient data retrieval for product listings with rating summaries

## Prerequisites

- Python 3.10.18
- Django 4.2.6
- Django REST Framework 3.14.0
- Conda or pip

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bineesh627/product_review_system.git
   cd product_review_system
   ```

2. **Create Conda environment**
   ```bash
   conda create -n product_review python=3.10.18
   conda activate product_review
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Server

```bash
python manage.py runserver
```

Access the API at `http://127.0.0.1:8000/`

## API Endpoints

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/register/` | POST | User registration | Public |
| `/login/` | POST | Obtain auth token | Public |
| `/logout/` | POST | Invalidate token | Authenticated |
| `/products/` | GET | List all products | Public |
| `/products/` | POST | Create new product | Admin |

## Example Requests

**User Registration**
```bash
curl -X POST http://127.0.0.1:8000/register/ \
  -H "Content-Type: application/json" \
  -D '{"username": "user1", "password": "pass123", "email": "user@example.com"}'
```

**User & Admin Login**
```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/json" \
  -D '{"username": "admin", "password": "admin"}'
```

**User & Admin Logout**
```bash
curl -X POST http://127.0.0.1:8000/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token token_here" \
```

**Add Products in Admin**
```bash
curl -X POST http://127.0.0.1:8000/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token token_here" \
  -D '{"name": "Assus", "description": "Good laptop for playing games","price": 60000}'
```

**View Products**
```bash
curl -X GET http://127.0.0.1:8000/products/ \
  -H "Content-Type: application/json"
```

## Configuration

Set these environment variables in `.env`:
```bash
DEBUG = True  # Set to False in production
SECRET_KEY = 'secret_key_here'
```

## License

MIT License - See [LICENSE](LICENSE) for details.