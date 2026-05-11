"""
Clase base para todos los agentes.
Define logging, error handling, y patrones comunes.
"""

import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Clase base para todos los agentes.

    Proporciona:
    - Logging estructurado
    - Error handling con reintentos
    - Métricas de ejecución
    - State management
    """

    def __init__(self, name: str, region: str = "es"):
        self.name = name
        self.region = region
        self.logger = logging.getLogger(f"agents.{name}")
        self.execution_stats = {
            "started_at": None,
            "completed_at": None,
            "duration_seconds": 0,
            "status": "pending",
            "error": None,
            "tokens_used": 0,
            "api_calls": 0
        }

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta el agente con manejo de errores.

        Flujo:
        1. Log inicio
        2. Validar input
        3. Ejecutar lógica principal
        4. Registrar métricas
        5. Return resultado
        """

        self.execution_stats["started_at"] = datetime.now().isoformat()
        self.logger.info(f"🚀 Iniciando {self.name}")

        try:
            # Validar input
            if not self._validate_input(input_data):
                raise ValueError(f"Input inválido para {self.name}")

            # Ejecutar lógica
            result = await self._execute(input_data)

            self.execution_stats["status"] = "success"
            self.logger.info(f"✅ {self.name} completado exitosamente")

            return {
                "status": "success",
                "agent": self.name,
                "result": result,
                "stats": self.execution_stats
            }

        except asyncio.TimeoutError:
            error_msg = f"Timeout en {self.name}"
            self.logger.error(error_msg)
            self.execution_stats["status"] = "timeout"
            self.execution_stats["error"] = error_msg
            raise

        except Exception as e:
            error_msg = f"Error en {self.name}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            self.execution_stats["status"] = "failed"
            self.execution_stats["error"] = error_msg
            raise

        finally:
            # Registrar duración
            if self.execution_stats["started_at"]:
                start = datetime.fromisoformat(self.execution_stats["started_at"])
                duration = (datetime.now() - start).total_seconds()
                self.execution_stats["duration_seconds"] = duration

    @abstractmethod
    async def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implementar en cada agente.
        Este es el método que debe ser reescrito por subclases.
        """
        pass

    def _validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validar que el input tiene los campos requeridos.
        Override en cada agente si necesitas validaciones específicas.
        """
        return isinstance(input_data, dict) and len(input_data) > 0

    async def retry_with_backoff(self,
                                 coro,
                                 max_retries: int = 3,
                                 backoff_factor: float = 2.0) -> Any:
        """
        Reintentar una operación con exponential backoff.

        Uso:
            result = await self.retry_with_backoff(
                self._call_api(),
                max_retries=3
            )
        """

        for attempt in range(max_retries):
            try:
                return await coro
            except Exception as e:
                if attempt == max_retries - 1:
                    raise

                wait_time = backoff_factor ** attempt
                self.logger.warning(
                    f"Intento {attempt + 1}/{max_retries} falló. "
                    f"Esperando {wait_time}s..."
                )
                await asyncio.sleep(wait_time)

    def log_api_call(self,
                     api_name: str,
                     tokens_used: int = 0,
                     status: str = "success"):
        """Registrar llamada a API"""
        self.execution_stats["api_calls"] += 1
        self.execution_stats["tokens_used"] += tokens_used
        self.logger.debug(f"API: {api_name} ({tokens_used} tokens) - {status}")

    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de ejecución"""
        return self.execution_stats.copy()
