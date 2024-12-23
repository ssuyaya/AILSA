from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from pydantic import BaseModel, Field
import os
import requests
import shutil

router = APIRouter()

# 病毒检测工具类
class VirusDetectionTool:
    def __init__(self, api_url: str, api_key: str) -> None:
        self.api_url = api_url
        self.api_key = api_key

    def detect_virus(self, file_path: str) -> dict:
        """
        Upload file to VirusTotal API and analyze the results.
        """
        headers = {"x-apikey": self.api_key}
        try:
            with open(file_path, "rb") as file:
                # Upload file for analysis
                response = requests.post(f"{self.api_url}/files", headers=headers, files={"file": file})
                response.raise_for_status()
                data = response.json()
                file_id = data["data"]["id"]

            # Fetch analysis results
            analysis_url = f"{self.api_url}/analyses/{file_id}"
            analysis_response = requests.get(analysis_url, headers=headers)
            analysis_response.raise_for_status()
            return analysis_response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

# 初始化病毒检测工具
virus_tool = VirusDetectionTool(
    api_url="https://www.virustotal.com/api/v3",  # 修改为你的 VirusTotal API URL
    api_key=os.getenv("VIRUSTOTAL_API_KEY", "your_api_key_here")
)

# 请求数据模型
class VirusScanQueryItem(BaseModel):
    file: UploadFile = File(...)

# 路由实现
@router.post("/tools/virus_detection", summary="A tool to scan files for viruses and analyze results.")
async def virus_detection(item: VirusScanQueryItem = Depends()):
    try:
        # 临时存储上传的文件
        with open(item.file.filename, "wb") as buffer:
            shutil.copyfileobj(item.file.file, buffer)

        # 调用病毒检测工具
        analysis_result = virus_tool.detect_virus(file_path=item.file.filename)

        # 清理临时文件
        os.remove(item.file.filename)

        # 分析结果
        stats = analysis_result.get("data", {}).get("attributes", {}).get("stats", {})
        malicious_count = stats.get("malicious", 0)
        harmless_count = stats.get("harmless", 0)
        suspicious_count = stats.get("suspicious", 0)

        # 输出分析结果
        return {
            "file_name": item.file.filename,
            "malicious_count": malicious_count,
            "harmless_count": harmless_count,
            "suspicious_count": suspicious_count,
            "is_virus_detected": malicious_count > 0,
        }
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
