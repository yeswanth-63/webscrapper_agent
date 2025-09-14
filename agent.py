from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import json
from config import HUGGINGFACEHUB_API_TOKEN, HF_MODEL, HF_TASK, HF_MAX_NEW_TOKENS, HF_PROVIDER
from scrapper import scrape_subcategory  # Import scraper function

# Initialize Hugging Face LLM
hf_llm = HuggingFaceEndpoint(
    repo_id=HF_MODEL,
    task=HF_TASK,
    max_new_tokens=HF_MAX_NEW_TOKENS,
    do_sample=False,
    repetition_penalty=1.03,
    provider=HF_PROVIDER,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)

chat_model = ChatHuggingFace(llm=hf_llm)

# Prompt template for LLM to classify query and extract info
classification_prompt = """
You are an assistant. Determine if the user's query is product-related.
If it is, extract the following in strict JSON format:
1. keyword (product name)
2. max_price (numeric only)
3. subcategory (laptops, tablets, or touch)

If not product-related, respond in natural language with a helpful message.

User query: "{user_query}"
"""

prompt_template = PromptTemplate(template=classification_prompt, input_variables=["user_query"])


# Main function
def process_user_prompt(user_prompt: str):
    formatted_prompt = prompt_template.format(user_query=user_prompt)
    response = chat_model.invoke(formatted_prompt)
    
    try:
        # Try to parse JSON if product-related
        data = json.loads(response.content)
        if data.get("query_type") == "generic":
            # If generic, print full LLM response as message
            return response.content
        else:
            subcategory = data.get("subcategory", "")
            keyword = data.get("keyword", "")
            max_price = data.get("max_price", None)
            # scrape_subcategory(subcategory, keyword, max_price)
            
            df = scrape_subcategory(subcategory, keyword, max_price)
            if not df.empty:
                # print("all products data :")
                # print(df.head(20))
                return df
            else:
                # print("[SCRAPER RESULTS] No products found matching criteria.")
                return "[SCRAPER RESULTS] No products found matching criteria."


    except json.JSONDecodeError:
        # If JSON parsing fails, assume it's a generic message
        # print(f"[GENERIC RESPONSE] {response.content}")
        return response.content



