# Steep Shop 🍃

Steep Shop is a full-stack e-commerce platform designed for selling a variety of tea products. Built with Django and enhanced with AJAX for seamless user interaction, this web application provides a smooth shopping experience. Users can browse, add items to their cart, and complete purchases securely through Razorpay integration.

![Steep Shop Screenshot](https://github.com/Ayush-Mittal10/Steep_Shop/assets/screenshot.png)

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- **Product Browsing:** Search and browse through a range of tea products with detailed descriptions.
- **Cart Functionality:** Add items to your cart with AJAX-based updates and quantity controls, offering a streamlined shopping experience without page reloads.
- **Order Processing:** View order summaries and checkout seamlessly.
- **Payment Integration:** Securely complete transactions with Razorpay payment gateway integration.
- **Automated Email Notifications:** Get order confirmations and updates through SMTP-configured email alerts.

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript (AJAX)
- **Database:** SQLite (configurable to PostgreSQL or MySQL)
- **Payment Integration:** Razorpay API
- **Other Tools:** Git for version control, SMTP for email notifications

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.x and pip installed
- Django installed (`pip install django`)
- Razorpay account for payment API keys
- Git installed for version control

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ayush-Mittal10/Steep_Shop.git
   cd Steep_Shop
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Set up environment variables:**
   Create a .env file in the root directory and add the following:
   ```bash
   RAZORPAY_API_KEY=<your_razorpay_api_key>
   RAZORPAY_API_SECRET=<your_razorpay_api_secret>
   EMAIL_HOST_USER=<your_email>
   EMAIL_HOST_PASSWORD=<your_email_password>
5. **Apply database migrations:**
   ```bash
   python manage.py migrate
6. **Create a superuser for admin access**
   ```bash
   python manage.py createsuperuser
7. **Run the development server:**
   ```bash
   python manage.py runserver

## Usage

- **Admin Dashboard:** Access the Django admin at `/admin` to manage products, orders, and users.
- **Product Catalog:** Browse the catalog on the home page, add products to the cart, and update quantities.
- **Checkout and Payments:** Complete checkout securely with Razorpay, and receive confirmation emails for each order.

## Project Structure

    ```plaintext
    Steep_Shop/
    ├── steep_shop/             # Core Django app and project settings
    ├── products/               # App for product catalog and cart management
    ├── static/                 # Static files (CSS, JavaScript, images)
    ├── templates/              # HTML templates for frontend
    └── requirements.txt        # List of dependencies


## License

This project is licensed under the MIT License.

