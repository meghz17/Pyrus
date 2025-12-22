"use client";

import { useEffect, useState } from "react";
import { HealthCard } from "@/components/HealthCard";
import { AIChatOverlay } from "@/components/AIChatOverlay";
import { Activity, Battery, Moon, Brain, Heart, Flame, Footprints, Scale, Ruler, Zap } from "lucide-react";

interface HealthData {
  date: string;
  timestamp: string;
  you: {
    recovery: {
      score: number;
      hrv: number;
      resting_hr?: number;
      spo2?: number;
      skin_temp?: number;
    };
    sleep: {
      hours: number;
      performance: number;
      efficiency?: number;
      deep_hours?: number;
      rem_hours?: number;
    };
    strain: {
      current: number;
      workout_count?: number;
    };
    body?: {
      height_meter?: number;
      weight_kg?: number;
      max_hr?: number;
    };
  };
  wife: {
    sleep: {
      total_hours: number;
      efficiency?: number;
    };
    activity: {
      score: number;
      steps: number;
      calories_burned?: number;
    };
    readiness?: {
      score: number;
      temperature_deviation?: number;
    };
    hrv?: {
      average_hrv?: number;
      lowest_hr?: number;
      average_hr?: number;
    };
    stress?: {
      stress_high?: number;
      recovery_high?: number;
      day_summary?: string;
    };
  };
}

export default function Home() {
  const [data, setData] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [isChatOpen, setIsChatOpen] = useState(false);

  // Date formatting
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
        <div className="animate-pulse flex flex-col items-center gap-4">
          <div className="h-12 w-12 border-4 border-zinc-800 border-t-white rounded-full animate-spin" />
          <p className="text-zinc-500 text-sm tracking-widest uppercase">Loading Life OS...</p>
        </div>
      </main>
    );
  }

  // Megh (Whoop) Data
  const recoveryScore = data?.you?.recovery?.score ?? 0;
  const sleepHoursYou = data?.you?.sleep?.hours?.toFixed(1) ?? "--";
  const strain = data?.you?.strain?.current?.toFixed(1) ?? "--";
  const hrv = data?.you?.recovery?.hrv?.toFixed(0) ?? "--";
  const restingHr = data?.you?.recovery?.resting_hr?.toFixed(0) ?? "--";
  const weightKg = data?.you?.body?.weight_kg?.toFixed(1) ?? "--";
  const maxHr = data?.you?.body?.max_hr ?? "--";

  // Meghna (Oura) Data
  const readinessScore = (data?.wife as any)?.readiness?.score ?? "--";
  const sleepHoursWife = data?.wife?.sleep?.total_hours?.toFixed(1) ?? "--";
  const activityScore = data?.wife?.activity?.score ?? "--";
  const stepsWife = data?.wife?.activity?.steps?.toLocaleString() ?? "--";
  const avgHrvOura = data?.wife?.hrv?.average_hrv?.toFixed(0) ?? "--";
  const lowestHrOura = data?.wife?.hrv?.lowest_hr ?? "--";

  return (
    <main className="min-h-screen bg-black text-white p-6 md:p-12 selection:bg-white/10">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-end justify-between gap-6">
          <div className="space-y-2">
            <h1 className="text-sm font-medium tracking-widest text-zinc-500 uppercase">Life OS // Dashboard</h1>
            <div className="flex items-baseline gap-4">
              <h2 className="text-4xl md:text-6xl font-bold tracking-tighter text-white">
                Good Evening
              </h2>
            </div>
            <p className="text-zinc-400 text-lg">{currentDate}</p>
          </div>

          <div className="flex flex-col items-end gap-2">
            <div className="flex items-center gap-4 bg-zinc-900/50 p-2 rounded-full border border-zinc-800">
              <div className="px-4 py-1.5 rounded-full bg-emerald-500/10 text-emerald-500 text-xs font-bold uppercase tracking-wider border border-emerald-500/20">
                All Systems Nominal
              </div>
            </div>
            {data?.timestamp && (
              <div className="flex items-center gap-2 text-zinc-500 text-sm">
                <span className="inline-block w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
                <span>
                  Data from: {new Date(data.timestamp).toLocaleString([], {
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>
            )}
          </div>
        </header>

        {/* Health Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <HealthCard
            title="Megh (Whoop)"
            type="whoop"
            lastUpdated={data?.timestamp ? new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Just now'}
            metrics={[
              { label: "Recovery", value: recoveryScore, unit: "%", icon: Battery, trend: "neutral" },
              { label: "Sleep", value: sleepHoursYou, unit: "h", icon: Moon, trend: "neutral" },
              { label: "Strain", value: strain, icon: Flame },
              { label: "HRV", value: hrv, unit: "ms", icon: Heart, trend: "neutral" },
              { label: "Resting HR", value: restingHr, unit: "bpm", icon: Heart },
              { label: "Weight", value: weightKg, unit: "kg", icon: Scale },
            ]}
          />

          <HealthCard
            title="Meghna (Oura)"
            type="oura"
            lastUpdated={data?.timestamp ? new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Just now'}
            metrics={[
              { label: "Readiness", value: readinessScore, unit: "%", icon: Brain, trend: "neutral" },
              { label: "Sleep", value: sleepHoursWife, unit: "h", icon: Moon, trend: "neutral" },
              { label: "Activity", value: activityScore, unit: "%", icon: Activity, trend: "neutral" },
              { label: "Steps", value: stepsWife, icon: Footprints },
              { label: "Avg HRV", value: avgHrvOura, unit: "ms", icon: Heart },
              { label: "Lowest HR", value: lowestHrOura, unit: "bpm", icon: Zap },
            ]}
          />
        </div>

        {/* AI & Date Night Section (Placeholder for now) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 rounded-3xl border border-zinc-800 bg-zinc-900/30 p-8 h-96 flex flex-col justify-between group hover:border-zinc-700 transition-colors">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="h-2 w-2 rounded-full bg-purple-500 animate-pulse" />
                <h3 className="text-lg font-semibold text-zinc-200">Pyrus AI Insight</h3>
              </div>
              <p className="text-xl md:text-2xl text-zinc-400 leading-relaxed font-light">
                "Data connection established. Waiting for sufficient historical data to generate personalized insights.
                Focus on consistent sleep schedules this week."
              </p>
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => setIsChatOpen(true)}
                className="px-6 py-3 rounded-full bg-white text-black font-semibold text-sm hover:bg-zinc-200 transition-colors"
              >
                Ask Pyrus
              </button>
            </div>
          </div>

          <div className="rounded-3xl border border-zinc-800 bg-zinc-900/30 p-8 h-96 flex flex-col relative overflow-hidden group hover:border-zinc-700 transition-colors">
            <div className="absolute top-0 right-0 w-32 h-32 bg-pink-500/10 blur-3xl rounded-full" />
            <h3 className="text-lg font-semibold text-zinc-200 mb-6 relative z-10">Next Date Idea</h3>

            <div className="flex-1 flex flex-col justify-center relative z-10">
              <span className="text-xs font-bold text-pink-500 uppercase tracking-widest mb-2">
                {(data as any)?.date_suggestion ? "Weekly Recommendation" : "Status"}
              </span>
              <h4 className="text-3xl font-bold text-white mb-2">
                {(data as any)?.date_suggestion?.suggested_dates?.[0]?.title || "Planning..."}
              </h4>
              <p className="text-zinc-500 text-sm leading-relaxed">
                {(data as any)?.date_suggestion?.suggested_dates?.[0]?.description || "Pyrus is analyzing your weekly energy to suggest the perfect Friday date."}
              </p>

              {(data as any)?.date_suggestion && (
                <div className="mt-8 flex items-center gap-4">
                  <div className="px-3 py-1 rounded-full bg-zinc-800 text-zinc-400 text-[10px] font-bold uppercase tracking-wider border border-white/5">
                    Energy: {(data as any)?.date_suggestion?.weekly_health?.energy_level}
                  </div>
                  <div className="px-3 py-1 rounded-full bg-zinc-800 text-zinc-400 text-[10px] font-bold uppercase tracking-wider border border-white/5">
                    Type: {(data as any)?.date_suggestion?.suggested_dates?.[0]?.type}
                  </div>
                </div>
              )}

              {!(data as any)?.date_suggestion && (
                <div className="mt-8 flex items-center gap-2">
                  <div className="h-1 flex-1 bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full w-3/4 bg-zinc-600 rounded-full animate-pulse" />
                  </div>
                  <span className="text-xs font-bold text-zinc-400">Syncing...</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <AIChatOverlay isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </main>
  );
}
