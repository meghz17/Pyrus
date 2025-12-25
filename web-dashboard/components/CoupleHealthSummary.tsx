"use client";

import { motion } from "framer-motion";
import { Heart, Moon, Battery, Brain, Zap } from "lucide-react";

interface CoupleHealthSummaryProps {
    whoop: {
        recovery_score: number | null;
        sleep_hours: number | null;
        hrv: number | null;
        strain: number | null;
    };
    oura: {
        readiness_score: number | null;
        sleep_hours: number | null;
        average_hrv: number | null;
        activity_score: number | null;
    };
}

// Get health status color based on percentage
function getHealthColor(value: number | null, max: number = 100): string {
    if (value === null) return "text-zinc-500";
    const pct = (value / max) * 100;
    if (pct >= 70) return "text-emerald-400";
    if (pct >= 40) return "text-amber-400";
    return "text-rose-400";
}

function getHealthBg(value: number | null, max: number = 100): string {
    if (value === null) return "bg-zinc-700";
    const pct = (value / max) * 100;
    if (pct >= 70) return "bg-emerald-500/20";
    if (pct >= 40) return "bg-amber-500/20";
    return "bg-rose-500/20";
}

// Simple progress ring component
function ProgressRing({ value, max = 100, color, size = 60 }: { value: number | null; max?: number; color: string; size?: number }) {
    const pct = value !== null ? Math.min((value / max) * 100, 100) : 0;
    const radius = (size - 8) / 2;
    const circumference = radius * 2 * Math.PI;
    const offset = circumference - (pct / 100) * circumference;

    return (
        <svg width={size} height={size} className="transform -rotate-90">
            <circle
                cx={size / 2}
                cy={size / 2}
                r={radius}
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
                className="text-zinc-800"
            />
            <circle
                cx={size / 2}
                cy={size / 2}
                r={radius}
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
                strokeDasharray={circumference}
                strokeDashoffset={offset}
                strokeLinecap="round"
                className={color}
                style={{ transition: "stroke-dashoffset 0.5s ease" }}
            />
        </svg>
    );
}

export function CoupleHealthSummary({ whoop, oura }: CoupleHealthSummaryProps) {
    const fmt = (v: number | null, d = 0) => (v !== null ? v.toFixed(d) : "–");

    return (
        <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative rounded-3xl border border-white/10 bg-gradient-to-br from-zinc-900/80 to-zinc-900/40 backdrop-blur-xl p-8 mb-8"
        >
            {/* Background gradient */}
            <div className="absolute inset-0 bg-gradient-to-r from-red-500/5 via-transparent to-blue-500/5 rounded-3xl" />

            <div className="relative z-10">
                {/* Header */}
                <div className="text-center mb-8">
                    <h3 className="text-xs font-bold tracking-[0.3em] text-zinc-500 uppercase mb-2">
                        Today's Health
                    </h3>
                    <h2 className="text-2xl font-bold text-white">Couple Summary</h2>
                </div>

                {/* Comparison Grid */}
                <div className="grid grid-cols-3 gap-4 items-center">
                    {/* Megh Column */}
                    <div className="text-center space-y-6">
                        <div className="flex flex-col items-center">
                            <div className="relative">
                                <ProgressRing value={whoop.recovery_score} color="text-red-400" size={80} />
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <span className={`text-xl font-bold ${getHealthColor(whoop.recovery_score)}`}>
                                        {fmt(whoop.recovery_score)}%
                                    </span>
                                </div>
                            </div>
                            <span className="text-xs text-zinc-500 mt-2">Recovery</span>
                        </div>
                        <div className="space-y-3">
                            <div className={`flex items-center justify-center gap-2 px-3 py-2 rounded-full ${getHealthBg(whoop.sleep_hours, 8)}`}>
                                <Moon className="w-4 h-4 text-zinc-400" />
                                <span className="text-white font-medium">{fmt(whoop.sleep_hours, 1)}h</span>
                            </div>
                            <div className="flex items-center justify-center gap-2 px-3 py-2 rounded-full bg-zinc-800/50">
                                <Heart className="w-4 h-4 text-zinc-400" />
                                <span className="text-white font-medium">{fmt(whoop.hrv)}ms</span>
                            </div>
                        </div>
                        <div className="text-sm font-semibold text-red-400">Megh</div>
                    </div>

                    {/* VS Separator */}
                    <div className="flex flex-col items-center justify-center">
                        <div className="w-px h-16 bg-gradient-to-b from-red-500/50 to-blue-500/50" />
                        <div className="my-4 px-4 py-2 rounded-full bg-zinc-800/50 border border-zinc-700">
                            <span className="text-xs font-bold text-zinc-400">VS</span>
                        </div>
                        <div className="w-px h-16 bg-gradient-to-b from-blue-500/50 to-transparent" />
                    </div>

                    {/* Meghna Column */}
                    <div className="text-center space-y-6">
                        <div className="flex flex-col items-center">
                            <div className="relative">
                                <ProgressRing value={oura.readiness_score} color="text-blue-400" size={80} />
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <span className={`text-xl font-bold ${getHealthColor(oura.readiness_score)}`}>
                                        {fmt(oura.readiness_score)}%
                                    </span>
                                </div>
                            </div>
                            <span className="text-xs text-zinc-500 mt-2">Readiness</span>
                        </div>
                        <div className="space-y-3">
                            <div className={`flex items-center justify-center gap-2 px-3 py-2 rounded-full ${getHealthBg(oura.sleep_hours, 8)}`}>
                                <Moon className="w-4 h-4 text-zinc-400" />
                                <span className="text-white font-medium">{fmt(oura.sleep_hours, 1)}h</span>
                            </div>
                            <div className="flex items-center justify-center gap-2 px-3 py-2 rounded-full bg-zinc-800/50">
                                <Heart className="w-4 h-4 text-zinc-400" />
                                <span className="text-white font-medium">{oura.average_hrv ? `${fmt(oura.average_hrv)}ms` : "–"}</span>
                            </div>
                        </div>
                        <div className="text-sm font-semibold text-blue-400">Meghna</div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
