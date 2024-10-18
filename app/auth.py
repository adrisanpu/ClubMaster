import boto3
from botocore.exceptions import ClientError
import os

# Load your Cognito details from environment variables or hardcode (not recommended for production)
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_REGION = os.getenv('COGNITO_REGION', 'us-east-1')

# Initialize the Cognito client
client = boto3.client('cognito-idp',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=COGNITO_REGION,
    verify=False)


def login_user(username, password):
    """Login a user with Cognito"""
    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            },
            ClientId=COGNITO_CLIENT_ID
        )

        # The response will contain an ID token (JWT) if login is successful
        return response['AuthenticationResult']['IdToken']

    except ClientError as e:
        print(f"Error during login: {e}")
        return None


def signup_user(username, password, email):
    """Signup a new user with Cognito"""
    try:
        response = client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                }
            ]
        )
        return response

    except ClientError as e:
        print(f"Error during signup: {e}")
        return None


def confirm_signup(username, confirmation_code):
    """Confirm a user after signup with Cognito"""
    try:
        response = client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code
        )
        return response
    except ClientError as e:
        print(f"Error during confirmation: {e}")
        return None
