# Pyrus Life OS 🧬✨

Pyrus is a comprehensive **Life OS** system that integrates premium health wearable data (Whoop & Oura) with a GPT-4o powered AI Health Coach. It features a stunning, responsive web dashboard and an automated cloud data pipeline.

## 🚀 Key Features

- **Dual-Wearable Tracking**: Unified dashboard for both you (Whoop) and your partner (Oura).
- **AI Health Coach**: "Pyrus" uses your live metrics and 7-day trends to provide actionable coaching.
- **Date Night Suggester**: Automatically suggests Friday date ideas based on your weekly energy levels.
- **Cloud-Ready**: Automated data fetching via GitHub Actions and persistent storage via Supabase.
- **Premium UI**: Dark-mode, glassmorphism dashboard built with Next.js 14 and Framer Motion.

## 📂 Project Structure

- `/web-dashboard`: The Next.js frontend and AI Chat API.
- `/src`: Python scripts for data fetching, analysis, and AI coaching logic.
- `/data`: Local JSON storage (for development/Raspberry Pi mode).
- `/magicmirror-modules`: Original modules for MagicMirror integration.
- `.github/workflows`: Automation for daily health data sync to the cloud.

## ⚙️ Setup & Deployment

1.  **Local Dashboard**: `cd web-dashboard && npm install && npm run dev`
2.  **Data Sync**: Configure `SUPABASE_URL` and `SUPABASE_KEY` to sync local data to the cloud.
3.  **Deployment**: See [deployment_plan.md](brain/a0b68fc7-8f6f-4030-9766-a5bb960f790c/deployment_plan.md) for Vercel + Supabase setup.

## 🧠 AI Coach Context

Pyrus is relationship-aware and energy-aware. It uses:
- **Whoop**: Recovery, Sleep, Strain, HRV.
- **Oura**: Readiness, Activity, Sleep, Steps.
- **Context**: Date night history and weekly energy trends.

---
Built with ❤️ for a balanced, high-performance life.
