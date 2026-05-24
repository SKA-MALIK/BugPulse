import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.config import settings
from app.database import SessionLocal
from app.services import ExternalAPIClient, GoogleChatNotifier, BugService

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = BackgroundScheduler()


def sync_bugs_job():
    """Job to sync bugs from external API and send notifications"""
    logger.info("Starting bug sync job")
    
    try:
        # Initialize clients
        api_client = ExternalAPIClient(settings.EXTERNAL_API_URL, settings.EXTERNAL_API_KEY)
        chat_notifier = GoogleChatNotifier(settings.GOOGLE_CHAT_WEBHOOK_URL)
        
        # Fetch bugs from external API
        external_bugs = api_client.fetch_bugs()
        
        if not external_bugs:
            logger.info("No bugs fetched from external API")
            return
        
        # Get database session
        db: Session = SessionLocal()
        
        try:
            for bug_data in external_bugs:
                # Extract bug data
                external_id = str(bug_data.get("id") or bug_data.get("bug_id", ""))
                title = bug_data.get("title", "Unknown")
                description = bug_data.get("description", "")
                severity = bug_data.get("severity", "medium")
                
                if not external_id:
                    logger.warning(f"Skipping bug with missing external_id: {bug_data}")
                    continue
                
                # Get or create bug
                bug, is_new = BugService.get_or_create_bug(
                    db, external_id, title, description, severity
                )
                
                # Send notification for new bugs
                if is_new:
                    logger.info(f"New bug detected: {title}")
                    if chat_notifier.send_notification(title, description, severity):
                        BugService.mark_as_notified(db, bug.id)
                    else:
                        logger.warning(f"Failed to send notification for bug {bug.id}")
            
            logger.info("Bug sync job completed successfully")
            
        except Exception as e:
            logger.error(f"Error during bug sync job: {str(e)}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in sync_bugs_job: {str(e)}")


def start_scheduler():
    """Start the background scheduler"""
    try:
        if not scheduler.running:
            # Add sync job
            scheduler.add_job(
                sync_bugs_job,
                'interval',
                minutes=settings.SCHEDULER_INTERVAL,
                id='sync_bugs_job',
                name='Sync bugs from external API',
                replace_existing=True,
                max_instances=1
            )
            
            scheduler.start()
            logger.info(f"Scheduler started - runs every {settings.SCHEDULER_INTERVAL} minutes")
        else:
            logger.info("Scheduler is already running")
            
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")
        raise


def stop_scheduler():
    """Stop the background scheduler"""
    try:
        if scheduler.running:
            scheduler.shutdown()
            logger.info("Scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {str(e)}")
