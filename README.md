
## Video Preview 
https://youtu.be/OwYYTjJkwF0


# FastAPI Login and OTP Verification System

This project is a FastAPI-based system for user login and authentication via OTP (One-Time Password). It integrates Twilio for sending OTPs via SMS and provides email OTP functionality using SMTP. The project uses SQLAlchemy for database interactions and JWT (JSON Web Token) for user authentication.

## Features

- **User Login**: Secure login system with username/password validation.
- **OTP via Twilio**: Generate and send OTP to users via SMS using Twilio API.
- **Email OTP**: OTP sent via email using SMTP.
- **Account Lock**: Temporarily lock accounts after multiple incorrect login attempts.
- **JWT Authentication**: Uses JWT tokens for secure authentication and session management.

## Technologies Used

- **FastAPI**: For creating APIs.
- **SQLAlchemy**: For database interaction.
- **Twilio API**: For sending OTP via SMS.
- **SMTP (Gmail)**: For sending OTP via email.
- **JWT**: For handling user authentication tokens.
- **Python Libraries**: `random`, `smtplib`, `logging`, `jwt`, `dateutil`, `datetime`, `email.mime`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aakashbaluoffical/Restful-Login-API-in-python.git
2. Install the required dependencies:
    ```bash
     pip install -r requirements.txt


## API Endpoints

1. User Login (/api/v1/login)
    Method: POST
    Description: Validate username and password for login.
    Body Parameters:
    username: User's username.
    password: User's password.
    Response:
    Success: Returns a welcome message.
    Error: Returns a 400 or 401 error with a detailed message.

## How It Works
  1. Login: The user provides their username and password for validation. If incorrect, the user gets a limited number of attempts before their account is temporarily locked.
  2. Account Lock: After a certain number of incorrect attempts, the user's account is locked for a brief period (configurable in the code).
  3. OTP Generation*: For mobile login, a 6-digit OTP is generated and sent via Twilio SMS. For email login, the OTP is sent via Gmail.

## Running the Project      
1. Run the FastAPI application using Uvicorn::
    ```bash
     uvicorn main:app --reload

    
## License
This project is licensed under the MIT License. See the LICENSE file for details.
Feel free to customize the instructions and details based on your project's specifics!


