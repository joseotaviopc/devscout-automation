import asyncio
import logging
import schedule
import time
from datetime import datetime
import os
from dotenv import load_dotenv

from main import DevScoutAutomation

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("devscout.log"), logging.StreamHandler()],
)


def run_automation_job():
    """Run the automation job"""
    logging.info("=" * 50)
    logging.info(f"Starting scheduled automation job at {datetime.now()}")

    try:
        # Run the async automation
        automation = DevScoutAutomation()
        success = asyncio.run(automation.run_automation())

        if success:
            logging.info("✅ Scheduled automation completed successfully!")
        else:
            logging.error("❌ Scheduled automation failed!")

    except Exception as e:
        logging.error(f"Scheduled job error: {e}")

    logging.info("=" * 50)


def setup_scheduler():
    """Setup the daily scheduler"""
    schedule_time = os.getenv("SCHEDULE_TIME", "09:00")

    # Schedule daily job
    schedule.every().day.at(schedule_time).do(run_automation_job)

    logging.info(f"Scheduler setup complete - will run daily at {schedule_time}")
    logging.info("Press Ctrl+C to stop the scheduler")


def main():
    """Main scheduler function"""
    setup_scheduler()

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")


if __name__ == "__main__":
    main()
