from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests

# Create FastAPI Router
router = APIRouter()

class FileScanRequest(BaseModel):
    file_path: str

class VirusDetection:
    """
    Detect if a file contains a virus using VirusTotal API.
    """
    def __init__(self, api_key: str,config,agent):
        self.api_key = api_key
        self.api_url = "https://www.virustotal.com/api/v3/files"
        self.config = config
        self.agent = agent
    def scan_file(self, file_path: str) -> dict:
        """
        Scan a single file for viruses.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        headers = {"x-apikey": self.api_key}
        with open(file_path, "rb") as file:
            response = requests.post(self.api_url, headers=headers, files={"file": file})

        if response.status_code == 200:
            data = response.json()
            file_id = data.get("data", {}).get("id")

            # Fetch analysis results
            analysis_url = f"https://www.virustotal.com/api/v3/analyses/{file_id}"
            analysis_response = requests.get(analysis_url, headers=headers)

            if analysis_response.status_code == 200:
                analysis_data = analysis_response.json()
                stats = analysis_data.get("data", {}).get("attributes", {}).get("stats", {})
                malicious = stats.get("malicious", 0)

                return {"malicious_count": malicious, "is_virus_detected": malicious > 0}
            else:
                raise Exception("Failed to retrieve analysis results.")
        else:
            raise Exception(f"File upload failed with status code: {response.status_code}")

@router.post("/tools/virus_detection", summary="Scan a file for viruses")
def scan_file_endpoint(request: FileScanRequest):
    """
    API Endpoint: Scan a file for viruses.
    """
    api_key = os.getenv("VIRUSTOTAL_API_KEY", "your_api_key_here")
    detector = VirusDetection(api_key=api_key)

    try:
        # Call the scan_file method directly without using an HTTP request
        result = detector.scan_file(request.file_path)
        return {"status": "success", "data": result}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
