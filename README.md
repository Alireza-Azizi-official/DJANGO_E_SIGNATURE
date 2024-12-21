# Django Test Project with DocuSign API

This project demonstrates how to create and sign a contract using Django and the DocuSign API. It allows a user to create a contract, sign it, and then send it via email to a recipient to sign.

## Project Workflow
The application follows this basic flow:
1. **Register**: User registers an account.
2. **Login**: User logs into the application.
3. **Home**: After login, the user is directed to the home page.
4. **Create Contract**: The user creates a contract.
5. **Success**: After contract creation, the user sees a success page.
6. **Send Email**: The contract is sent to a determined recipient to sign via email.
7. **Contract Status**: Track the contract signing status.
8. **Error**: If there is an error, it is displayed to the user.

## Contract Text
The contract text is set by default using Lorem Ipsum text, which is used throughout the app. If needed, you can find a test PDF file named `test.pdf` in the project directory.

## Configuration
All the key factors related to DocuSign configuration are in the `core/secrets.env` file.
The private key used for authentication with DocuSign is located in `contracts/private_key`.
The DocuSign username and password should be defined in the `secrets.env` file. However, due to personal privacy concerns, I have refrained from including them in the `secrets.env` file.

## DocuSign Configuration
Some key DocuSign configuration settings are placed in `core/secrets.env` and may require adjustments for your own DocuSign account.

**Important Note**: There is a minor issue in the configuration of DocuSign that I was unable to fix despite my efforts using Stack Overflow, ChatGPT, and DocuSign documentation. The issue arises when trying to create an envelope and contract, but it has not been resolved yet.

## Admin Login Information
To log in as the admin, use the following credentials:
- **Username**: admin1
- **Password**: adminadmin
  
## Requirements
All required dependencies are listed in the `requirements.txt` file. Install them using the following command:

```bash
pip install -r requirements.txt
