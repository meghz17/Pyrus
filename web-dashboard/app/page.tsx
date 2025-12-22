"use client";

import { useEffect, useState } from "react";
import { HealthCard } from "@/components/HealthCard";
import { CoupleHealthSummary } from "@/components/CoupleHealthSummary";
import { AIChatOverlay } from "@/components/AIChatOverlay";
import {
  Activity, Battery, Moon, Brain, Heart, Flame,
  Footprints, Scale, Thermometer, Wind, Clock, Zap,
  Sparkles
} from "lucide-react";

// Phase J: Flat metrics interface
interface HealthData {
  whoop_date: string;
  oura_date: string;
  whoop_fetched_at: string;
  oura_fetched_at: string;

  whoop: {
    recovery_score: number | null;
    resting_hr: number | null;
    hrv: number | null;
    spo2: number | null;
    skin_temp: number | null;
    sleep_hours: number | null;
    sleep_performance: number | null;
    sleep_efficiency: number | null;
    rem_hours: number | null;
    deep_hours: number | null;
    light_hours: number | null;
    awake_hours: number | null;
    sleep_cycles: number | null;
    respiratory_rate: number | null;
    strain: number | null;
    workout_count: number | null;
    height_m: number | null;
    weight_kg: number | null;
    max_hr: number | null;
  };

  oura: {
    readiness_score: number | null;
    temp_deviation: number | null;
    hrv_balance: number | null;
    sleep_hours: number | null;
    sleep_efficiency: number | null;
    rem_hours: number | null;
    deep_hours: number | null;
    light_hours: number | null;
    awake_hours: number | null;
    latency_minutes: number | null;
    lowest_hr: number | null;
    average_hr: number | null;
    average_hrv: number | null;
    activity_score: number | null;
    steps: number | null;
    active_calories: number | null;
    high_activity_minutes: number | null;
    stress_high: number | null;
    recovery_high: number | null;
    spo2: number | null;
  };
}

// Format helper - show "–" instead of "N/A" for cleaner look
const fmt = (val: number | null | undefined, decimals = 0): string => {
  if (val === null || val === undefined) return "–";
  return Number(val).toFixed(decimals);
};

// Get greeting based on time
function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return "Good Morning";
  if (hour < 17) return "Good Afternoon";
  return "Good Evening";
}

export default function Home() {
  const [data, setData] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  const currentDate = new Date().toLocaleDateString("en-US", {
    weekday: 'long',
    month: 'long',
    day: 'numeric'
  });

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch('/api/health');
        if (res.ok) {
          const json = await res.json();
          setData(json);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (!mounted || loading) {
    return (
      <main className="min-h-screen bg-black text-white p-6 md:p-12 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="h-12 w-12 border-4 border-zinc-800 border-t-emerald-500 rounded-full animate-spin" />
          <p className="text-zinc-500 text-sm tracking-widest uppercase">Loading Life OS...</p>
        </div>
      </main>
    );
  }

  const w = data?.whoop;
  const o = data?.oura;

  return (
    <main className="min-h-screen bg-gradient-to-b from-black via-zinc-950 to-black text-white p-6 md:p-10 selection:bg-white/10">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
          <div>
            <p className="text-xs font-medium tracking-[0.3em] text-zinc-600 uppercase mb-1">
              Life OS // Dashboard
            </p>
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight bg-gradient-to-r from-white to-zinc-500 bg-clip-text text-transparent">
              {getGreeting()}
            </h1>
            <p className="text-zinc-500 mt-1">{currentDate}</p>
          </div>

          <div className="flex flex-col items-end gap-2">
            {data?.whoop && data?.oura && (
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                  All Systems Nominal
                </span>
              </div>
            )}
            {data?.whoop_fetched_at && (
              <span className="text-xs text-zinc-600">
                Last sync: {new Date(data.whoop_fetched_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            )}
          </div>
        </header>

        {/* Couple Health Summary - Holistic View */}
        {data && (
          <CoupleHealthSummary
            whoop={{
              recovery_score: w?.recovery_score ?? null,
              sleep_hours: w?.sleep_hours ?? null,
              hrv: w?.hrv ?? null,
              strain: w?.strain ?? null,
            }}
            oura={{
              readiness_score: o?.readiness_score ?? null,
              sleep_hours: o?.sleep_hours ?? null,
              average_hrv: o?.average_hrv ?? null,
              activity_score: o?.activity_score ?? null,
            }}
          />
        )}

        {/* Individual Health Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Megh (Whoop) */}
          <HealthCard
            title="Megh (Whoop)"
            type="whoop"
            lastUpdated={data?.whoop_date}
            metrics={[
              // Primary (always visible)
              { label: "Recovery", value: fmt(w?.recovery_score), unit: "%", icon: Battery },
              { label: "Sleep", value: fmt(w?.sleep_hours, 1), unit: "h", icon: Moon },
              { label: "Strain", value: fmt(w?.strain, 1), icon: Flame },
              { label: "HRV", value: fmt(w?.hrv), unit: "ms", icon: Heart },
              // Secondary (expandable)
              { label: "Resting HR", value: fmt(w?.resting_hr), unit: "bpm", icon: Heart },
              { label: "SpO2", value: fmt(w?.spo2, 1), unit: "%", icon: Wind },
              { label: "Sleep Perf", value: fmt(w?.sleep_performance), unit: "%", icon: Moon },
              { label: "Deep Sleep", value: fmt(w?.deep_hours, 1), unit: "h", icon: Moon },
              { label: "REM Sleep", value: fmt(w?.rem_hours, 1), unit: "h", icon: Moon },
              { label: "Resp Rate", value: fmt(w?.respiratory_rate, 1), unit: "/min", icon: Wind },
              { label: "Skin Temp", value: fmt(w?.skin_temp, 1), unit: "°C", icon: Thermometer },
              { label: "Weight", value: fmt(w?.weight_kg, 1), unit: "kg", icon: Scale },
            ]}
          />

          {/* Meghna (Oura) */}
          <HealthCard
            title="Meghna (Oura)"
            type="oura"
            lastUpdated={data?.oura_date}
            metrics={[
              // Primary (always visible)
              { label: "Readiness", value: fmt(o?.readiness_score), unit: "%", icon: Brain },
              { label: "Sleep", value: fmt(o?.sleep_hours, 1), unit: "h", icon: Moon },
              { label: "Activity", value: fmt(o?.activity_score), unit: "%", icon: Activity },
              { label: "Steps", value: o?.steps?.toLocaleString() ?? "–", icon: Footprints },
              // Secondary (expandable)
              { label: "Avg HRV", value: fmt(o?.average_hrv), unit: "ms", icon: Heart },
              { label: "Lowest HR", value: fmt(o?.lowest_hr), unit: "bpm", icon: Heart },
              { label: "Sleep Eff", value: fmt(o?.sleep_efficiency), unit: "%", icon: Moon },
              { label: "Deep Sleep", value: fmt(o?.deep_hours, 1), unit: "h", icon: Moon },
              { label: "REM Sleep", value: fmt(o?.rem_hours, 1), unit: "h", icon: Moon },
              { label: "Latency", value: fmt(o?.latency_minutes), unit: "min", icon: Clock },
              { label: "Temp Dev", value: fmt(o?.temp_deviation, 2), unit: "°C", icon: Thermometer },
              { label: "Calories", value: fmt(o?.active_calories), unit: "kcal", icon: Zap },
            ]}
          />
        </div>

        {/* AI Assistant */}
        <div className="rounded-3xl border border-zinc-800/50 bg-gradient-to-br from-zinc-900/80 to-zinc-900/40 p-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-xl bg-purple-500/10 border border-purple-500/20">
              <Sparkles className="h-5 w-5 text-purple-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">Pyrus AI</h3>
              <p className="text-xs text-zinc-500">Your health insights assistant</p>
            </div>
          </div>
          <p className="text-zinc-400 mb-6">
            "Both of you had shorter sleep tonight. Consider an earlier bedtime to improve recovery scores tomorrow."
          </p>
          <button
            onClick={() => setIsChatOpen(true)}
            className="px-6 py-3 rounded-full bg-white text-black font-semibold text-sm hover:bg-zinc-200 transition-all hover:scale-105"
          >
            Ask Pyrus
          </button>
        </div>
      </div>

      <AIChatOverlay isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </main>
  );
}
