#!/usr/bin/env python
"""
Application entry point for BugPulse
"""

import sys
import logging
from app.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Run the application"""
    try:
        import uvicorn
        
        logger.info("Starting BugPulse API Server")
        logger.info(f"Debug Mode: {settings.DEBUG}")
        logger.info(f"Log Level: {settings.LOG_LEVEL}")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error running application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
