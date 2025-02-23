from bs4 import BeautifulSoup
import pandas as pd

# Read the HTML file
with open("index.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "lxml")

# Find all images inside the corrected class 'productImges'
images = soup.select(".productImges img")

# Extract image URLs
image_urls = [img["src"] for img in images if img["src"].endswith(".png")]

# Save to Excel
df = pd.DataFrame({"Image URLs": image_urls})
df.to_excel("images.xlsx", index=False)

print("✅ Image URLs successfully saved to images.xlsx")
