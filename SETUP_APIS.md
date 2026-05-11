# 🔐 API Configuration Guide

Este documento explica cómo obtener y configurar todas las claves API necesarias para el sistema de monetización.

## 1️⃣ TikTok API (TIKTOK_ACCESS_TOKEN)

### Obtener Token:
1. Ir a https://developers.tiktok.com/
2. Crear una aplicación en "My Apps"
3. Seleccionar "Web"
4. En "Scopes", habilitar:
   - `video.upload` (Subir videos)
   - `video.query` (Obtener estadísticas)
5. Generar "Server-side" token
6. Copiar el token a `.env` como `TIKTOK_ACCESS_TOKEN`

### Requisitos:
- ✅ 1,000 seguidores en TikTok
- ✅ 10,000 vistas en últimos 30 días
- ✅ Cumplir términos de servicio

**Monetización TikTok:**
- Creator Fund: €0.20-0.40 CPM
- Shop Affiliate: 5-20% comisión
- Sponsored: €500-5,000 por video

---

## 2️⃣ Instagram API (INSTAGRAM_ACCESS_TOKEN)

### Obtener Token:
1. Ir a https://business.facebook.com/
2. Crear aplicación en "Apps" → "Create App"
3. Seleccionar "Business"
4. En "Instagram Graph API", obtener Access Token
5. Agregar permisos: `instagram_basic`, `instagram_content_publishing`
6. Copiar token a `.env` como `INSTAGRAM_ACCESS_TOKEN`

### Requisitos:
- ✅ Cuenta Instagram Business conectada a Facebook
- ✅ 10,000 seguidores (para monetización)
- ✅ Cumplir políticas de comunidad

**Monetización Instagram:**
- Reels Play Bonus: €0.30-0.80 CPM
- Brand Collabs: €200-1,000 por reel
- Sponsored: €100-500 por reel

---

## 3️⃣ YouTube API (YOUTUBE_ACCESS_TOKEN + YOUTUBE_CLIENT_SECRET_PATH)

### Obtener Token:
1. Ir a https://console.cloud.google.com/
2. Crear nuevo proyecto
3. Habilitar "YouTube Data API v3"
4. Crear "OAuth 2.0 Client ID" → "Desktop application"
5. Descargar JSON como `youtube_secret.json`
6. Guardar en `./config/youtube_secret.json`
7. Ejecutar auth script para obtener Access Token

### Script de Autenticación:
```python
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ["https://www.googleapis.com/auth/youtube"]
flow = InstalledAppFlow.from_client_secrets_file(
    './config/youtube_secret.json', SCOPES)
creds = flow.run_local_server(port=0)

print(creds.token)  # ← Copiar este token a .env
```

### Requisitos:
- ✅ Canal verificado
- ✅ 1,000 suscriptores
- ✅ 4,000 horas de watch time (últimos 12 meses)
- ✅ YouTube Partner Program aprobado

**Monetización YouTube:**
- AdSense: €2-8 CPM
- Brand deals: €1,000-10,000 por video
- Affiliate: 5-20% comisión

---

## 4️⃣ Pexels API (PEXELS_API_KEY) [GRATIS]

### Obtener Token:
1. Ir a https://www.pexels.com/api/
2. Click en "Get Started"
3. Crear cuenta
4. Generar API key
5. Copiar a `.env` como `PEXELS_API_KEY`

**Límites:**
- ✅ 200 requests/hora (FREE)
- ✅ Videos 4K gratis
- ✅ Sin watermark

---

## 5️⃣ ElevenLabs API (ELEVENLABS_API_KEY) [FREEMIUM]

Ya configurado en fase anterior.

**Límites Free Tier:**
- ✅ 10,000 caracteres/mes
- ✅ 1 voz
- ✅ Velocidad estándar

---

## 🔧 Configurar .env

```bash
# .env
TIKTOK_ACCESS_TOKEN=your_tiktok_token_here
INSTAGRAM_ACCESS_TOKEN=your_instagram_token_here
YOUTUBE_ACCESS_TOKEN=your_youtube_token_here
YOUTUBE_CLIENT_SECRET_PATH=./config/youtube_secret.json
PEXELS_API_KEY=your_pexels_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

---

## 🚀 Testeando la Configuración

```bash
# Test individual APIs
python test_apis.py

# Run complete pipeline (1 video)
python run_complete_pipeline.py

# Check output
ls output/publications/
ls output/videos/
ls output/monetization/
```

---

## 📊 Estimación de Ingresos Mensuales

| Plataforma | Views/mes | CPM | Ingresos |
|---|---|---|---|
| TikTok | 50,000 | €0.25 | €12.50 |
| Instagram | 30,000 | €0.50 | €15.00 |
| YouTube | 10,000 | €2.00 | €20.00 |
| **TOTAL** | **90,000** | - | **€47.50/mes** |

*Basado en faceless channels sin costo de producción*

---

## ⚠️ Notas Importantes

1. **Límites de API:**
   - Respeta rate limits de cada plataforma
   - Implementa backoff exponencial en errores
   - Cachea resultados cuando sea posible

2. **Seguridad:**
   - Nunca commits `.env` a git
   - Usa variables de entorno en producción
   - Rota tokens periódicamente

3. **Cumplimiento:**
   - Lee términos de servicio de cada plataforma
   - No uses bots para engagement
   - Publica contenido original/de valor

4. **Monetización:**
   - Requiere mínimos (ej: YouTube Partner Program)
   - Ingresos pueden variar por geografía/nicho
   - Tax compliance según localidad

---

## 🔗 Referencias

- TikTok API: https://developers.tiktok.com/
- Instagram API: https://developers.facebook.com/docs/instagram-api/
- YouTube API: https://developers.google.com/youtube
- Pexels API: https://www.pexels.com/api/
- ElevenLabs: https://elevenlabs.io/

