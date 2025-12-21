# Pyrus Life OS // Web Dashboard

This is the frontend and AI orchestration layer of the Life OS system.

## 🚀 Features

- **Health Visualization**: Real-time cards for Whoop and Oura metrics.
- **Interactive AI Chat**: Slide-out overlay to chat with Pyrus (GPT-4o).
- **Glassmorphism Design**: High-end aesthetic with dark mode and animations.
- **Multi-source Data**: Supports local JSON fallback and Supabase cloud ingestion.

## 🛠 Tech Stack

- **Next.js 14** (App Router)
- **Tailwind CSS v4** (Styling)
- **Framer Motion** (Animations)
- **OpenAI SDK** (AI Coaching)
- **Supabase SDK** (Cloud Data)

## ⚙️ Environment Variables

Create a `.env` file in this directory and add:

```env
# AI
OPENAI_API_KEY=your_key
AI_INTEGRATIONS_OPENAI_BASE_URL= (optional)

# Database
NEXT_PUBLIC_SUPABASE_URL=your_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_key
```

## 🏃 Getting Started

```bash
npm install
npm run dev
```

Visit [localhost:3000](http://localhost:3000) to see your Life OS.
