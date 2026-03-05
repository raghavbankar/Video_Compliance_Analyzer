# Azure opentelemetry integration

import os
import logging
from azure.monitor.opentelemetry import configure_azure_monitor

logger = logging.getLogger("Video_compliance-Telemetry")

def setup_telementry():
    """
    Initializes the Azure Monitor Opentelemetry
    Tracks : HTTP requests, database queries, errors, performance metrics
    Sents this data to azure monitor
    
    It auto captures every API request
    No need to manually log each end point
    """
    
    # retrieve connection string
    
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    # Checking if configured 
    if not connection_string:
        logger.warning("No instrumentation  key found. Telemtry is Disabled")
        return
    
    #Configured the azure monitor
    
    try:
        #register the automatic requests for HTTP request
        #starts a background threads to send the data to azure monitor
        configure_azure_monitor(
            connection_string=connection_string,
            logger_name="Video_Compliance-Tracer"
        )
        logger.info("Azure Monitor tracking enabled and connected")
    
    except Exception as e:
        logger.error(f"Failed to Initialize Azure Monitor: {e}")
        

        

    