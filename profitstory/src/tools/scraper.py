# src/tools/scraper.py
from langchain_core.tools import tool
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import time

class LegalScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ProfitStoryAI-PricingBot/1.0"
        })
        self.robot_parsers = {}

    def can_fetch(self, url: str) -> bool:
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        if base_url not in self.robot_parsers:
            rp = RobotFileParser()
            robots_url = urljoin(base_url, "/robots.txt")
            try:
                rp.set_url(robots_url)
                rp.read()
                self.robot_parsers[base_url] = rp
            except:
                return True

        return self.robot_parsers[base_url].can_fetch(
            self.session.headers["User-Agent"], url
        )

    def extract_product_data(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        domain = urlparse(url).netloc

        data = {
            "title": "",
            "description": "",
            "brand": "",
            "images": [],
            "price": None,
        }

        # AMAZON
        if "amazon" in domain:
            title = soup.select_one("#productTitle")
            price = soup.select_one(".a-price-whole")
            desc = soup.select_one("#feature-bullets")
            brand = soup.select_one("#bylineInfo")
            images = soup.select(".imageThumbnail img")

            data["title"] = title.get_text(strip=True) if title else ""
            if price:
                num = "".join(c for c in price.get_text() if c.isdigit())
                data["price"] = float(num) if num else None
            data["description"] = desc.get_text(strip=True) if desc else ""
            data["brand"] = brand.get_text(strip=True) if brand else ""

        # FLIPKART
        elif "flipkart" in domain:
            title = soup.select_one("span.B_NuCI")
            price = soup.select_one("div._30jeq3")
            desc = soup.select_one("div._1mXcCf")
            images = soup.select("img._396cs4")

            data["title"] = title.get_text(strip=True) if title else ""
            if price:
                num = "".join(c for c in price.get_text() if c.isdigit())
                data["price"] = float(num) if num else None
            data["description"] = desc.get_text(strip=True) if desc else ""

        # MYNTRA
        elif "myntra" in domain:
            title = soup.select_one("h1.pdp-title")
            price = soup.select_one("span.pdp-price")
            desc = soup.select_one("div.pdp-product-description-content")
            images = soup.select("div.image-grid-image img")

            data["title"] = title.get_text(strip=True) if title else ""
            if price:
                num = "".join(c for c in price.get_text() if c.isdigit())
                data["price"] = float(num) if num else None
            data["description"] = desc.get_text(strip=True) if desc else ""

        data["images"] = [img.get("src") for img in images][:5] if "images" in locals() else []
        return data


# ------------------------------- FIXED TOOL ------------------------------- #

@tool
def legal_web_scraper_tool(input: dict) -> dict:
    """
    LEGAL web scraper wrapper compatible with LangChain tools.

    Expected Input:
        { "url": "https://example.com/product" }
    """
    url = input.get("url")
    if not url:
        return {"error": "Missing 'url' in input"}

    scraper = LegalScraper()

    if not scraper.can_fetch(url):
        return {"scrape_allowed": False, "error": "Blocked by robots.txt", "url": url}

    try:
        time.sleep(1.5)
        response = scraper.session.get(url, timeout=10)
        response.raise_for_status()

        product = scraper.extract_product_data(response.text, url)
        product["scrape_allowed"] = True
        product["url"] = url
        return product

    except Exception as e:
        return {
            "scrape_allowed": True,
            "error": f"Scrape failed: {str(e)}",
            "url": url
        }
