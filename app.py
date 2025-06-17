from flask import Flask, render_template
import json
from vmware_versions import save_versions

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Try to read existing JSON file
        with open('vmware_versions.json', 'r') as f:
            data = json.load(f)
            latest_tools = data['vmware_tools'][0] if data['vmware_tools'] else None
            latest_esxi8 = data['esxi_versions']['esxi8'][0] if data['esxi_versions']['esxi8'] else None
            latest_esxi7 = data['esxi_versions']['esxi7'][0] if data['esxi_versions']['esxi7'] else None
            latest_vcenter8 = data['vcenter_versions']['vcenter8'][0] if data['vcenter_versions']['vcenter8'] else None
            latest_vcenter7 = data['vcenter_versions']['vcenter7'][0] if data['vcenter_versions']['vcenter7'] else None
            latest_vcf5 = data['vcf_versions']['vcf5'][0] if data['vcf_versions']['vcf5'] else None
            last_updated = data['last_updated']
    except FileNotFoundError:
        # If file doesn't exist, scrape the data
        data = save_versions()
        latest_tools = data['vmware_tools'][0] if data['vmware_tools'] else None
        latest_esxi8 = data['esxi_versions']['esxi8'][0] if data['esxi_versions']['esxi8'] else None
        latest_esxi7 = data['esxi_versions']['esxi7'][0] if data['esxi_versions']['esxi7'] else None
        latest_vcenter8 = data['vcenter_versions']['vcenter8'][0] if data['vcenter_versions']['vcenter8'] else None
        latest_vcenter7 = data['vcenter_versions']['vcenter7'][0] if data['vcenter_versions']['vcenter7'] else None
        latest_vcf5 = data['vcf_versions']['vcf5'][0] if data['vcf_versions']['vcf5'] else None
        last_updated = data['last_updated']
    
    return render_template('index.html', 
                         latest_tools=latest_tools,
                         latest_esxi8=latest_esxi8,
                         latest_esxi7=latest_esxi7,
                         latest_vcenter8=latest_vcenter8,
                         latest_vcenter7=latest_vcenter7,
                         latest_vcf5=latest_vcf5,
                         last_updated=last_updated)

@app.route('/refresh')
def refresh():
    save_versions()
    return {'success': True, 'message': 'Data refreshed successfully'}

if __name__ == '__main__':
    app.run(debug=True) 