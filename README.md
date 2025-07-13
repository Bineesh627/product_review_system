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

Access the API at `http://127.0.0.1:8000/api/`

## API Endpoints

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/register/` | POST | User registration | User |
| `/api/login/` | POST | Obtain auth token | User/Admin |
| `/api/logout/` | POST | Invalidate token | Authenticated |
| `/api/products/` | GET | List all products | User/Admin |
| `/api/products/1/` |	GET	| Product details | User/Admin |
| `/api/products/` | POST | Create new product | Admin |
| `/api/products/1/` | DELETE | Remove product | Admin |
| `/api/products/1/` | PUT | Update product | Admin |
| `/api/products/1/` | PATCH | Edit product | Admin |
| `/api/products/1/reviews/` | GET | List product reviews | User |
| `/api/products/1/reviews/` |	POST | Submit review | User |


## Example Requests

**User Registration**
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -D '{"username": "user1", "password": "pass123", "email": "user@example.com"}'
```

**User & Admin Login**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -D '{"username": "admin", "password": "admin"}'
```

**User & Admin Logout**
```bash
curl -X POST http://127.0.0.1:8000/api/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token ADMIN/USER_TOKEN_HERE"
```

**Add Products in Admin**
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token ADMIN_TOKEN_HERE" \
  -D '{"name": "Assus", "description": "Good laptop for playing games","price": 60000}'
```

**View Products**
```bash
curl -X GET http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token ADMIN/USER_TOKEN_HERE"
```
**Delete Products**
```bash
curl -X DELETE http://127.0.0.1:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token ADMIN_TOKEN_HERE"
```
**Update Products Using Put**
```bash
curl -X PUT http://127.0.0.1:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token ADMIN_TOKEN_HERE" \
  -d '{"name": "lenova", "description": "brand new", "price":1000}'
```

**Update Products Using Patch**
```bash
curl -X PATCH http://127.0.0.1:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token ADMIN_TOKEN_HERE" \
  -d '{"price": 1000}'
```

**Submit Review**
```bash
curl -X POST http://127.0.0.1:8000/api/products/1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token USER_TOKEN_HERE" \
  -d '{"rating": 5, "feedback": "Excellent"}'
```

**View Product Review**
```bash
curl -X GET http://127.0.0.1:8000/api/products/1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token USER_TOKEN_HERE"
```

## Configuration

Set these environment variables in `.env`:
```bash
DEBUG = True  # Set to False in production
SECRET_KEY = 'secret_key_here'
```

## License

MIT License - See [LICENSE](LICENSE) for details.