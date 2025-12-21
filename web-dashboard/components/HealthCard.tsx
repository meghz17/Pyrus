"use client";

import { motion } from "framer-motion";
import { Activity, Moon, Battery, Heart, TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "@/lib/utils";

interface Metric {
    label: string;
    value: string | number;
    unit?: string;
    trend?: "up" | "down" | "neutral";
    color?: string;
    icon?: React.ElementType;
}

interface HealthCardProps {
    title: string;
    type: "whoop" | "oura";
    metrics: Metric[];
    lastUpdated?: string;
}

export function HealthCard({ title, type, metrics, lastUpdated }: HealthCardProps) {
    const isWhoop = type === "whoop";
    const brandColor = isWhoop ? "bg-red-500" : "bg-blue-500";
    const brandColorText = isWhoop ? "text-red-500" : "text-blue-500";
    const brandGradient = isWhoop
        ? "from-red-500/20 to-red-500/5"
        : "from-blue-500/20 to-blue-500/5";

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
                "relative overflow-hidden rounded-3xl border border-white/10 backdrop-blur-xl",
                "bg-gradient-to-br p-6 shadow-2xl",
                "dark:bg-zinc-900/50 dark:border-zinc-800"
            )}
        >
            {/* Dynamic Background Glow */}
            <div className={cn("absolute -right-20 -top-20 h-60 w-60 rounded-full blur-3xl opacity-20", brandColor)} />

            <div className="relative z-10">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-3">
                        <div className={cn("h-3 w-3 rounded-full animate-pulse", brandColor)} />
                        <h2 className="text-xl font-bold tracking-tight text-zinc-100">{title}</h2>
                    </div>
                    {lastUpdated && (
                        <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
                            {lastUpdated}
                        </span>
                    )}
                </div>

                {/* Metrics Grid */}
                <div className="grid grid-cols-2 gap-6">
                    {metrics.map((metric, i) => (
                        <div key={i} className="flex flex-col gap-1">
                            <div className="flex items-center gap-2 text-zinc-400 mb-1">
                                {metric.icon && <metric.icon className="w-4 h-4" />}
                                <span className="text-sm font-medium">{metric.label}</span>
                            </div>
                            <div className="flex items-baseline gap-1">
                                <span className={cn("text-3xl font-bold tracking-tighter", brandColorText)}>
                                    {metric.value}
                                </span>
                                {metric.unit && <span className="text-sm text-zinc-500">{metric.unit}</span>}
                            </div>
                            {metric.trend && (
                                <div className="flex items-center gap-1 text-xs">
                                    {metric.trend === "up" ? (
                                        <TrendingUp className="w-3 h-3 text-emerald-500" />
                                    ) : metric.trend === "down" ? (
                                        <TrendingDown className="w-3 h-3 text-rose-500" />
                                    ) : null}
                                    <span className={cn(
                                        metric.trend === "up" ? "text-emerald-500" :
                                            metric.trend === "down" ? "text-rose-500" : "text-zinc-500"
                                    )}>
                                        {metric.trend === "up" ? "+2%" : metric.trend === "down" ? "-5%" : "Stable"}
                                    </span>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </motion.div>
    );
}
