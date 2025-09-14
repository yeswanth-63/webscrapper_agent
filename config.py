import os
from dotenv import load_dotenv

load_dotenv()

# API Tokens
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# HuggingFace LLM config
HF_MODEL = "openai/gpt-oss-20b"   # your model repo_id
HF_TASK = "text-generation"
HF_MAX_NEW_TOKENS = 512
HF_PROVIDER = "auto"

# Category → Subcategory → URL mapping
CATEGORIES_DICT = {
    "computers": {
        "laptops": "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
        "tablets": "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
    },
    "phones": {
        "touch": "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch",
    }
}
