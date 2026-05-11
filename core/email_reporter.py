"""
EMAIL REPORTER: Envía resumen diario de scripts generados

Responsabilidad:
- Generar email HTML con scripts del día
- Enviar vía SMTP a admin
- Incluir métricas y analytics

Entrada: {trends: [...], scripts: [...], metrics: {...}}
Salida: Email enviado ✅
"""

import smtplib
from typing import List, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

from config.settings import settings


class EmailReporter:
    """Envía reportes diarios por email"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.admin_email = settings.ADMIN_EMAIL

    async def send_daily_report(self,
                                 trends: List[Dict[str, Any]],
                                 scripts: List[Dict[str, Any]],
                                 metrics: Dict[str, Any]) -> bool:
        """
        Envía reporte diario con scripts generados

        Input:
        {
            "trends": [{"title": "...", "score": 0.92}, ...],
            "scripts": [{"title": "...", "content": "..."}, ...],
            "metrics": {
                "total_discovered": 10,
                "total_generated": 5,
                "avg_score": 0.87,
                "cost_eur": 0.12,
                "duration_seconds": 45
            }
        }

        Output: True si se envió exitosamente
        """

        try:
            self.logger.info(f"📧 Preparando reporte para {self.admin_email}...")

            # Generar HTML del email
            html_content = self._generate_email_html(trends, scripts, metrics)

            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 AutoContentCreator - Reporte Diario {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = self.smtp_user
            msg['To'] = self.admin_email

            # Adjuntar HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Enviar vía SMTP
            self.logger.info(f"🔄 Conectando a {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            self.logger.info(f"✅ Email enviado exitosamente a {self.admin_email}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error enviando email: {str(e)}")
            return False

    def _generate_email_html(self,
                             trends: List[Dict[str, Any]],
                             scripts: List[Dict[str, Any]],
                             metrics: Dict[str, Any]) -> str:
        """Genera HTML del email"""

        scripts_html = ""
        for i, script in enumerate(scripts, 1):
            title = script.get("title", "Script sin título")
            score = script.get("monetization_score", 0)
            content = script.get("script", "")[:200] + "..."

            scripts_html += f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 15px; text-align: center; font-weight: bold;">{i}</td>
                <td style="padding: 15px;"><strong>{title}</strong></td>
                <td style="padding: 15px; text-align: center;">
                    <span style="background: #667eea; color: white; padding: 5px 10px; border-radius: 4px; font-size: 0.9em;">
                        {score:.2f}
                    </span>
                </td>
                <td style="padding: 15px; font-size: 0.85em; color: #666;">
                    {content}
                </td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 20px; }}
                .header h1 {{ margin: 0; font-size: 1.8em; }}
                .header p {{ margin: 5px 0 0 0; opacity: 0.9; }}
                .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }}
                .metric-box {{ background: #f5f5f5; padding: 15px; border-radius: 8px; text-align: center; }}
                .metric-value {{ font-size: 1.8em; font-weight: bold; color: #667eea; }}
                .metric-label {{ font-size: 0.85em; color: #666; margin-top: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background: #667eea; color: white; padding: 12px; text-align: left; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; font-size: 0.85em; color: #666; }}
                .cta-button {{ background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; margin-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 AutoContentCreator</h1>
                    <p>Reporte diario de generación de contenido viral</p>
                    <p style="margin-top: 10px; font-size: 0.9em;">{datetime.now().strftime('%d de %B de %Y')}</p>
                </div>

                <div class="metrics">
                    <div class="metric-box">
                        <div class="metric-value">{metrics.get('total_discovered', 0)}</div>
                        <div class="metric-label">Trends Descubiertos</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{len(scripts)}</div>
                        <div class="metric-label">Scripts Generados</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{metrics.get('avg_score', 0):.2f}</div>
                        <div class="metric-label">Score Promedio</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">€{metrics.get('cost_eur', 0):.2f}</div>
                        <div class="metric-label">Costo API</div>
                    </div>
                </div>

                <h2>📝 Scripts de Hoy</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Título</th>
                            <th>Score</th>
                            <th>Preview</th>
                        </tr>
                    </thead>
                    <tbody>
                        {scripts_html}
                    </tbody>
                </table>

                <div class="footer">
                    <h3>📊 Próximos Pasos</h3>
                    <ul>
                        <li>Dashboard interactivo disponible en: <code>dashboard.html</code></li>
                        <li>Monetización: Vender scripts a €0.50 cada uno</li>
                        <li>SaaS básico: €15/mes por 10 scripts</li>
                    </ul>

                    <p style="margin-top: 20px;">
                        <strong>AutoContentCreator v1.0 MVP</strong><br>
                        Sistema autónomo de generación de contenido viral<br>
                        Powered by Tavily + Gemini + Local LLM
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        return html


# ============================================================================
# TESTING
# ============================================================================

async def test_email_reporter():
    """Test rápido del reporter"""

    reporter = EmailReporter()

    # Mock data
    trends = [
        {"title": "OpenAI lanza GPT-5", "score": 0.92},
        {"title": "Regulaciones IA", "score": 0.88},
    ]

    scripts = [
        {
            "title": "OpenAI lanza GPT-5: todo lo que necesitas saber",
            "monetization_score": 0.92,
            "script": "Hook brillante... Loop enganchador... CTA viral..."
        },
        {
            "title": "Nuevas regulaciones de IA en Europa 2026",
            "monetization_score": 0.88,
            "script": "Explicación clara... Datos impactantes... Llamada a acción..."
        }
    ]

    metrics = {
        "total_discovered": 10,
        "avg_score": 0.87,
        "cost_eur": 0.12,
        "duration_seconds": 45
    }

    result = await reporter.send_daily_report(trends, scripts, metrics)

    if result:
        print("✅ Email enviado exitosamente")
    else:
        print("⚠️ No se pudo enviar el email (verifica SMTP_USER/PASSWORD en .env)")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_email_reporter())
