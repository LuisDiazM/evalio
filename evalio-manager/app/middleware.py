import base64
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class JWTExtractorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            # Extract the token
            token = auth_header.split(" ")[1]
            try:
                # Split the token and get the payload (second part)
                payload = token.split(".")[1]
                # Add padding if necessary
                payload += "=" * (-len(payload) % 4)
                # Decode the payload
                decoded_payload = base64.b64decode(payload)
                # Parse the JSON
                token_data = json.loads(decoded_payload)
                
                # Extract professor_id
                professor_id = token_data.get("professor_id")
                professor_name = token_data.get("name")
                if professor_id and professor_name:
                    # Add professor_id as a header
                    request.headers.__dict__["_list"].append(
                        (b"x-professor-id", professor_id.encode()),
                    )
                    request.headers.__dict__["_list"].append(
                        (b"x-professor-name", professor_name.encode()),
                    )
            except Exception:
                # If there's any error in processing the token, continue without the header
                pass
        
        # Continue with the request
        response = await call_next(request)
        return response 