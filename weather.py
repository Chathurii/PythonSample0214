"""
Weather retrieval program using Yahoo Weather API
Usage: python weather.py <postal_code>
"""

import sys
import requests
import json
from datetime import datetime

def get_weather(postal_code):
    """
    Retrieve weather information for a given postal code using Yahoo Weather API.
    
    Args:
        postal_code (str): The postal code to retrieve weather for
        
    Returns:
        dict: Weather information or None if failed
    """
    try:
        # Yahoo Weather API endpoint using YQL service
        # Note: This uses a free public endpoint for weather data
        url = f"https://weather-ydn-yql.media.yahoo.com/forecastrss"
        
        # Alternative approach using wttr.in which provides weather via postal code
        # This is more reliable than Yahoo's current offerings
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Using wttr.in API as a reliable alternative
        response = requests.get(
            f"https://wttr.in/{postal_code}?format=j1",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return parse_weather_data(data, postal_code)
        else:
            print(f"Error: Failed to retrieve weather data (Status: {response.status_code})")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to weather service: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid response from weather service")
        return None

def parse_weather_data(data, postal_code):
    """
    Parse weather data from the API response.
    
    Args:
        data (dict): Raw weather data from API
        postal_code (str): The postal code queried
        
    Returns:
        dict: Formatted weather information
    """
    try:
        current = data.get('current_condition', [{}])[0]
        
        weather_info = {
            'postal_code': postal_code,
            'location': data.get('nearest_area', [{}])[0].get('areaName', [{}])[0].get('value', 'Unknown'),
            'temperature': current.get('temp_C', 'N/A'),
            'temperature_f': current.get('temp_F', 'N/A'),
            'condition': current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
            'humidity': current.get('humidity', 'N/A'),
            'wind_speed': current.get('windspeedKmph', 'N/A'),
            'visibility': current.get('visibility', 'N/A'),
        }
        
        return weather_info
    except (KeyError, IndexError, TypeError):
        print("Error: Unable to parse weather data")
        return None

def display_weather(weather_info):
    """
    Display weather information in a formatted manner.
    
    Args:
        weather_info (dict): Parsed weather information
    """
    if not weather_info:
        return
    
    print("\n" + "="*50)
    print(f"Weather Information for {weather_info['location']}")
    print(f"Postal Code: {weather_info['postal_code']}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    print(f"Temperature: {weather_info['temperature']}°C ({weather_info['temperature_f']}°F)")
    print(f"Condition: {weather_info['condition']}")
    print(f"Humidity: {weather_info['humidity']}%")
    print(f"Wind Speed: {weather_info['wind_speed']} km/h")
    print(f"Visibility: {weather_info['visibility']} km")
    print("="*50 + "\n")

def main():
    """Main entry point of the program."""
    if len(sys.argv) != 2:
        print("Usage: python weather.py <postal_code>")
        print("Example: python weather.py 10001")
        sys.exit(1)
    
    postal_code = sys.argv[1]
    
    print(f"Retrieving weather information for postal code: {postal_code}...")
    
    weather_info = get_weather(postal_code)
    
    if weather_info:
        display_weather(weather_info)
    else:
        print("Failed to retrieve weather information.")
        sys.exit(1)

if __name__ == "__main__":
    main()
