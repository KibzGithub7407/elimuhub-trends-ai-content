"""
Main entry point for Elimuhub Trends AI Content Generator.

This module orchestrates the daily content generation pipeline:
1. Fetches trending topics in Kenya
2. Generates educational content for each topic
3. Publishes to multiple platforms
4. Logs all activities
"""

import logging
import sys
from datetime import datetime
from typing import List
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/content_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

try:
    from src.trends.fetcher import fetch_trending_topics
    from src.generation.generator import generate_elimuhub_post
    from src.publishing.publisher import publish_post
    from src.utils.config import load_config
    from src.utils.database import init_database
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)


def ensure_directories():
    """Ensure all necessary directories exist."""
    directories = [
        'data/logs',
        'data/generated',
        'data/metrics',
        'data/cache'
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


def process_topics(topics: List[str], config: dict) -> dict:
    """
    Process each trending topic and generate content.
    
    Args:
        topics: List of trending topics to process
        config: Configuration dictionary
    
    Returns:
        Dictionary with processing statistics
    """
    stats = {
        'total_topics': len(topics),
        'successful_generations': 0,
        'failed_generations': 0,
        'published_posts': 0,
        'errors': []
    }
    
    for idx, topic in enumerate(topics, 1):
        try:
            logger.info(f"[{idx}/{len(topics)}] Processing topic: {topic}")
            
            # Generate content for the topic
            logger.debug(f"Generating content for: {topic}")
            title, content, tags = generate_elimuhub_post(topic, config)
            
            if not title or not content:
                raise ValueError(f"Empty content generated for topic: {topic}")
            
            stats['successful_generations'] += 1
            logger.info(f"✅ Successfully generated content: {title}")
            
            # Publish the post
            if config.get('auto_publish', True):
                logger.debug(f"Publishing post: {title}")
                publish_result = publish_post(title, content, tags, config)
                
                if publish_result.get('success', False):
                    stats['published_posts'] += 1
                    logger.info(f"🚀 Successfully published: {title}")
                else:
                    error_msg = f"Publication failed for {topic}: {publish_result.get('error')}"
                    logger.warning(error_msg)
                    stats['errors'].append(error_msg)
            else:
                logger.info(f"⏭️  Auto-publish disabled. Content ready for: {topic}")
                
        except Exception as e:
            stats['failed_generations'] += 1
            error_msg = f"Error processing topic '{topic}': {str(e)}"
            logger.error(error_msg, exc_info=True)
            stats['errors'].append(error_msg)
    
    return stats


def log_statistics(stats: dict):
    """Log and display processing statistics."""
    logger.info("=" * 60)
    logger.info("📊 CONTENT GENERATION STATISTICS")
    logger.info("=" * 60)
    logger.info(f"Total Topics Processed: {stats['total_topics']}")
    logger.info(f"✅ Successful Generations: {stats['successful_generations']}")
    logger.info(f"❌ Failed Generations: {stats['failed_generations']}")
    logger.info(f"🚀 Published Posts: {stats['published_posts']}")
    
    if stats['errors']:
        logger.warning(f"⚠️  Errors Encountered: {len(stats['errors'])}")
        for error in stats['errors']:
            logger.warning(f"  - {error}")
    
    logger.info("=" * 60)
    
    # Calculate success rate
    if stats['total_topics'] > 0:
        success_rate = (stats['successful_generations'] / stats['total_topics']) * 100
        logger.info(f"Success Rate: {success_rate:.1f}%")


def main():
    """
    Main orchestration function for content generation pipeline.
    """
    start_time = datetime.now()
    logger.info(f"🚀 Starting Elimuhub Content Generation Pipeline")
    logger.info(f"⏰ Execution Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Step 1: Ensure directories exist
        ensure_directories()
        
        # Step 2: Load configuration
        logger.info("📋 Loading configuration...")
        config = load_config()
        logger.info("✅ Configuration loaded successfully")
        
        # Step 3: Initialize database
        logger.info("🗄️  Initializing database...")
        init_database(config)
        logger.info("✅ Database initialized")
        
        # Step 4: Fetch trending topics
        logger.info("📊 Fetching trending topics in Kenya...")
        topics = fetch_trending_topics(config)
        
        if not topics:
            logger.warning("⚠️  No trending topics found!")
            return
        
        logger.info(f"✅ Found {len(topics)} trending topics")
        for topic in topics:
            logger.debug(f"  - {topic}")
        
        # Step 5: Process all topics
        logger.info("🔄 Processing topics and generating content...")
        stats = process_topics(topics, config)
        
        # Step 6: Log statistics
        log_statistics(stats)
        
        # Calculate and log execution time
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"✅ Pipeline completed in {duration:.2f} seconds")
        
    except Exception as e:
        logger.critical(f"❌ Critical error in main pipeline: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
