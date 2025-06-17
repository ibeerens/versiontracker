from http.server import HTTPServer, BaseHTTPRequestHandler
from app import app
import json

def handler(event, context):
    """Handle the incoming request"""
    try:
        # Get the request path and method
        path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        
        # Create a test request context
        with app.test_request_context(path=path, method=method):
            # Process the request
            response = app.full_dispatch_request()
            
            # Return the response
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        } 