# VMware Version Tracker

This application tracks and displays the latest versions of VMware products:
- VMware Tools versions
- ESXi 8.x versions
- ESXi 7.x versions
- vCenter Server 8.x versions
- vCenter Server 7.x versions

The application scrapes version information from Broadcom's knowledge base and displays it in a clean web interface.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create the templates directory (if it doesn't exist):
```bash
mkdir templates
```

## Usage

1. Run the initial scraper to create the JSON file:
```bash
python vmware_versions.py
```

2. Start the web server:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Features

- Displays the latest versions of:
  - VMware Tools
  - ESXi 8.x
  - ESXi 7.x
  - vCenter Server 8.x
  - vCenter Server 7.x
- Organizes information in clear sections with cards
- Stores all version data in `vmware_versions.json`
- Provides a refresh button to update the data
- Shows last updated timestamp
- Clean and responsive web interface with card layout

## Data Structure

The `vmware_versions.json` file contains:
- Last updated timestamp
- VMware Tools versions array with:
  - Version number
  - Release date
  - Build number
  - Tool internal version
- ESXi versions object with:
  - ESXi 8.x versions array
  - ESXi 7.x versions array
  Each ESXi version includes:
  - Version number
  - Release name
  - Release date
  - Build number
  - Available as (ISO/Patch)
- vCenter versions object with:
  - vCenter 8.x versions array
  - vCenter 7.x versions array
  Each vCenter version includes:
  - Release name
  - Version number
  - Release date
  - Build number
  - MOB number 