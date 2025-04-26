import requests
import re
from bs4 import BeautifulSoup

def dynamic_scrape(url, attr_type, attr_value, selections):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return [f"Failed to retrieve content. Status code: {response.status_code}"]

        soup = BeautifulSoup(response.text, 'html.parser')

        # Use <div> as the default tag
        if attr_type == "class":
            elements = soup.find_all("div", class_=attr_value)
        elif attr_type == "id":
            el = soup.find("div", id=attr_value)
            elements = [el] if el else []
        else:
            elements = soup.find_all("div")

        results = []

        for el in elements:
            text = el.get_text(separator=' ', strip=True)

            if "product_name" in selections and re.search(r"(name|title)", text, re.I):
                results.append(f"🛍️ Product Name: {text}")
            if "product_price" in selections and re.search(r"\$\d+(\.\d{2})?", text):
                results.append(f"💲 Price: {text}")
            if "email" in selections:
                emails = re.findall(r'\b[\w\.-]+?@\w+?\.\w{2,4}\b', text)
                for e in emails:
                    results.append(f"📧 Email: {e}")
            if "phone" in selections:
                phones = re.findall(r'\+?\d[\d\s\-\(\)]{7,}', text)
                for p in phones:
                    results.append(f"📞 Phone: {p}")
            if "description" in selections and "description" in text.lower():
                results.append(f"📝 Description: {text}")
            if "sizes" in selections and re.search(r"(size|small|medium|large)", text, re.I):
                results.append(f"📏 Size Info: {text}")
            if "variants" in selections and "variant" in text.lower():
                results.append(f"🔄 Variants: {text}")

        if not results:
            results.append("No matching data found for selected options.")
        return results

    except Exception as e:
        return [f"Error: {str(e)}"]
