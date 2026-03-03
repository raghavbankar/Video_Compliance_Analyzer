#chunking of pdf data 

import os
import glob
import logging
from dotenv import load_dotenv
load_dotenv(override=True)

#document loaders and splitters
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#azure Components
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

#setup logging

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger=logging.getlogger("indexer")

def index_docs():
    """
    Reads the PDFs , chunks them and upload them to Azure AI search
    """
    
    # define paths, Data folder
    current_dir=os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir,"../../backend/data")
    
    # Checking the environment variables
    logger.info("="*60)
    logger.info("Environment Confifuration Check: ")
    logger.info(f"AZURE_OPENAI_ENDPOINT : {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    logger.info(f"AZURE_OPENAI_API_VERSION : {os.getenv('AZURE_OPENAI_API_VERSION')}")
    logger.info(f"AZURE_OPENAI_EMBEDDING_DEPLOYMENT : {os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT',"text-embedding-3-small")}")
    logger.info(f"AZURE_SEARCH_ENDPOINT : {os.getenv('AZURE_SEARCH_ENDPOINT')}")
    logger.info(f"AZURE_SEARCH_INDEX_NAME : {os.getenv('AZURE_SEARCH_INDEX_NAME')}")
    logger.info("="*60)
                        
    #validate the required env variables
    required_vars=[
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_API_KEY",
        "AZURE_SEARCH_INDEX_NAME"
    ]
    
    #checking the variables and getting the missing variables and logging the errors
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables :{missing_vars}")
        logger.error("Please check your .env file and ensure all the variables are set")
        return
    
    #initialize the embeddings model
    #turns text into vectors
    
    try:
        logger.info("Initializing Azure OpenAI Embeddings....")
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT',"text-embedding-3-small"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION","2024-02-01")
        )
        
        logger.info("Embeddings model initialized successfully")
    
    except Exception as e:
        logger.error(f"Failed to initialize the embeddings: {e}")
        logger.error("Please verify your Azure OpenAI deployment credentials")
        return
    
    #initialize the azure search
    try:
        logger.info("Initializing Azure AI Search Vector store")
        vector_store= AzureSearch(
            index_name=os.getenv('AZURE_SEARCH_INDEX_NAME'),
            azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            azure_search_key=os.getenv("AZURE_SEARCH_API_KEY"),
            embedding_function=embeddings.embed_query
        )
        logger.info("Azure AI Search initialized successfully : {index_name}")
    
    except Exception as e:
        logger.error(f"Failed to initialize the AI Search: {e}")
        logger.error("Please verify your Azure Search credentials")
        return
    
    #Find the PDF files
    pdf_files = glob.glob(os.path.join(data_folder,"*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDFs found in {data_folder}. Please add files")
    logger.info(f"Found {len(pdf_files)} PDFs to process: {[os.path.basename(f) for f in pdf_files]}")
    
    # to store chunks
    all_splits =[]
    
    #process each pdf
    for pdf_path in pdf_files:
        try:
            logger.info(f"Loading: {os.path.basename(pdf_path)}............")
            loader=PyPDFLoader(pdf_path)
            raw_docs = loader.load()
            
            #chuncking strategy for the docs retrieved
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            splits=text_splitter.split_documents(raw_docs)
            for split in splits:
                split.metadata["source"] = os.path.basename(pdf_path)
                
            all_splits.extend(splits)
            
            logger.info(f"Splited into {len(splits)} chunks")
        
        except Exception as e:
            logger.error(f"Failed to process {pdf_path} : {e}")
            
        #Upload to Azure
        if all_splits:
            logger.info(f"Uploading {len(all_splits)} chunks to Azure AI search Index '{index_name}'")
            try:
                # azure search accepts batches automatically via this method
                
                vector_store.add_documents(all_splits)
                logger.info("="*60)
                logger.info("Indexing Complete! Knowledge Base is ready....")
                logger.info(f"Total chunks indexed : {len(all_splits)}")
                logger.info("="*60)
            
            except Exception as e:
                logger.error(f"Failed to upload the documents to Azure Search")
                logger.error(f"Check the Azure search configuration and try again")
                
        else:
            logger.warning("No documents were processed")
            

if __name__=="__main__":
    index_docs()

