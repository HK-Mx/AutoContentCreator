# 🚀 SETUP RÁPIDO (5 MINUTOS)

## Paso 1: Instalar Dependencias

```bash
cd C:\Users\maxi\DATA\ SCIENCE\AutoContentCreator

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

**Esperado**: Sin errores, ~30 segundos

## Paso 2: Configurar API Keys

```bash
# Copiar template
cp .env.example .env

# Editar con VS Code
code .env
```

**Necesitas estos valores inicialmente** (mínimo para Fase 1):

1. **TAVILY_API_KEY**:
   - Ve a: https://tavily.com/
   - Sign up (gratis)
   - Copia tu API key
   - Pega en `.env`

2. **GEMINI_API_KEY**, **CLAUDE_API_KEY**, **ELEVENLABS_API_KEY** (para después, por ahora deja dummy)

```env
TAVILY_API_KEY=your-actual-key-here
GEMINI_API_KEY=placeholder
CLAUDE_API_KEY=placeholder
ELEVENLABS_API_KEY=placeholder
AWS_ACCESS_KEY_ID=placeholder
AWS_SECRET_ACCESS_KEY=placeholder
```

## Paso 3: Test Inicial

```bash
# Verificar que Python ve las API keys
python -c "from config.settings import settings; print('✅ Config OK' if settings.TAVILY_API_KEY != 'placeholder' else '❌ API Key no configurada')"
```

**Esperado**: `✅ Config OK` (si completaste Paso 2 correctamente)

## Paso 4: Levanta los Servicios (Docker)

```bash
docker-compose up -d
docker-compose ps
```

**Esperado**: 4 servicios en estado "healthy"

```
NAME      STATUS
ollama    healthy
postgres  healthy
redis     healthy
app       healthy
```

Si falta Ollama, espera ~30s más:
```bash
docker exec autocontent-ollama ollama pull mistral
```

## Paso 5: Test Agent 1

```bash
python agents/agent_1_trends.py
```

**Esperado**: Sin errores y output como:

```
============================================================
🔍 TREND SCOUT TEST RESULT
============================================================
Status: success
Trends encontrados: 3

1. OpenAI lanza GPT-5: todo lo que necesitas saber
   Score: 0.92
   Source: techcrunch

2. Nuevas regulaciones de IA en Europa 2026
   Score: 0.88
   Source: reuters

3. Agentes IA autónomos: el futuro del trabajo
   Score: 0.85
   Source: linkedin

============================================================
```

**Si ves esto**: ✅ ¡LISTO! Fase 1 funciona

---

## 🎯 Próximos Pasos

### Ahora (dentro de 5 min)
1. ✅ Completar Paso 1-5 arriba
2. ✅ Reportar qué funcionó/qué no
3. ✅ Si todo OK, pasar a Fase 2

### Mañana (Fase 2)
- Rellenar Agent 2 (ScriptMaster) con Gemini + Claude
- Testear generación de guiones
- Implementar anti-IA bypass

### Día 3 (Fase 3)
- Rellenar Agent 3 (VideoProducer) con ElevenLabs + MoviePy
- Generar primer video
- Subir a S3

### Día 4-5
- Agent 4 (Publisher)
- Pipeline completo
- Dashboard

### Semana 2
- Cron diario (automatización)
- Email reports
- Deployment en VPS

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'tavily'"

```bash
pip install -r requirements.txt
```

### "Docker daemon is not running"

Necesitas Docker Desktop. Descárgalo desde: https://www.docker.com/products/docker-desktop

### "TAVILY_API_KEY not found"

Asegúrate que:
1. Editaste `.env` correctamente
2. No hay espacios: `TAVILY_API_KEY=xxx` (no `TAVILY_API_KEY = xxx`)
3. Guardaste el archivo (Ctrl+S)

### "Port 8000/5432/6379 already in use"

```bash
# Termina procesos usando esos puertos
lsof -i :8000
kill -9 <PID>
```

---

## 📋 Checklist

- [ ] Venv creado y activado
- [ ] requirements.txt instalado
- [ ] .env editado con TAVILY_API_KEY real
- [ ] docker-compose up funcionando
- [ ] Agent 1 test pasa sin errores
- [ ] Trending topics reales en output

**Si todas las casillas** ✅ **→ Estás listo para Fase 2**

---

## 📞 Dile a Claude:

Una vez hayas completado SETUP, envía un mensaje como:

```
Setup completado ✅

Agent 1 test output:
[pega el output aquí]

Próximo paso: Fase 2 (Agent 2 - ScriptMaster)
```

Y continuaremos rellenando los demás agentes en orden.

---

**¡Vamos! 🚀**
