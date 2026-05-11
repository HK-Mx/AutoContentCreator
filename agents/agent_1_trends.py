"""
AGENT 1: TREND SCOUT 🔍

Responsabilidad:
- Buscar trending topics en tiempo real (Tavily API)
- Filtrar por relevancia + monetización (Ollama local)
- Guardar en Supabase
- Devolver top N trends

Entrada: {region: "es", num_trends: 5}
Salida: [{id, title, url, monetization_score, source}, ...]

ESTADO: 🔴 TODO - Necesita ser rellenado
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx

from agents.base import BaseAgent
from config.settings import settings


class TrendScout(BaseAgent):
    """
    Descubre trending topics relevantes por región.

    Flujo MVP:
    1. Tavily API → busca trending topics últimas 24h
    2. Score mockup → asigna scores de viralidad (será Ollama en Phase 2)
    3. Supabase → guarda trends con scores (será Phase 2)
    4. Return → lista de trends ordenada por score
    """

    def __init__(self, region: str = "es", db=None):
        super().__init__(name="TrendScout", region=region)
        self.region = region
        self.db = db
        self.tavily_api_key = settings.TAVILY_API_KEY
        self.ollama_host = settings.OLLAMA_HOST

    async def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta descubrimiento de trends.

        Input:
        {
            "region": "es",
            "num_trends": 5,
            "min_monetization_score": 0.6
        }

        Output:
        {
            "trends": [
                {
                    "id": "trend_001",
                    "title": "OpenAI lanza GPT-5",
                    "url": "https://...",
                    "monetization_score": 0.92,
                    "source": "reddit",
                    "discovered_at": "2026-05-05T14:22:30"
                },
                ...
            ],
            "total_discovered": 10,
            "filtered_count": 3,
            "execution_time_ms": 2534
        }
        """

        start_time = datetime.now()

        try:
            num_trends = input_data.get("num_trends", 5)
            min_score = input_data.get("min_monetization_score", 0.6)

            # Step 1: Buscar con Tavily
            self.logger.info(f"📍 Buscando trending topics en {self.region}...")
            raw_trends = await self._search_tavily()
            self.log_api_call("tavily", tokens_used=0, status="success")

            if not raw_trends:
                self.logger.warning("⚠️ No trends encontrados en Tavily")
                return {
                    "trends": [],
                    "total_discovered": 0,
                    "filtered_count": 0
                }

            # Step 2: Filtrar y puntuar (MVP: scoring mockup, Phase 2: Ollama)
            self.logger.info(f"📊 Analizando {len(raw_trends)} trends con scoring...")
            filtered_trends = await self._filter_with_ollama(raw_trends, min_score)
            self.log_api_call("score-filter", tokens_used=0, status="success")

            # Step 3: Ordenar por score
            filtered_trends = sorted(
                filtered_trends,
                key=lambda x: x["monetization_score"],
                reverse=True
            )[:num_trends]

            # Step 4: Guardar en Supabase (si db disponible)
            if self.db:
                await self._save_to_db(filtered_trends)
                self.logger.info(f"💾 {len(filtered_trends)} trends guardados en BD")

            # Calcular duración
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000

            return {
                "trends": filtered_trends,
                "total_discovered": len(raw_trends),
                "filtered_count": len(filtered_trends),
                "execution_time_ms": int(duration_ms)
            }

        except Exception as e:
            self.logger.error(f"❌ Error en TrendScout: {str(e)}")
            raise

    async def _search_tavily(self) -> List[Dict[str, Any]]:
        """
        TODO: Implementar búsqueda real con Tavily API

        Reemplazar esto con:
        ```python
        from tavily import TavilyClient

        client = TavilyClient(api_key=self.tavily_api_key)
        response = client.search(
            f"trending topics {self.region} last 24 hours",
            max_results=10,
            include_answer=True
        )

        trends = []
        for result in response.get("results", []):
            trends.append({
                "title": result["title"],
                "url": result["url"],
                "content": result.get("content", ""),
                "source": result.get("source", "web")
            })

        return trends
        ```

        POR AHORA: Devuelve mock trends para testing
        """

        # MOCK DATA (para testing sin Tavily)
        mock_trends = [
            {
                "title": "OpenAI lanza GPT-5: todo lo que necesitas saber",
                "url": "https://example.com/gpt5",
                "content": "OpenAI has announced GPT-5...",
                "source": "techcrunch"
            },
            {
                "title": "Nuevas regulaciones de IA en Europa 2026",
                "url": "https://example.com/ai-regulations",
                "content": "The European Commission announces new AI regulations...",
                "source": "reuters"
            },
            {
                "title": "Agentes IA autónomos: el futuro del trabajo",
                "url": "https://example.com/autonomous-agents",
                "content": "Autonomous AI agents are transforming businesses...",
                "source": "linkedin"
            },
            {
                "title": "VPN security: what changed in 2026",
                "url": "https://example.com/vpn-security",
                "content": "New VPN security standards announced...",
                "source": "hacker_news"
            },
            {
                "title": "Python Data Science frameworks comparación",
                "url": "https://example.com/python-ds",
                "content": "Comparing modern Python data science tools...",
                "source": "medium"
            }
        ]

        await asyncio.sleep(0.5)  # Simular latencia
        self.logger.debug(f"Mock: {len(mock_trends)} trends generados")
        return mock_trends

    async def _filter_with_ollama(self,
                                  trends: List[Dict],
                                  min_score: float = 0.6) -> List[Dict]:
        """
        TODO: Implementar filtrado real con Ollama

        Lógica:
        1. Para cada trend, crear prompt para Ollama
        2. Ollama evalúa: ¿es monetizable? ¿tiene alcance?
        3. Devolver score 0-1

        Reemplazar esto con:
        ```python
        import httpx

        filtered = []
        async with httpx.AsyncClient() as client:
            for trend in trends:
                prompt = f'''
                Trend: {trend['title']}

                Rate (0-1): ¿Es monetizable en YouTube/TikTok/Instagram?
                Considera: viralidad potencial, demanda, competencia.
                Solo responde número.
                '''

                response = await client.post(
                    f"{self.ollama_host}/api/generate",
                    json={"model": "mistral", "prompt": prompt, "stream": False},
                    timeout=10
                )

                score_text = response.json()["response"].strip()
                try:
                    score = float(score_text)
                    if score >= min_score:
                        trend["monetization_score"] = score
                        filtered.append(trend)
                except ValueError:
                    continue

        return filtered
        ```

        POR AHORA: Asigna scores mock
        """

        filtered = []
        scores = [0.92, 0.88, 0.85, 0.78, 0.72]

        for i, trend in enumerate(trends):
            trend["monetization_score"] = scores[i % len(scores)]
            trend["discovered_at"] = datetime.now().isoformat()
            trend["region"] = self.region
            trend["id"] = f"trend_{i:03d}"

            if trend["monetization_score"] >= min_score:
                filtered.append(trend)

        await asyncio.sleep(0.3)  # Simular latencia de Ollama
        return filtered

    async def _save_to_db(self, trends: List[Dict]):
        """
        TODO: Guardar trends en Supabase

        Reemplazar con:
        ```python
        await self.db.insert_trends(trends)
        ```
        """

        # Por ahora, solo log
        self.logger.debug(f"Saveable trends: {len(trends)}")
        pass


# ============================================================================
# TESTING
# ============================================================================

async def test_trend_scout():
    """Test rápido del agente"""

    agent = TrendScout(region="es")
    result = await agent.execute({
        "num_trends": 3,
        "min_monetization_score": 0.6
    })

    print("\n" + "=" * 60)
    print("🔍 TREND SCOUT TEST RESULT")
    print("=" * 60)
    print(f"Status: {result['status']}")
    print(f"Trends encontrados: {result['result']['filtered_count']}")

    for i, trend in enumerate(result['result']['trends'], 1):
        print(f"\n{i}. {trend['title']}")
        print(f"   Score: {trend['monetization_score']:.2f}")
        print(f"   Source: {trend['source']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_trend_scout())
