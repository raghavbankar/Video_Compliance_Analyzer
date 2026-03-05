"""
Main Execution Entry point for the Compliance QA Pipeline
Orchestration part 
This file is the "control center" that starts and manages the entire 
compliance audit workflow. Think of it as the master switch that:
1. Sets up the audit request
2. Runs the AI workflow
3. Displays the final compliance report
"""

import uuid,json
import logging
from pprint import pprint

from dotenv import load_dotenv
load_dotenv(override=True)

# importing the main workflow graph 
from backend.src.graph.workflow import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger("Video-Complianve-runner")

def run_cli_simulation():
    """
    Simulates a Video Compliance Audit request.
    
    This function orchestrates the entire audit process:
    - Creates a unique session ID
    - Prepares the video URL and metadata
    - Runs it through the AI workflow
    - Displays the compliance results
    """
    
    # generate the session ID
    session_id = str(uuid.uuid4())
    logger.info(f"Starting Audit Session : {session_id}")
    
    # Define the initial inputs Dictionary that contains all the input data for the workflow
    initial_inputs ={
        # Youtube video URL
        "video_url": "https://youtu.be/dT7S75eYhcQ",
        # Shortend Video ID (first 8 characters of session ID)
        "video_id"  : f"vid_{session_id[:8]}",
        #Empty list that will store compliance violations found
        "compliance_results" : [],
        #Empty list for any errors during processing
        "errors" : []
    }
    
    print("n-------Initializing Workflow.............")
    print(f"Input Payload : {json.dumps(initial_inputs, indent=2)}")
    
    try:
        #Executing the graph
        #START -> Indexer -> Auditor -> END
        final_state = app.invoke(initial_inputs)
        
        ## Display Section
        print("\n---------Workflow execution is complete.........")
        
        print("\n Compliance Audit Report ==")
        # shows the Vidoe ID
        print(f"Video ID : {final_state.get('video_id')}")
        # shows pass or fail status
        print(f"Status : {final_state.get('final_status')}")
        
        ### Violations Section 
        print("\n [VIOLATIONS DETECTED]")
        
        # Extract the list of compliance violations
        results = final_state.get('compliance_results',[])
        if results:
            # Loop through each violations and display it
            for issue in results:
                print(f"-- [{issue.get('severity')}] : [{issue.get('category')}] : [{issue.get('description')}]")
        else:
            print("No violations Detected......")
            
        print("\n[FINAL SUMMARY]")
        # Displays the AI generated natural language summary
        print(final_state.get('final_report'))
    
    except Exception as e:
        logger.error(f"Workflow Execution Failed : {str(e)}")
        raise e
    
#Entry point
if __name__ == "__main__":
    run_cli_simulation()
    

        