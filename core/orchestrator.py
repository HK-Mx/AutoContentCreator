"""
ORQUESTADOR PRINCIPAL: Coordina el flujo completo de todos los agentes.

Patrón: Fan-out / Fan-in
- Agent 1 ejecuta serial (rápido)
- Agents 2-4 ejecutan en paralelo (I/O heavy)

Flujo:
Trends → Scripts (paralelo) → Videos (paralelo) → Publish (paralelo) → Metrics
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

from agents import TrendScout, ScriptMaster, VideoProducer, MultiPublisher
from config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class PipelineMetrics:
    """Métricas de ejecución del pipeline"""
    started_at: str
    completed_at: str
    duration_seconds: float
    trends_discovered: int
    scripts_generated: int
    videos_produced: int
    publications: int
    errors: int
    total_cost_eur: float
    tokens_used: int


class PipelineOrchestrator:
    """
    Orquestador principal: ejecuta el pipeline completo de forma paralela y eficiente.

    Uso:
    ```python
    orchestrator = PipelineOrchestrator(region="es")
    result = await orchestrator.run_daily()
    ```
    """

    def __init__(self, region: str = "es", db=None, storage=None):
        self.region = region
        self.db = db
        self.storage = storage
        self.logger = logging.getLogger(__name__)

        # Inicializar agentes
        self.agent_trends = TrendScout(region=region, db=db)
        self.agent_script = ScriptMaster(region=region)
        self.agent_video = VideoProducer(region=region, storage=storage, db=db)
        self.agent_publisher = MultiPublisher(region=region, db=db)

        self.metrics = None

    async def run_daily(self) -> Dict[str, Any]:
        """
        Ejecuta el pipeline diario completo.

        Retorna:
        {
            "status": "success|error",
            "results": {
                "trends": [...],
                "scripts": [...],
                "videos": [...],
                "publications": [...]
            },
            "metrics": {...}
        }
        """

        start_time = datetime.now()
        self.logger.info("=" * 60)
        self.logger.info("🤖 INICIANDO PIPELINE DIARIO")
        self.logger.info("=" * 60)

        try:
            # ============ STEP 1: Descubrir Trends ============
            self.logger.info("📍 STEP 1/4: Descubriendo trends...")
            trends_result = await self.agent_trends.execute({
                "region": self.region,
                "num_trends": 5,
                "min_monetization_score": 0.6
            })

            if trends_result["status"] != "success":
                raise Exception("Trends discovery failed")

            trends = trends_result["result"]["trends"]
            self.logger.info(f"✅ {len(trends)} trends encontrados")

            if not trends:
                return {
                    "status": "no_trends",
                    "message": "No trends encontrados"
                }

            # ============ STEP 2: Generar Scripts (PARALELO) ============
            self.logger.info("📍 STEP 2/4: Generando scripts...")
            script_tasks = [
                self.agent_script.execute({
                    "trend_id": trend.get("id"),
                    "title": trend.get("title"),
                    "platform": "tiktok",
                    "duration_seconds": 60
                })
                for trend in trends
            ]

            script_results = await asyncio.gather(*script_tasks, return_exceptions=True)
            scripts = [r["result"] for r in script_results if isinstance(r, dict) and r.get("status") == "success"]
            self.logger.info(f"✅ {len(scripts)}/{len(trends)} scripts generados")

            # ============ STEP 3: Producir Videos (PARALELO) ============
            self.logger.info("📍 STEP 3/4: Produciendo videos...")
            video_tasks = [
                self.agent_video.execute({
                    "script": script.get("script"),
                    "trend_id": script.get("metadata", {}).get("trend_id"),
                    "platform": "tiktok"
                })
                for script in scripts
            ]

            video_results = await asyncio.gather(*video_tasks, return_exceptions=True)
            videos = [r["result"] for r in video_results if isinstance(r, dict) and r.get("status") == "success"]
            self.logger.info(f"✅ {len(videos)}/{len(scripts)} videos producidos")

            # ============ STEP 4: Publicar (PARALELO) ============
            self.logger.info("📍 STEP 4/4: Publicando...")
            publish_tasks = [
                self.agent_publisher.execute({
                    "video_url": video.get("video_url"),
                    "script": script.get("script"),
                    "trend_title": script.get("metadata", {}).get("trend_id"),
                    "platforms": ["instagram", "tiktok", "youtube"]
                })
                for video, script in zip(videos, scripts[:len(videos)])
            ]

            publish_results = await asyncio.gather(*publish_tasks, return_exceptions=True)
            publications = [r["result"] for r in publish_results if isinstance(r, dict) and r.get("status") == "success"]
            self.logger.info(f"✅ {len(publications)}/{len(videos)} lotes publicados")

            # ============ Calcular Métricas ============
            duration = (datetime.now() - start_time).total_seconds()
            metrics = PipelineMetrics(
                started_at=start_time.isoformat(),
                completed_at=datetime.now().isoformat(),
                duration_seconds=duration,
                trends_discovered=len(trends),
                scripts_generated=len(scripts),
                videos_produced=len(videos),
                publications=len(publications) * 3,  # 3 plataformas por video
                errors=0,
                total_cost_eur=len(videos) * 0.15,  # €0.15 por video
                tokens_used=sum([
                    len(s.get("script", "")) // 4 for s in scripts
                ])  # Aproximado
            )

            self.logger.info("=" * 60)
            self.logger.info("✅ PIPELINE COMPLETADO EXITOSAMENTE")
            self.logger.info(f"   Duración: {duration:.1f}s")
            self.logger.info(f"   Costo: €{metrics.total_cost_eur:.2f}")
            self.logger.info("=" * 60)

            return {
                "status": "success",
                "results": {
                    "trends": trends,
                    "scripts": scripts,
                    "videos": videos,
                    "publications": publications
                },
                "metrics": {
                    "started_at": metrics.started_at,
                    "completed_at": metrics.completed_at,
                    "duration_seconds": metrics.duration_seconds,
                    "trends_discovered": metrics.trends_discovered,
                    "scripts_generated": metrics.scripts_generated,
                    "videos_produced": metrics.videos_produced,
                    "publications": metrics.publications,
                    "total_cost_eur": metrics.total_cost_eur,
                    "tokens_used": metrics.tokens_used
                }
            }

        except Exception as e:
            self.logger.error(f"❌ ERROR EN PIPELINE: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "started_at": start_time.isoformat(),
                "completed_at": datetime.now().isoformat()
            }


async def test_orchestrator():
    """Test rápido del orquestador"""

    orchestrator = PipelineOrchestrator(region="es")
    result = await orchestrator.run_daily()

    print("\n" + "=" * 60)
    print("🤖 ORCHESTRATOR TEST RESULT")
    print("=" * 60)
    print(f"Status: {result['status']}")

    if result['status'] == 'success':
        metrics = result['metrics']
        print(f"\nMetrics:")
        print(f"  Trends: {metrics['trends_discovered']}")
        print(f"  Scripts: {metrics['scripts_generated']}")
        print(f"  Videos: {metrics['videos_produced']}")
        print(f"  Publications: {metrics['publications']}")
        print(f"  Duration: {metrics['duration_seconds']:.1f}s")
        print(f"  Cost: €{metrics['total_cost_eur']:.2f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_orchestrator())
