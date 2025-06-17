from app import app
import json

def handler(event, context):
    """Handle the incoming request"""
    try:
        # Get the request path and method
        path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        query_string = event.get('queryStringParameters', {}) or {}
        headers = event.get('headers', {}) or {}
        body = event.get('body', '')
        
        # Create a test request context with all parameters
        with app.test_request_context(
            path=path,
            method=method,
            query_string=query_string,
            headers=headers,
            data=body
        ):
            # Process the request
            response = app.full_dispatch_request()
            
            # Return the response
            return {
                'statusCode': response.status_code,
                'headers': {
                    'Content-Type': response.headers.get('Content-Type', 'text/html'),
                    'Access-Control-Allow-Origin': '*'
                },
                'body': response.get_data(as_text=True)
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        } 