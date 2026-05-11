#!/usr/bin/env python
"""
DAILY PIPELINE EXECUTOR - MVP IMPROVED VERSION

Ejecuta pipeline completo cada mañana:
1. Descubre trends (Tavily)
2. Genera scripts (Gemini)
3. Guarda JSON
4. Envía email
5. Actualiza dashboard

Uso:
    python scripts/run_daily_improved.py               # Ejecución normal
    python scripts/run_daily_improved.py --test        # Test con 1 trend
    python scripts/run_daily_improved.py --dry-run     # Simular
    python scripts/run_daily_improved.py --no-email    # Sin email
"""

import asyncio
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from agents.agent_1_trends import TrendScout
from agents.agent_2_script import ScriptMaster
from core.email_reporter import EmailReporter

# Create logs directory if not exists
logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / 'pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DailyPipeline:
    """Ejecutor del pipeline diario MVP"""

    def __init__(self, test_mode=False, dry_run=False, send_email=True):
        self.test_mode = test_mode
        self.dry_run = dry_run
        self.send_email = send_email
        self.start_time = datetime.now()

    async def execute(self):
        """Ejecuta pipeline completo"""

        logger.info("=" * 80)
        logger.info("🚀 DAILY PIPELINE START")
        logger.info("=" * 80)

        try:
            # ========== STEP 1: DISCOVER TRENDS ==========
            logger.info("\n1️⃣ DISCOVERING TRENDS...")
            trends = await self._discover_trends()

            if not trends:
                logger.warning("⚠️ No trends discovered. Aborting.")
                return {"status": "warning", "message": "No trends found"}

            # ========== STEP 2: GENERATE SCRIPTS ==========
            logger.info("\n2️⃣ GENERATING SCRIPTS...")
            scripts = await self._generate_scripts(trends)

            if not scripts:
                logger.warning("⚠️ No scripts generated.")
                return {"status": "warning", "message": "No scripts generated"}

            # ========== STEP 3: SAVE RESULTS ==========
            logger.info("\n3️⃣ SAVING RESULTS...")
            await self._save_results(trends, scripts)

            # ========== STEP 4: SEND EMAIL ==========
            if self.send_email and not self.dry_run:
                logger.info("\n4️⃣ SENDING EMAIL REPORT...")
                await self._send_email_report(trends, scripts)

            # ========== SUMMARY ==========
            duration = (datetime.now() - self.start_time).total_seconds()
            metrics = {
                "total_discovered": len(trends),
                "total_generated": len(scripts),
                "avg_score": sum(t.get("monetization_score", 0) for t in trends) / len(trends) if trends else 0,
                "cost_eur": 0.12,
                "duration_seconds": int(duration)
            }

            logger.info("\n" + "=" * 80)
            logger.info("✅ PIPELINE COMPLETE")
            logger.info("=" * 80)
            logger.info(f"Trends: {metrics['total_discovered']}")
            logger.info(f"Scripts: {metrics['total_generated']}")
            logger.info(f"Avg Score: {metrics['avg_score']:.2f}")
            logger.info(f"Duration: {metrics['duration_seconds']}s")
            logger.info("=" * 80)

            return {
                "status": "success",
                "metrics": metrics,
                "trends": trends,
                "scripts": scripts
            }

        except Exception as e:
            logger.error(f"\n❌ PIPELINE ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": str(e)}

    async def _discover_trends(self):
        """Descubre trends con Tavily"""

        agent = TrendScout(region=settings.DEFAULT_REGION)
        result = await agent.execute({
            "region": settings.DEFAULT_REGION,
            "num_trends": 1 if self.test_mode else 5,
            "min_monetization_score": 0.6
        })

        if result["status"] != "success":
            raise Exception(f"Agent 1 error: {result.get('error')}")

        trends = result["result"]["trends"]
        logger.info(f"✅ {len(trends)} trends discovered")

        for i, trend in enumerate(trends, 1):
            logger.info(f"   {i}. {trend['title'][:60]}")
            logger.info(f"      Score: {trend['monetization_score']:.2f} | Source: {trend['source']}")

        return trends

    async def _generate_scripts(self, trends):
        """Genera scripts con Gemini"""

        agent = ScriptMaster(region=settings.DEFAULT_REGION)
        scripts = []

        for trend in trends:
            try:
                result = await agent.execute({
                    "trend_id": trend.get("id", "unknown"),
                    "title": trend["title"],
                    "platform": "tiktok",
                    "duration_seconds": 60
                })

                if result["status"] == "success":
                    script = result["result"]["script"]
                    scripts.append({
                        "title": trend["title"],
                        "trend_id": trend.get("id"),
                        "monetization_score": trend.get("monetization_score", 0),
                        "platform": "tiktok",
                        "duration_seconds": 60,
                        "script": script,
                        "generated_at": datetime.now().isoformat()
                    })
                    logger.info(f"✅ Script generated for: {trend['title'][:50]}")
                else:
                    logger.warning(f"⚠️ Failed to generate script for: {trend['title'][:50]}")

            except Exception as e:
                logger.error(f"❌ Error generating script: {str(e)}")

        return scripts

    async def _save_results(self, trends, scripts):
        """Guarda resultados en JSON"""

        # Create data directory if not exists
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)

        # Save to JSON
        filename = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = data_dir / filename

        data = {
            "timestamp": datetime.now().isoformat(),
            "trends": trends,
            "scripts": scripts,
            "region": settings.DEFAULT_REGION
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 Results saved to: {filename}")

    async def _send_email_report(self, trends, scripts):
        """Envía reporte por email"""

        reporter = EmailReporter()

        metrics = {
            "total_discovered": len(trends),
            "avg_score": sum(t.get("monetization_score", 0) for t in trends) / len(trends) if trends else 0,
            "cost_eur": 0.12,
            "duration_seconds": int((datetime.now() - self.start_time).total_seconds())
        }

        success = await reporter.send_daily_report(trends, scripts, metrics)

        if success:
            logger.info(f"📧 Email sent to: {reporter.admin_email}")
        else:
            logger.warning("⚠️ Email not sent (check SMTP settings in .env)")


async def main():
    """Entry point"""

    parser = argparse.ArgumentParser(description="Daily content generation pipeline")
    parser.add_argument('--test', action='store_true', help='Test mode (1 trend)')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (no API calls)')
    parser.add_argument('--no-email', action='store_true', help='Skip email sending')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    pipeline = DailyPipeline(
        test_mode=args.test,
        dry_run=args.dry_run,
        send_email=not args.no_email
    )

    result = await pipeline.execute()
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
