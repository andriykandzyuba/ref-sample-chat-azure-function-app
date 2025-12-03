import azure.functions as func
import logging
import json
from datetime import datetime

app = func.FunctionApp()

@app.route(route="chat", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def chat_api(req: func.HttpRequest) -> func.HttpResponse:
    """
    Chat API endpoint that accepts POST requests with JSON payload.
    Logs all requests to console and returns a response.
    """
    logging.info('Chat API endpoint triggered')
    
    # Log request details
    logging.info(f'Request method: {req.method}')
    logging.info(f'Request URL: {req.url}')
    logging.info(f'Headers: {dict(req.headers)}')
    
    try:
        # Parse request body
        req_body = req.get_json()
        logging.info(f'Request body: {json.dumps(req_body, indent=2)}')
        
        # Extract message from request
        message = req_body.get('message', '')
        user_id = req_body.get('user_id', 'anonymous')
        
        if not message:
            logging.warning('Empty message received')
            return func.HttpResponse(
                json.dumps({
                    "error": "Message field is required",
                    "timestamp": datetime.utcnow().isoformat()
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        # Log the conversation
        logging.info(f'User: {user_id}, Message: {message}')
        
        # Create response
        response_data = {
            "status": "success",
            "user_id": user_id,
            "message_received": message,
            "response": f"Echo: {message}",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logging.info(f'Response: {json.dumps(response_data, indent=2)}')
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        logging.error(f'Invalid JSON in request: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "Invalid JSON format",
                "timestamp": datetime.utcnow().isoformat()
            }),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f'Error processing request: {str(e)}', exc_info=True)
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "timestamp": datetime.utcnow().isoformat()
            }),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint for monitoring and load balancers.
    """
    logging.info('Health check endpoint triggered')
    
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }),
        status_code=200,
        mimetype="application/json"
    )
