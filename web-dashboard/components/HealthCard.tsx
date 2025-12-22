"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@/lib/utils";

interface Metric {
    label: string;
    value: string | number;
    unit?: string;
    icon?: React.ElementType;
    primary?: boolean; // Show in collapsed view
}

interface HealthCardProps {
    title: string;
    type: "whoop" | "oura";
    metrics: Metric[];
    lastUpdated?: string;
}

// Get color based on metric value (for percentage metrics)
function getValueColor(value: string | number, brandColor: string): string {
    if (typeof value === "string" && value === "N/A") return "text-zinc-600";
    const num = typeof value === "string" ? parseFloat(value) : value;
    if (isNaN(num)) return brandColor;
    if (num >= 70) return "text-emerald-400";
    if (num >= 40) return "text-amber-400";
    if (num < 40 && num > 0) return "text-rose-400";
    return brandColor;
}

export function HealthCard({ title, type, metrics, lastUpdated }: HealthCardProps) {
    const [expanded, setExpanded] = useState(false);
    const isWhoop = type === "whoop";
    const brandColor = isWhoop ? "bg-red-500" : "bg-blue-500";
    const brandColorText = isWhoop ? "text-red-400" : "text-blue-400";
    const brandRing = isWhoop ? "ring-red-500/30" : "ring-blue-500/30";

    // Split metrics: first 4 are primary, rest are secondary
    const primaryMetrics = metrics.slice(0, 4);
    const secondaryMetrics = metrics.slice(4);

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
                "relative overflow-hidden rounded-3xl border border-zinc-800/50",
                "bg-gradient-to-br from-zinc-900/90 to-zinc-900/50 backdrop-blur-xl",
                "p-6 shadow-2xl transition-all duration-300",
                expanded && "ring-2",
                expanded && brandRing
            )}
        >
            {/* Background Glow */}
            <div className={cn(
                "absolute -right-20 -top-20 h-48 w-48 rounded-full blur-3xl opacity-10",
                brandColor
            )} />

            <div className="relative z-10">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <div className={cn("h-2.5 w-2.5 rounded-full", brandColor)} />
                        <h2 className="text-lg font-bold tracking-tight text-zinc-100">{title}</h2>
                    </div>
                    {lastUpdated && (
                        <span className="text-xs font-medium text-zinc-600 uppercase tracking-wider">
                            {lastUpdated}
                        </span>
                    )}
                </div>

                {/* Primary Metrics (Always Visible) */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    {primaryMetrics.map((metric, i) => (
                        <div
                            key={i}
                            className="flex flex-col gap-1 p-3 rounded-2xl bg-zinc-800/30 border border-zinc-800/50"
                        >
                            <div className="flex items-center gap-1.5 text-zinc-500">
                                {metric.icon && <metric.icon className="w-3.5 h-3.5" />}
                                <span className="text-xs font-medium">{metric.label}</span>
                            </div>
                            <div className="flex items-baseline gap-1">
                                <span className={cn(
                                    "text-2xl font-bold tracking-tight",
                                    metric.label.includes("%") || metric.label.includes("Recovery") || metric.label.includes("Readiness") || metric.label.includes("Activity") || metric.label.includes("Sleep Perf")
                                        ? getValueColor(metric.value, brandColorText)
                                        : brandColorText
                                )}>
                                    {metric.value}
                                </span>
                                {metric.unit && (
                                    <span className="text-xs text-zinc-500">{metric.unit}</span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Expand/Collapse Button */}
                {secondaryMetrics.length > 0 && (
                    <button
                        onClick={() => setExpanded(!expanded)}
                        className={cn(
                            "w-full flex items-center justify-center gap-2 py-2 rounded-xl",
                            "text-xs font-medium text-zinc-500 hover:text-zinc-300",
                            "bg-zinc-800/20 hover:bg-zinc-800/40 transition-colors"
                        )}
                    >
                        {expanded ? (
                            <>
                                <ChevronUp className="w-4 h-4" />
                                Hide Details
                            </>
                        ) : (
                            <>
                                <ChevronDown className="w-4 h-4" />
                                Show {secondaryMetrics.length} More Metrics
                            </>
                        )}
                    </button>
                )}

                {/* Secondary Metrics (Expandable) */}
                <AnimatePresence>
                    {expanded && (
                        <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: "auto", opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.2 }}
                            className="overflow-hidden"
                        >
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-4 border-t border-zinc-800/50 mt-4">
                                {secondaryMetrics.map((metric, i) => (
                                    <div key={i} className="flex flex-col gap-0.5">
                                        <div className="flex items-center gap-1 text-zinc-500">
                                            {metric.icon && <metric.icon className="w-3 h-3" />}
                                            <span className="text-xs">{metric.label}</span>
                                        </div>
                                        <div className="flex items-baseline gap-1">
                                            <span className={cn("text-lg font-semibold", brandColorText)}>
                                                {metric.value}
                                            </span>
                                            {metric.unit && (
                                                <span className="text-xs text-zinc-600">{metric.unit}</span>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </motion.div>
    );
}
