from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

app = Flask(__name__)

def get_vmware_versions():
    try:
        # VMware Product Downloads page
        url = "https://customerconnect.vmware.com/downloads"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all product sections
        products = []
        product_sections = soup.find_all('div', class_='product-downloads')
        
        for section in product_sections:
            product_name = section.find('h2').text.strip()
            version_elem = section.find('span', class_='version')
            if version_elem:
                version = version_elem.text.strip()
                products.append({
                    'name': product_name,
                    'version': version,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        
        return products
    except Exception as e:
        print(f"Error fetching VMware versions: {str(e)}")
        return []

@app.route('/')
def index():
    versions = get_vmware_versions()
    return render_template('index.html', versions=versions)

@app.route('/api/versions')
def get_versions():
    versions = get_vmware_versions()
    return jsonify(versions)

if __name__ == '__main__':
    app.run(debug=True) 