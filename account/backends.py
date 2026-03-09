from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login using email instead of username
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate against email or username
        """
        try:
            # Try to get user by email first
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Fall back to username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
