import yaml
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self._config = self._load_config()
        self._environment = self._get_environment()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Configuration file not found at {config_path}\n"
                f"Please ensure config/config.yaml exists with the required environment configurations.\n"
                f"Expected structure:\n"
                f"development:\n"
                f"  server:\n"
                f"    host: \"127.0.0.1\"\n"
                f"    port: 8000\n"
                f"    base_url: \"http://localhost:8000\"\n"
                f"production:\n"
                f"  server:\n"
                f"    host: \"0.0.0.0\"\n"
                f"    port: 8000\n"
                f"    base_url: \"https://your-server-domain.com\"\n"
                f"default_environment: \"development\""
            )
        
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                if not config:
                    raise ValueError(f"Configuration file {config_path} is empty")
                return config
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration file {config_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading configuration from {config_path}: {e}")
    
    def _get_environment(self) -> str:
        """Get current environment from environment variable or default"""
        env = os.getenv("ATM_ENV", self._config.get("default_environment", "development"))
        
        if env not in self._config:
            print(f"Warning: Environment '{env}' not found in config. Using 'development'.")
            return "development"
        
        return env
    
    def get_server_host(self) -> str:
        """Get server host with environment variable override"""
        default_host = self._config[self._environment]["server"]["host"]
        return os.getenv("ATM_HOST", default_host)
    
    def get_server_port(self) -> int:
        """Get server port with environment variable override"""
        default_port = self._config[self._environment]["server"]["port"]
        return int(os.getenv("ATM_PORT", str(default_port)))
    
    def get_base_url(self) -> str:
        """Get base URL with environment variable override"""
        default_url = self._config[self._environment]["server"]["base_url"]
        custom_url = os.getenv("ATM_BASE_URL", default_url)
        
        if custom_url:
            return custom_url
        
        host = self.get_server_host()
        port = self.get_server_port()
        
        if host == "0.0.0.0":
            host = "localhost"
        
        return f"http://{host}:{port}"
    
    def get_environment(self) -> str:
        """Get current environment"""
        return self._environment
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get complete configuration for current environment"""
        return self._config[self._environment]

config = Config()