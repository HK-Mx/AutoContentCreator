# ⚡ QUICK START - MVP PHASE 1B

## 🎯 OBJETIVO: Deploy + Email + Dashboard EN ESTA NOCHE

---

## 📝 PASO 1: Verificar Email (5 min)

### Setup SMTP en .env

Abre `.env` y reemplaza:

```env
# ========== Email Reporting ==========
ADMIN_EMAIL=maxivivas211@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
```

**Para Gmail (2 opciones)**:

**Opción A: App Password (RECOMENDADO)**
1. Ve a: https://myaccount.google.com/apppasswords
2. Selecciona "Mail" y "Windows" (o tu SO)
3. Google genera password de 16 caracteres
4. Copia ese password en SMTP_PASSWORD

**Opción B: Less Secure Apps**
1. Ve a: https://myaccount.google.com/lesssecureapps
2. Habilita "Allow less secure apps"
3. Usa tu contraseña de Gmail normal

---

## 🚀 PASO 2: Ejecutar Test Pipeline (2 min)

```bash
# Entra en venv
venv\Scripts\activate

# Ejecuta test (1 trend + email)
python scripts/run_daily_improved.py --test
```

**Esperado**:
```
================================================================================
🚀 DAILY PIPELINE START
================================================================================

1️⃣ DISCOVERING TRENDS...
✅ 1 trends discovered
   1. OpenAI lanza GPT-5...

2️⃣ GENERATING SCRIPTS...
✅ Script generated for: OpenAI lanza GPT-5...

3️⃣ SAVING RESULTS...
💾 Results saved to: pipeline_20260511_132541.json

4️⃣ SENDING EMAIL REPORT...
📧 Email sent to: maxivivas211@gmail.com

================================================================================
✅ PIPELINE COMPLETE
================================================================================
Trends: 1
Scripts: 1
Avg Score: 0.92
Duration: 15s
================================================================================
```

---

## 📧 PASO 3: Verificar Email (1 min)

**Chequea tu inbox**:
- Remitente: tu-email@gmail.com
- Asunto: "📊 AutoContentCreator - Reporte Diario 2026-05-11"
- Contenido: HTML con métricas + scripts

Si no llega:
- Revisar spam
- Verificar logs: `type logs/pipeline.log`
- Run con --no-email: `python scripts/run_daily_improved.py --test --no-email`

---

## 📊 PASO 4: Abrir Dashboard (1 min)

```bash
# Abre en navegador
start dashboard.html
```

**Lo que ves**:
- 4 KPI cards (trends, scripts, score, costo)
- 2 gráficos (distribución scores + sources)
- 3 scripts generados con contenido
- Responsive en mobile

---

## 🔥 PASO 5: Ejecutar Pipeline Completo (3 min)

```bash
# Sin --test = 5 trends + 5 scripts
python scripts/run_daily_improved.py

# O con verbose para ver todo
python scripts/run_daily_improved.py --verbose
```

---

## ✨ STEP 6: Ver Resultados

**Los archivos creados**:
```
✅ pipeline_20260511_*.json      → Trends + scripts guardados
✅ logs/pipeline.log              → Log completo
✅ dashboard.html                 → Dashboard actualizado
✅ Email en inbox                 → Reporte diario
```

---

## 🎯 PASO 7: Próximo Paso HARÁ

### OPCIÓN A: Automatizar (Windows - 5 min)
1. Abrir "Task Scheduler"
2. New Basic Task → "AutoContentCreator Daily"
3. Trigger: Daily 9:00 AM
4. Action: `C:\Users\maxi\DATA SCIENCE\AutoContentCreator\venv\Scripts\python.exe scripts/run_daily_improved.py`
5. Start in: `C:\Users\maxi\DATA SCIENCE\AutoContentCreator`

### OPCIÓN B: Cron (Linux/Mac - 2 min)
```bash
# Editar crontab
crontab -e

# Agregar línea (ejecutar 9am)
0 9 * * * cd /path/to/project && python scripts/run_daily_improved.py
```

### OPCIÓN C: Manual (Sin automatización)
```bash
# Ejecutar cuando quieras
python scripts/run_daily_improved.py
```

---

## 💰 ANTES DE VENDER

**Checklist final**:
- [ ] Email funciona (test enviado)
- [ ] Dashboard carga bien
- [ ] Pipeline ejecuta sin errores
- [ ] Tienes 5 scripts generados
- [ ] Sabes el costo por script (€0.12 Gemini)

---

## 🚀 LISTO PARA VENDER

**Presentes a cliente**:
1. Dashboard con últimos 5 scripts
2. Email con reporte diario
3. Precios:
   - **€0.50/script** (pago por uso)
   - **€15/mes** (10 scripts/mes)
   - **€100/mes** (white label)

---

## 🆘 TROUBLESHOOTING RÁPIDO

| Error | Solución |
|-------|----------|
| "SMTPAuthenticationError" | Verificar SMTP_USER/PASSWORD en .env |
| "Email not sent" | Revisar logs: `type logs/pipeline.log` |
| "No models available" | Normal: fallback local genera scripts |
| "Dashboard no carga" | Abrir con navegador: `start dashboard.html` |
| "Pipeline no ejecuta" | Verificar venv activado: `venv\Scripts\activate` |

---

## ⏱️ TIMELINE ESPERADO

| Paso | Tiempo | Status |
|------|--------|--------|
| 1. Setup SMTP | 5 min | ← AHORA |
| 2. Test pipeline | 2 min | ← AHORA |
| 3. Verificar email | 1 min | ← AHORA |
| 4. Dashboard | 1 min | ← AHORA |
| 5. Pipeline completo | 3 min | ← AHORA |
| 6. Automatizar | 5 min | Después |
| **TOTAL** | **17 min** | **MVP READY** |

---

## 🎉 DESPUÉS (Mañana)

1. Crear landing page simple
2. Contactar primeros clientes
3. Primera venta
4. Setup Stripe/PayPal
5. Monetización

---

**¿Listo?** Dale caña → `python scripts/run_daily_improved.py --test` 🚀
