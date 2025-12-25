# Pyrus V2 Documentation

## Quick Links

- **[Walkthrough](file:///.gemini/antigravity/brain/b090bf34-9527-48d1-b23f-2885c7d8ac03/walkthrough.md)** - Complete overview of Phase 1-3
- **[Setup Guide](file:///.gemini/antigravity/brain/b090bf34-9527-48d1-b23f-2885c7d8ac03/setup_guide.md)** - Initial Docker + API setup
- **[Phase 3 Guide](file:///.gemini/antigravity/brain/b090bf34-9527-48d1-b23f-2885c7d8ac03/phase3_guide.md)** - Joint Battery activation
- **[Telegram Setup](file:///telegram_setup.md)** - Bot configuration
- **[Whoop Debugging](file:///whoop_debugging.md)** - OAuth troubleshooting

## Active Services

- **n8n**: [http://localhost:5678](http://localhost:5678)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **pgAdmin**: [http://localhost:5050](http://localhost:5050)

## Quick Commands

**Restart all services:**
```bash
docker compose restart
```

**View logs:**
```bash
docker compose logs --tail=100
```

**Backup database:**
```bash
docker exec pyrus-db pg_dump -U pyrus_admin pyrus_main > backup.sql
```

## Status

**Phase 3: COMPLETE** ✅
- Oura + Whoop integration working
- Empathy algorithm deployed
- Telegram notifications active
