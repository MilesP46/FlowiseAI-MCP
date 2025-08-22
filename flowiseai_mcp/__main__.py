"""Entry point for the FlowiseAI MCP server"""

import sys
import os
import logging

# Set up logging to stderr to avoid interfering with MCP protocol on stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point with error handling"""
    try:
        # Import server module
        from .server import main as server_main
        
        # Log startup
        logger.info("Starting FlowiseAI MCP Server...")
        logger.info(f"FLOWISEAI_URL: {os.getenv('FLOWISEAI_URL', 'not set')}")
        logger.info(f"FLOWISEAI_API_KEY: {'set' if os.getenv('FLOWISEAI_API_KEY') else 'not set'}")
        
        # Run the server
        server_main()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()