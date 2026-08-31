import os
from typing import Any, List

def get_env_var(var_name: str, default: Any = None, cast_type: type = str) -> Any:
    """
    Reusable utility to fetch environment variables with optional type casting.
    Helps prevent DRY violations in settings.py and ensures safe fallbacks.
    """
    try:
        value = os.environ[var_name]
        
        if cast_type == bool:
            return value.lower() in ('true', '1', 't', 'y', 'yes')
            
        if cast_type == list:
            return [item.strip() for item in value.split(',') if item.strip()]
            
        return cast_type(value)
        
    except KeyError:
        if default is not None:
            return default
        raise ImproperlyConfigured(f"Set the {var_name} environment variable")

class ImproperlyConfigured(Exception):
    """Exception raised when a required environment variable is missing."""
    pass
