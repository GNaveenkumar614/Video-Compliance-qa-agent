import operator
from typing import Annotated, List, Dict, Optional, Any, TypedDict

# 1. Define the Schema for a Single Compliance Result
class ComplianceIssue(TypedDict):
    category: str           # e.g., "FTC_DISCLOSURE"
    description: str        # Specific detail of the violation
    severity: str           # "CRITICAL" | "WARNING"
    timestamp: Optional[str]# Timestamp of occurrence (if applicable)

# 2. Define the Global Graph State
class VideoAuditState(TypedDict):
    """
    Defines the data schema for the LangGraph execution context.
    """
    # --- Input Parameters ---
    video_url: str
    video_id: str

    # --- Ingestion & Extraction Data ---

    local_file_path: Optional[str]  
    video_metadata: Dict[str, Any]  # e.g., {"duration": 15, "resolution": "1080p"}
    transcript: Optional[str]       
    ocr_text: List[str]             

    # --- Analysis Output ---
    # annotated with operator.add to allow append-only updates from multiple nodes.
    compliance_results: Annotated[List[ComplianceIssue], operator.add]
    
    # --- Final Deliverables ---
    final_status: str               # "PASS" | "FAIL"
    final_report: str               #  summary for the frontend
    
    # --- System Observability ---

    errors: Annotated[List[str], operator.add]  # Appends system-level errors