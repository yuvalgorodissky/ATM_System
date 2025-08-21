import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import config

def get_server_config():
    """Get server configuration (host and port)"""
    return {
        "host": config.get_server_host(),
        "port": config.get_server_port()
    }

def get_base_url():
    """Get base URL for API testing"""
    return config.get_base_url()

def get_environment():
    """Get current environment"""
    return config.get_environment()

def get_server_host():
    """Get server host"""
    return config.get_server_host()

def get_server_port():
    """Get server port"""
    return config.get_server_port()

def print_current_config():
    """Print current configuration for debugging"""
    print(f"Environment: {get_environment()}")
    print(f"Server Host: {get_server_host()}")
    print(f"Server Port: {get_server_port()}")
    print(f"Base URL: {get_base_url()}")

if __name__ == "__main__":
    print_current_config()