import os
from models import User
from dotenv import load_dotenv

load_dotenv()

# Set up test data
test_user_data = {
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "testpassword"
}

# Create a new user instance
user = User(name=test_user_data["name"], email=test_user_data["email"])

# Set password
user.set_password(test_user_data["password"])
print(f"Password hash: {user.password_hash}")

# Save user to database
user.save_to_db()
print("User saved to database.")

# Find user by email
found_user = User.find_by_email(test_user_data["email"])
print(f"Found user: {found_user}")

# Check password
is_password_correct = found_user.check_password(test_user_data["password"])
print(f"Is password correct: {is_password_correct}")

# Generate reset token
reset_token = found_user.generate_reset_token()
print(f"Reset token: {reset_token}")

# Verify reset token
verified_email = User.verify_reset_token(reset_token)
print(f"Verified email from reset token: {verified_email}")

# Remove reset token
User.remove_reset_token(reset_token)
print("Reset token removed.")

# Verify reset token after removal
verified_email_after_removal = User.verify_reset_token(reset_token)
print(f"Verified email from reset token after removal: {verified_email_after_removal}")