from typing import Annotated, TypedDict, List, Dict, Optional, Any
import operator

# Defining the structure for single compliance 
#Error report format
class ComplianceIssue(TypedDict):
    category:str
    description:str #details of violations
    severity:str #Critical | Warning
    timestamp:Optional[str]
    
    
# Define the global graph state

class VideoAuditState(TypedDict):
    """Defines the data schema for langgraph execution content
        Main container : Holds all the info about the audit
        URL --->>> Final Report
    """
    
    #input parameters
    video_url:str
    video_id:str
    
    #ingestion and extraction data
    local_file_path:Optional[str]
    video_metadata : Dict[str,Any] 
    transcript : Optional[str] # extracted speech to text
    OCR_text : List[str] # texts appeared in the video 
    
    #analysis output
    # stores list of all violations
    compliance_results : Annotated[List[ComplianceIssue], operator.add] #operator.add will add all the new issuses that are founded by any of the node
    
    #final deliverables
    final_status : str # Pass Fail
    final_report : str # Markdown format
    
    #system observability
    #system level crashes
    # errors : API timeout, system level errors
    errors : Annotated[List[str],operator.add]
    