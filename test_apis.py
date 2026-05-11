#!/usr/bin/env python
"""
TEST RÁPIDO: Valida que tus APIs funcionan (Tavily + Gemini)

Uso:
    python test_apis.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from agents.agent_1_trends import TrendScout
from agents.agent_2_script import ScriptMaster


async def test_apis():
    """Test de APIs en secuencia"""

    print("\n" + "=" * 80)
    print("🧪 TEST RÁPIDO: Tavily + Gemini")
    print("=" * 80)

    # ========== VALIDAR CONFIGURACIÓN ==========
    print("\n1️⃣ VALIDANDO CONFIGURACIÓN...")

    if settings.TAVILY_API_KEY == "your-tavily-api-key-here":
        print("❌ TAVILY_API_KEY no configurada en .env")
        return 1

    if settings.GEMINI_API_KEY == "your-gemini-api-key-here":
        print("❌ GEMINI_API_KEY no configurada en .env")
        return 1

    print("✅ API keys configuradas correctamente")

    # ========== TEST AGENT 1 ==========
    print("\n2️⃣ TEST AGENT 1: TrendScout (Tavily)")
    print("-" * 80)

    try:
        agent_trends = TrendScout(region="es")
        print("🔍 Buscando trends reales en Tavily...")

        result = await agent_trends.execute({
            "region": "es",
            "num_trends": 3,
            "min_monetization_score": 0.6
        })

        if result["status"] != "success":
            print(f"❌ Error en Agent 1: {result.get('error')}")
            return 1

        trends = result["result"]["trends"]
        print(f"✅ {len(trends)} trends descubiertos:\n")

        for i, trend in enumerate(trends, 1):
            print(f"{i}. {trend['title'][:60]}")
            print(f"   Score: {trend['monetization_score']:.2f} | Source: {trend['source']}")

    except Exception as e:
        print(f"❌ Excepción en Agent 1: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    # ========== TEST AGENT 2 ==========
    print("\n3️⃣ TEST AGENT 2: ScriptMaster (Gemini)")
    print("-" * 80)

    try:
        agent_script = ScriptMaster(region="es")

        if not trends:
            print("⚠️ No hay trends para generar script. Saltando Agent 2.")
            return 0

        trend = trends[0]
        print(f"✍️ Generando script para: {trend['title'][:50]}...")

        result = await agent_script.execute({
            "trend_id": trend.get("id", "test_001"),
            "title": trend["title"],
            "platform": "tiktok",
            "duration_seconds": 60
        })

        if result["status"] != "success":
            print(f"❌ Error en Agent 2: {result.get('error')}")
            return 1

        script = result["result"]["script"]
        metadata = result["result"]["metadata"]

        print("✅ Script generado exitosamente:\n")
        print(script)
        print(f"\n📊 Metadata:")
        print(f"   Modelo: {metadata.get('generated_with')}")
        print(f"   Plataforma: {metadata.get('platform')}")
        print(f"   Generado: {metadata.get('generated_at')}")

    except Exception as e:
        print(f"❌ Excepción en Agent 2: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    # ========== RESUMEN ==========
    print("\n" + "=" * 80)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 80)
    print("\n📝 Próximos pasos:")
    print("   1. Levantar Docker: docker-compose up -d")
    print("   2. Ejecutar Agent 3 + Agent 4 tests")
    print("   3. Ejecutar pipeline completo: python scripts/run_daily.py --test")
    print("\n")

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(test_apis())
    sys.exit(exit_code)
