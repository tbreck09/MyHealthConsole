# MyHealthConsole Web App

MyHealthConsole is a platform designed to help users keep track of their healthcare-related information. On the app users can track their care providers, prescriptions, or appointments. Our app provides a convenient and organized solution for all your healthcare data tracking needs. Built using the Django web framework and powered by PostgreSQL, this app ensures security, reliability, and a seamless user experience.


 

![My Health Console landing page](https://i.imgur.com/6gWKjwz.png)
![My Health Console about page](https://i.imgur.com/hOPRyP7.png)


## Features

- **User Authentication:** Secure user authentication system to ensure that each user's data is private and accessible only to them.

- **Care Provider Management:** Easily add, edit, or remove information about your healthcare providers. Store their names, departments, and location.

- **Prescription Tracking:** Keep a record of your prescriptions, including medication names, and descriptions.

- **Appointment Scheduling:** Schedule and manage your medical appointments. Save the date and time of each appointment.

- **Intuitive Dashboard:** The dashboard provides an overview of upcoming appointments, active prescriptions, and quick access to care provider details.

- **User-Friendly Interface:** A clean and modern interface that is easy to navigate, making it simple for users of all levels to manage their healthcare information.

## Technology Stack

- **Django:**

- **PostgreSQL:**

## Installation and Setup

1. Clone the repository: `git clone https://github.com/your-username/healthcare-tracker.git`
2. Navigate to the project directory: `cd healthcare-tracker`
3. Create and activate a virtual environment: `python -m venv venv && source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up the database in `settings.py` using your PostgreSQL credentials.
6. Apply migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Start the development server: `python manage.py runserver`

## Usage

1. Open your web browser and go to `http://127.0.0.1:8000/`
2. Log in using your superuser credentials.
3. Navigate through the different sections to add and manage care providers, prescriptions, and appointments.
4. Enjoy the seamless experience of tracking your healthcare data!

## Contribution

Contributions to this project are welcome! Feel free to submit issues and pull requests on the GitHub repository. Please ensure that you follow the project's code of conduct and guidelines for contributing.



