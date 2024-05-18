from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model



class EmailBackEnd(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        try:
            # Attempt to retrieve a user by email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # No user was found by this email
            return None

        # Verify the password against the user's hashed password
        if user.check_password(password):
            return user  # Authentication successful

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None