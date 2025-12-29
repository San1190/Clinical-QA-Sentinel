"""
Configuration Loader Utility
=============================
Centralized configuration management for Clinical-QA-Sentinel

This module handles loading configuration from:
1. config.json file
2. Environment variables (.env file or system env)
3. Command-line arguments (future expansion)

Priority: Environment Variables > config.json > Defaults
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing"""
    pass


class ConfigLoader:
    """
    Singleton configuration loader for the application.
    
    Usage:
        config = ConfigLoader().get_config()
        portal_url = config['portal_url']
    """
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_configuration()
    
    def _load_configuration(self) -> None:
        """Load configuration from all sources"""
        # Load environment variables from .env file
        load_dotenv()
        
        # Get project root directory
        project_root = Path(__file__).parent.parent
        config_file = project_root / 'config' / 'config.json'
        
        # Load JSON configuration
        if not config_file.exists():
            raise ConfigurationError(f"Configuration file not found: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            self._config = json.load(f)
        
        # Apply environment-specific configuration
        self._apply_environment_config()
        
        # Override with environment variables
        self._apply_env_overrides()
        
        # Validate configuration
        self._validate_config()
    
    def _apply_environment_config(self) -> None:
        """Apply active environment configuration"""
        active_env = os.getenv('ENVIRONMENT', self._config.get('active_environment', 'demo'))
        
        if active_env not in self._config['environments']:
            raise ConfigurationError(f"Invalid environment: {active_env}")
        
        env_config = self._config['environments'][active_env]
        
        # Merge environment-specific config into main config
        self._config['portal_url'] = env_config['portal_url']
        self._config['base_url'] = env_config['base_url']
        self._config['active_environment'] = active_env
    
    def _apply_env_overrides(self) -> None:
        """Override configuration with environment variables"""
        # Portal URL override
        if os.getenv('PORTAL_URL'):
            self._config['portal_url'] = os.getenv('PORTAL_URL')
        
        # Headless mode override
        if os.getenv('HEADLESS_MODE'):
            self._config['browser']['headless'] = os.getenv('HEADLESS_MODE').lower() == 'true'
        
        # Browser name override
        if os.getenv('BROWSER_NAME'):
            self._config['browser']['name'] = os.getenv('BROWSER_NAME')
        
        # Log level override
        if os.getenv('LOG_LEVEL'):
            self._config['logging']['level'] = os.getenv('LOG_LEVEL')
        
        # Selenium Grid configuration
        if os.getenv('SELENIUM_HUB_URL'):
            self._config['selenium_hub_url'] = os.getenv('SELENIUM_HUB_URL')
            self._config['use_remote_driver'] = True
        else:
            self._config['use_remote_driver'] = False
    
    def _validate_config(self) -> None:
        """Validate that required configuration exists"""
        required_keys = ['portal_url', 'timeouts', 'browser', 'logging']
        
        for key in required_keys:
            if key not in self._config:
                raise ConfigurationError(f"Missing required configuration: {key}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get the complete configuration dictionary"""
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a specific configuration value.
        
        Supports nested keys using dot notation:
            config.get('browser.headless')
            config.get('timeouts.page_load_timeout')
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def reload(self) -> None:
        """Reload configuration from files"""
        self._config = None
        self._load_configuration()


# Convenience function for quick access
def load_config() -> Dict[str, Any]:
    """
    Load and return the application configuration.
    
    Returns:
        dict: Complete configuration dictionary
    """
    return ConfigLoader().get_config()


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a specific configuration value.
    
    Args:
        key: Configuration key (supports dot notation)
        default: Default value if key not found
        
    Returns:
        Configuration value or default
    """
    return ConfigLoader().get(key, default)


# Example usage and testing
if __name__ == "__main__":
    print("="*70)
    print("Configuration Loader - Test Run")
    print("="*70)
    
    try:
        config = load_config()
        
        print(f"\nActive Environment: {config['active_environment']}")
        print(f"Portal URL: {config['portal_url']}")
        print(f"Browser: {config['browser']['name']}")
        print(f"Headless Mode: {config['browser']['headless']}")
        print(f"Page Load Timeout: {config['timeouts']['page_load_timeout']}s")
        
        print("\nTest Users:")
        for i, user in enumerate(config['test_users'], 1):
            print(f"  {i}. {user['username']} - Expected: {user['expected_result']}")
        
        print("\nConfiguration loaded successfully! ✓")
        
    except ConfigurationError as e:
        print(f"\n✗ Configuration Error: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
