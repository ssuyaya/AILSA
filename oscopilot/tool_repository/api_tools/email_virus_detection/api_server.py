import os
import dotenv

from fastapi import FastAPI
from oscopilot.utils.server_config import ConfigManager
dotenv.load_dotenv(dotenv_path=".env", override=True)  # Load environment variables

app = FastAPI()

# Import routers for your services
from oscopilot.tool_repository.api_tools.bing.bing_service import router as bing_router
from oscopilot.tool_repository.api_tools.audio2text.audio2text_service import router as audio2text_router
from oscopilot.tool_repository.api_tools.image_caption.image_caption_service import router as image_caption_router
from oscopilot.tool_repository.api_tools.wolfram_alpha.wolfram_alpha import router as wolfram_alpha_router
from oscopilot.tool_repository.api_tools.email_virus_detection.virus_detection_service import router as email_virus_detection_router

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


# Middleware to log incoming and outgoing requests
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Incoming request: {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            print(f"Request error: {str(e)}")
            raise e from None
        else:
            print(f"Outgoing response: {response.status_code}")
        return response


app.add_middleware(LoggingMiddleware)

# Service router mapping
services = {
    "bing": bing_router,  # Bing search, image search, and web loader
    "audio2text": audio2text_router,
    "image_caption": image_caption_router,
    "wolfram_alpha": wolfram_alpha_router,
    "virus_detection": virus_detection_router,  # Virus detection service
}

# List of services to include
server_list = ["bing", "audio2text", "image_caption", "virus_detection"]

# Dynamically include only the routers listed in `server_list`
for service in server_list:
    if service in services:
        app.include_router(services[service])
    else:
        print(f"Service '{service}' is not defined in `services` dictionary.")

# Optional: Apply proxy settings if necessary
# proxy_manager = ConfigManager()
# proxy_manager.apply_proxies()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8079)
