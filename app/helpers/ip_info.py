from fastapi import Request

import os
import requests
import json
import ipaddress
import random


from app.configs.logger import logger

IPINFO_API_URL = "https://ipinfo.io/{}"
IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")

def is_private_ip(ip):
    try:
        logger.debug(f"Checking if IP address is private: {ip}")
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False

def get_random_ip():
    logger.debug("Generating a random IP address")
    return str(ipaddress.IPv4Address(random.randint(0, (2**32) - 1)))

def get_client_ip(request: Request) -> str:
    logger.info(f"Get client ip from request: {request.headers}")
    forwarded_for = request.headers.get("x-forwarded-for")
    client_ip = forwarded_for.split(",")[0] if forwarded_for else request.client.host
    # If client ip is private (docker client), then get a random ip address.
    # Is for testing purposes
    if is_private_ip(client_ip):
        client_ip = get_random_ip()
    return client_ip

def get_country_and_timezone(client_ip: str) -> dict:
    """
        Gets the country and timezone from the IPinfo API.
        Args:
            client_ip (str): client IP address.
        Returns:
            dict: Dictionary with 'country' and 'timezone', or default values if there is an error.
    """
    try:
        logger.info(f"Getting country and timezone for IP: {client_ip}")
        # Make a GET request to the IPinfo API with the provided IP address and API token.
        response = requests.get(
            IPINFO_API_URL.format(client_ip),
            params={"token": IPINFO_TOKEN}
        )
        # If the request is successful, parse the JSON response and return the country and timezone.
        if response.status_code == 200:
            try:
                data = response.json()
                logger.info(f"Fetched data from IPinfo: {data}")
                return {
                    "country": data.get("country", "Unknown"),  # Ejemplo: "Cordoba"
                    "timezone": data.get("timezone", "Unknown"),  # Ejemplo: "America/Argentina/Cordoba"
                }
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON response from IPinfo: {response.text}")
        else:
            logger.warning(f"Error fetching data from IPinfo: {response.status_code}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
    return {"country": "Unknown", "timezone": "Unknown"}

