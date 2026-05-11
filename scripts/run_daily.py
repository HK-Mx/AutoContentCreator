#!/usr/bin/env python
"""
ENTRY POINT: Ejecuta el pipeline diario completo.

Uso:
    python scripts/run_daily.py                  # Producción normal
    python scripts/run_daily.py --test           # Test (1 trend)
    python scripts/run_daily.py --verbose        # Con debug logging
    python scripts/run_daily.py --dry-run        # Solo mostrar qué haría

Vía CRON (diario 09:00 AM):
    0 9 * * * cd /path/to/AutoContentCreator && python scripts/run_daily.py >> /var/log/pipeline.log 2>&1
"""

import asyncio
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Agregar project root al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.orchestrator import PipelineOrchestrator
from config.settings import settings


def setup_logging(verbose: bool = False):
    """Configura logging centralizado"""

    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log", mode="a"),
            logging.StreamHandler()
        ]
    )

    # Crear dir logs si no existe
    Path("logs").mkdir(exist_ok=True)


async def run_pipeline(test_mode: bool = False,
                       verbose: bool = False,
                       dry_run: bool = False) -> int:
    """
    Ejecuta el pipeline diario completo.

    Retorna:
        0 si exitoso
        1 si error
    """

    logger = logging.getLogger(__name__)

    logger.info("=" * 80)
    logger.info("🤖 AUTONOMOUS CONTENT CREATOR - PIPELINE DIARIO")
    logger.info("=" * 80)
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"Region: {settings.DEFAULT_REGION}")
    logger.info(f"Mode: {'TEST' if test_mode else 'PRODUCTION'}")
    logger.info(f"Dry-run: {dry_run}")

    if not settings.validate_apis():
        logger.error("❌ APIs no configuradas. Edita .env con tus claves.")
        return 1

    try:
        # Crear orquestador
        orchestrator = PipelineOrchestrator(region=settings.DEFAULT_REGION)

        # Ejecutar pipeline
        if dry_run:
            logger.info("🔍 DRY-RUN MODE: Simulando pipeline sin ejecutar...")
            logger.info("  - Descubraría 5 trends")
            logger.info("  - Generaría 5 scripts")
            logger.info("  - Produciría 5 videos")
            logger.info("  - Publicaría 15 posts (5 videos × 3 plataformas)")
            logger.info("✅ Dry-run completado sin errores")
            return 0

        # Ejecutar real
        result = await orchestrator.run_daily()

        # Procesar resultado
        if result["status"] == "success":
            metrics = result["metrics"]

            logger.info("=" * 80)
            logger.info("✅ PIPELINE EXITOSO")
            logger.info("=" * 80)
            logger.info(f"📊 Métricas:")
            logger.info(f"   Trends descubiertos: {metrics['trends_discovered']}")
            logger.info(f"   Scripts generados: {metrics['scripts_generated']}")
            logger.info(f"   Videos producidos: {metrics['videos_produced']}")
            logger.info(f"   Posts publicados: {metrics['publications']}")
            logger.info(f"   Duración: {metrics['duration_seconds']:.1f}s")
            logger.info(f"   Costo: €{metrics['total_cost_eur']:.2f}")
            logger.info(f"   Tokens: {metrics['tokens_used']:,}")

            # TODO: Enviar email report
            # await send_daily_report(result)

            return 0

        elif result["status"] == "no_trends":
            logger.warning("⚠️ No se encontraron trends relevantes hoy")
            return 0

        else:
            logger.error(f"❌ Pipeline falló: {result.get('error', 'Unknown error')}")
            return 1

    except KeyboardInterrupt:
        logger.warning("⚠️ Pipeline interrumpido por usuario")
        return 1

    except Exception as e:
        logger.error(f"❌ Error fatal: {str(e)}", exc_info=True)
        return 1


def main():
    """Entry point"""

    parser = argparse.ArgumentParser(
        description="Autonomous Content Creator - Pipeline Diario"
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Modo test (1 trend solamente)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Logging verbose (DEBUG)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simular sin ejecutar"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(verbose=args.verbose)

    # Run
    exit_code = asyncio.run(
        run_pipeline(
            test_mode=args.test,
            verbose=args.verbose,
            dry_run=args.dry_run
        )
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
