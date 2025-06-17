import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')
    except:
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
        except:
            try:
                return datetime.strptime(date_str, '%d %b %Y').strftime('%Y-%m-%d')
            except:
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                except:
                    return None

def scrape_vmware_tools():
    url = "https://knowledge.broadcom.com/external/article/304809/build-numbers-and-versions-of-vmware-too.html"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        versions = []
        table = soup.find('table')
        
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 4:
                    version_info = {
                        "version": cols[0].text.strip(),
                        "release_date": parse_date(cols[1].text.strip()),
                        "build_number": cols[2].text.strip(),
                        "tool_internal_version": cols[3].text.strip()
                    }
                    versions.append(version_info)
        
        return versions
    except Exception as e:
        print(f"Error scraping VMware Tools versions: {str(e)}")
        return []

def scrape_esxi_versions():
    url = "https://knowledge.broadcom.com/external/article/316595/build-numbers-and-versions-of-vmware-esx.html"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        esxi_versions = {
            "esxi8": [],
            "esxi7": []
        }
        
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 4:
                    version = cols[0].text.strip()
                    if version.startswith('ESXi 8') or version.startswith('ESXi 7'):
                        version_info = {
                            "version": version,
                            "release_name": cols[1].text.strip(),
                            "release_date": parse_date(cols[2].text.strip()),
                            "build_number": cols[3].text.strip(),
                            "available_as": cols[4].text.strip() if len(cols) > 4 else "N/A"
                        }
                        if version.startswith('ESXi 8'):
                            esxi_versions["esxi8"].append(version_info)
                        elif version.startswith('ESXi 7'):
                            esxi_versions["esxi7"].append(version_info)
        
        # Sort versions by release date
        for key in esxi_versions:
            esxi_versions[key].sort(key=lambda x: x["release_date"] if x["release_date"] else "", reverse=True)
        
        return esxi_versions
    except Exception as e:
        print(f"Error scraping ESXi versions: {str(e)}")
        return {"esxi8": [], "esxi7": []}

def scrape_vcenter_versions():
    url = "https://knowledge.broadcom.com/external/article/326316/vmware-vcenter-server-versions-and-build.html"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        vcenter_versions = {
            "vcenter8": [],
            "vcenter7": []
        }
        
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 4:
                    release_name = cols[0].text.strip()
                    if release_name.startswith('vCenter Server 8') or release_name.startswith('vCenter Server 7'):
                        version_info = {
                            "release_name": release_name,
                            "version": cols[1].text.strip(),
                            "release_date": parse_date(cols[2].text.strip()),
                            "build_number": cols[3].text.strip(),
                            "mob_number": cols[4].text.strip() if len(cols) > 4 else "N/A"
                        }
                        if release_name.startswith('vCenter Server 8'):
                            vcenter_versions["vcenter8"].append(version_info)
                        elif release_name.startswith('vCenter Server 7'):
                            vcenter_versions["vcenter7"].append(version_info)
        
        # Sort versions by release date
        for key in vcenter_versions:
            vcenter_versions[key].sort(key=lambda x: x["release_date"] if x["release_date"] else "", reverse=True)
        
        return vcenter_versions
    except Exception as e:
        print(f"Error scraping vCenter versions: {str(e)}")
        return {"vcenter8": [], "vcenter7": []}

def scrape_vcf_versions():
    url = "https://knowledge.broadcom.com/external/article/314608/correlating-vmware-cloud-foundation-vers.html"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        vcf_versions = {
            "vcf5": []
        }
        
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 8:  # VCF table has 8 or more columns
                    version_text = cols[0].text.strip()
                    if '5.' in version_text:  # Look for VCF 5.x versions
                        # Extract version number and build number
                        version_match = re.search(r'(\d+\.\d+\.\d+).*?(\d{4,})', version_text)
                        if version_match:
                            version = version_match.group(1)
                            build = version_match.group(2)
                        else:
                            # Fallback to just finding the version number
                            version_match = re.search(r'(\d+\.\d+\.\d+)', version_text)
                            version = version_match.group(1) if version_match else version_text
                            build = "N/A"
                        
                        version_info = {
                            "version": version,
                            "build": build,
                            "release_date": parse_date(cols[1].text.strip()),
                            "cloud_builder": cols[2].text.strip(),
                            "sddc_manager": cols[3].text.strip(),
                            "vcenter": cols[4].text.strip(),
                            "esxi": cols[5].text.strip(),
                            "vsan_witness": cols[6].text.strip(),
                            "nsx": cols[7].text.strip(),
                            "aria_suite": cols[8].text.strip() if len(cols) > 8 else "N/A"
                        }
                        vcf_versions["vcf5"].append(version_info)
        
        # Sort versions by release date
        for key in vcf_versions:
            vcf_versions[key].sort(key=lambda x: x["release_date"] if x["release_date"] else "", reverse=True)
        
        return vcf_versions
    except Exception as e:
        print(f"Error scraping VCF versions: {str(e)}")
        return {"vcf5": []}

def save_versions():
    vmware_tools = scrape_vmware_tools()
    esxi_versions = scrape_esxi_versions()
    vcenter_versions = scrape_vcenter_versions()
    vcf_versions = scrape_vcf_versions()
    
    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vmware_tools": sorted(vmware_tools, key=lambda x: x["release_date"] if x["release_date"] else "", reverse=True),
        "esxi_versions": esxi_versions,
        "vcenter_versions": vcenter_versions,
        "vcf_versions": vcf_versions
    }
    
    with open('vmware_versions.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    return data

if __name__ == "__main__":
    save_versions() 