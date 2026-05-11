"""
COMPLETE AUTONOMOUS MEDIA ENGINE PIPELINE 🚀
5-Agent Orchestration: Trend → Script → Video → Publish → Monetize

Flow:
1. Agent 1: TrendScout → Detecta tendencias virales
2. Agent 2: Copywriter → Genera guiones optimizados
3. Agent 3: VideoProducer → Compila vídeos (MoviePy + ElevenLabs)
4. Agent 4: Publisher → Publica en 3 plataformas (TikTok, Instagram, YouTube)
5. Agent 5: MonetizationTracker → Trackea ingresos en tiempo real

Costos totales: €0-5/mes (free tier APIs + free stock)
"""

import asyncio
import logging
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import agents
from agents.agent_1_trends import TrendScout
from agents.agent_2_copywriter import Copywriter
from agents.agent_3_video import VideoProducer
from agents.agent_4_publisher import Publisher
from agents.agent_5_monetization import MonetizationTracker

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AutonomousMediaEngine:
    """Orquestador de 5 agentes para contenido viral automático"""

    def __init__(self, region: str = "es"):
        self.region = region
        self.output_dir = project_root / "output" / "pipeline"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize agents
        self.trend_scout = TrendScout(region=region)
        self.copywriter = Copywriter(region=region)
        self.video_producer = VideoProducer(region=region)
        self.publisher = Publisher(region=region)
        self.monetization_tracker = MonetizationTracker(region=region)

        logger.info("🚀 Autonomous Media Engine initialized")

    async def run_daily_pipeline(self, num_videos: int = 1) -> Dict[str, Any]:
        """
        Ejecuta el pipeline completo diariamente.
        
        Genera `num_videos` vídeos virales, los publica en 3 plataformas
        y comienza a trackear monetización.
        """
        try:
            logger.info(f"🎬 Starting daily pipeline: {num_videos} videos")
            
            results = []
            published_videos = []

            for i in range(num_videos):
                logger.info(f"\n{'='*60}")
                logger.info(f"📹 VIDEO {i+1}/{num_videos}")
                logger.info(f"{'='*60}\n")

                # Step 1: Find trends
                logger.info("🔍 STEP 1: Detecting trends...")
                trend_result = await self.trend_scout.execute({
                    "keywords": ["AI", "tech", "productivity"],
                    "limit": 1
                })

                if trend_result["status"] != "success":
                    logger.error(f"❌ Trend detection failed: {trend_result.get('error')}")
                    continue

                trend_data = trend_result["result"][0]
                logger.info(f"✅ Trend found: {trend_data['topic']} (score: {trend_data['trend_score']})")

                # Step 2: Generate script
                logger.info("\n✍️ STEP 2: Generating viral script...")
                script_result = await self.copywriter.execute({
                    "topic": trend_data["topic"],
                    "trend_score": trend_data["trend_score"],
                    "target_emotion": trend_data.get("target_emotion", "curiosity"),
                    "duration_seconds": 60
                })

                if script_result["status"] != "success":
                    logger.error(f"❌ Script generation failed: {script_result.get('error')}")
                    continue

                script = script_result["result"]["script"]
                logger.info(f"✅ Script generated ({len(script)} chars)")

                # Step 3: Produce video
                logger.info("\n🎥 STEP 3: Producing video...")
                video_result = await self.video_producer.execute({
                    "trend_title": trend_data["topic"],
                    "script": script,
                    "duration_seconds": 60,
                    "platform": "tiktok"
                })

                if video_result["status"] != "success":
                    logger.error(f"❌ Video production failed: {video_result.get('error')}")
                    continue

                video_path = video_result["result"]["video_path"]
                logger.info(f"✅ Video produced: {Path(video_path).name} ({video_result['result']['file_size_mb']}MB)")

                # Step 4: Publish to platforms
                logger.info("\n📱 STEP 4: Publishing to 3 platforms...")
                publish_result = await self.publisher.execute({
                    "video_path": video_path,
                    "title": trend_data["topic"],
                    "description": f"Latest trend: {trend_data['topic']}. 🚀 #AI #Tech #Trending",
                    "tags": ["AI", "tech", "trending"],
                    "platforms": ["tiktok", "instagram", "youtube"]
                })

                if publish_result["status"] != "success":
                    logger.error(f"❌ Publishing failed: {publish_result.get('error')}")
                    continue

                published_results = publish_result["result"]["results"]
                platforms_count = publish_result["result"]["platforms_published"]
                logger.info(f"✅ Published to {platforms_count}/3 platforms")

                # Track video IDs for monetization
                for platform_result in published_results:
                    if platform_result["upload_status"] == "published":
                        published_videos.append({
                            "platform": platform_result["platform"],
                            "video_id": platform_result["video_id"],
                            "url": platform_result["video_url"]
                        })

                # Store result
                results.append({
                    "trend": trend_data["topic"],
                    "video_path": video_path,
                    "published_platforms": platforms_count,
                    "published_at": datetime.now().isoformat()
                })

            # Step 5: Track monetization
            if published_videos:
                logger.info("\n💰 STEP 5: Tracking monetization...")
                monetization_result = await self.monetization_tracker.execute({
                    "video_ids": published_videos
                })

                if monetization_result["status"] == "success":
                    stats = monetization_result["result"]
                    logger.info(f"✅ Monetization tracking started")
                    logger.info(f"   Total views (est.): {stats['total_views']:,}")
                    logger.info(f"   Total likes (est.): {stats['total_likes']:,}")
                    logger.info(f"   Revenue (est.): €{stats['total_revenue_estimate']:.2f}")

            # Save pipeline execution record
            pipeline_record = {
                "executed_at": datetime.now().isoformat(),
                "videos_generated": len(results),
                "videos_published": len(published_videos),
                "results": results,
                "published_videos": published_videos
            }

            record_path = self.output_dir / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(record_path, 'w', encoding='utf-8') as f:
                json.dump(pipeline_record, f, indent=2, ensure_ascii=False)

            logger.info(f"\n{'='*60}")
            logger.info(f"✅ DAILY PIPELINE COMPLETED")
            logger.info(f"{'='*60}")
            logger.info(f"Videos generated: {len(results)}")
            logger.info(f"Videos published: {len(published_videos)}")
            logger.info(f"Record saved: {record_path}")

            return {
                "status": "success",
                "videos_generated": len(results),
                "videos_published": len(published_videos),
                "published_videos": published_videos,
                "record_path": str(record_path)
            }

        except Exception as e:
            logger.error(f"❌ Pipeline error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


async def main():
    """Main entry point"""
    
    # Initialize engine
    engine = AutonomousMediaEngine(region="es")

    # Run daily pipeline (generate 1 video for testing)
    result = await engine.run_daily_pipeline(num_videos=1)

    print("\n" + "="*70)
    print("🎬 AUTONOMOUS MEDIA ENGINE - DAILY EXECUTION SUMMARY")
    print("="*70)
    print(f"Status: {result['status']}")
    print(f"Videos Generated: {result['videos_generated']}")
    print(f"Videos Published: {result['videos_published']}")
    
    if result['status'] == 'success' and result['published_videos']:
        print(f"\n📱 Published Videos:")
        for video in result['published_videos']:
            print(f"  - {video['platform'].upper()}: {video['url']}")
    
    print(f"\nRecord: {result['record_path']}")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
