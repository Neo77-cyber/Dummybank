# Dummybank-Finanace-Mnagement-Application

Dummy Bank is a simulated banking system and a finance management application created with Django for testing and educational purposes. It provides a comprehensive solution for managing your finances, shopping lists, budgeting, and savings goals. With an intuitive interface and powerful features, it aims to help users stay organized and achieve their financial goals. 

## Features

- Account Creation: Users can create new bank accounts with basic information such as name, address, and initial balance.

- Deposits and Withdrawals: Users can deposit and withdraw funds from their accounts.

- Balance Inquiry: Users can check their account balances.
- 
- Financial Management: Track your income, expenses, and overall financial health. Update your account balance when receiving new funds to keep your financial situation up to date.

- Shopping Lists: Create and manage shopping lists for your everyday needs. Add items, mark them as purchased, and have the amount deducted from your balance. Get notifications when your spending reaches a certain threshold to stay within your budget.

- Budgeting and Savings Goals: Set up budgets and savings goals to track your spending and savings progress. Get insights into your spending habits and save towards specific targets.

- Wishlist and Future Plans: Plan for future purchases by creating a wishlist of items you want to buy. Keep track of upcoming expenses and set aside funds accordingly.

- Transfer Funds: Easily transfer funds to other users of the app. Stay organized when splitting expenses or sharing costs with friends and family.

## Getting Started

To get started with the Dummy Bank system, follow these steps:

## Installation
1. Clone the repository: `git clone https://github.com/neo77-cyber/ Dummybank.git`
2. Navigate to the project directory: `cd novaproject-django`
3. Create a virtual environment: `pipenv shell`
5. Install dependencies: `pipenv install -r requirements.txt`
6. Apply database migrations: `python manage.py migrate`
7. Start the development server: `python manage.py runserver`
8. Access the app in your browser at `http://localhost:8000`
9. Access FastAPI backend code seperately: exit previous virtual environment `deactivate`
10.  Navigate to the fastapi directory: `cd novaproject-fastapi`
11. create a virtual environment `pipenv shell`
12. install dependecies `pipenv install -r requirements.txt`
13. start the development server `uvicorn main:app --reload`
14. Access the app in your browser at `http://localhost:8000`

## Technologies Used
- Django: Python web framework
- FastAPI: python web framework
- SQLite: Relational database management system
- JavaScript, HTML, CSS: Frontend development
- Bootstrap: CSS framework for responsive design

## Contributing
Contributions to the Dummybank App are welcome! If you encounter any issues or have suggestions for improvements, please submit an issue or a pull request to the GitHub repository.


## Disclaimer

Please note that Dummy Bank is a simulated banking system and should not be used for actual financial transactions or sensitive data. It is intended for testing and educational purposes only.
