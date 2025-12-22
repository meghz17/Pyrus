import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

export const dynamic = 'force-dynamic'; // Disable caching

export async function GET() {
    try {
        if (!supabase) {
            return NextResponse.json({ error: 'Supabase not configured' }, { status: 500 });
        }

        // Query both new tables in parallel
        const [whoopResult, ouraResult] = await Promise.all([
            supabase
                .from('whoop_metrics')
                .select('*')
                .order('date', { ascending: false })
                .limit(1)
                .single(),
            supabase
                .from('oura_metrics')
                .select('*')
                .order('date', { ascending: false })
                .limit(1)
                .single()
        ]);

        // Log for debugging
        console.log('[API /health] Whoop date:', whoopResult.data?.date, 'Error:', whoopResult.error?.message);
        console.log('[API /health] Oura date:', ouraResult.data?.date, 'Error:', ouraResult.error?.message);

        const whoop = whoopResult.data || {};
        const oura = ouraResult.data || {};

        // Build flat response with all metrics
        return NextResponse.json({
            // Metadata
            whoop_date: whoop.date,
            oura_date: oura.date,
            whoop_fetched_at: whoop.fetched_at,
            oura_fetched_at: oura.fetched_at,

            // Whoop Metrics (Megh)
            whoop: {
                // Recovery
                recovery_score: whoop.recovery_score,
                resting_hr: whoop.resting_hr,
                hrv: whoop.hrv_rmssd,
                spo2: whoop.spo2,
                skin_temp: whoop.skin_temp_c,

                // Sleep
                sleep_hours: whoop.sleep_hours,
                sleep_performance: whoop.sleep_performance,
                sleep_efficiency: whoop.sleep_efficiency,
                rem_hours: whoop.rem_hours,
                deep_hours: whoop.deep_hours,
                light_hours: whoop.light_hours,
                awake_hours: whoop.awake_hours,
                sleep_cycles: whoop.sleep_cycles,
                respiratory_rate: whoop.respiratory_rate,

                // Strain
                strain: whoop.strain_score,
                workout_count: whoop.workout_count,

                // Body
                height_m: whoop.height_m,
                weight_kg: whoop.weight_kg,
                max_hr: whoop.max_hr,
            },

            // Oura Metrics (Meghna)
            oura: {
                // Readiness
                readiness_score: oura.readiness_score,
                temp_deviation: oura.temp_deviation,
                hrv_balance: oura.hrv_balance,

                // Sleep
                sleep_hours: oura.sleep_hours,
                sleep_efficiency: oura.sleep_efficiency,
                rem_hours: oura.rem_hours,
                deep_hours: oura.deep_hours,
                light_hours: oura.light_hours,
                awake_hours: oura.awake_hours,
                latency_minutes: oura.latency_minutes,
                lowest_hr: oura.lowest_hr,
                average_hr: oura.average_hr,
                average_hrv: oura.average_hrv,

                // Activity
                activity_score: oura.activity_score,
                steps: oura.steps,
                active_calories: oura.active_calories,
                high_activity_minutes: oura.high_activity_minutes,

                // Stress (Gen3)
                stress_high: oura.stress_high,
                recovery_high: oura.recovery_high,

                // SpO2
                spo2: oura.spo2_avg,
            }
        });
    } catch (error) {
        console.error('[API /health] Error:', error);
        return NextResponse.json({ error: 'Failed to fetch health data' }, { status: 500 });
    }
}
