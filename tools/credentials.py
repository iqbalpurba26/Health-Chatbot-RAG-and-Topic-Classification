"""Accommodate the credentials."""
import os
import openai
from dotenv import load_dotenv
# Load configuration from .env file
load_dotenv()

# Azure OpenAI configuration
# API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get('API_KEY')
DEPLOYMENT_CHAT = os.environ.get('DEPLOYMENT_CHAT')
openai.api_key = API_KEY
# openai.api_base = API_URL
