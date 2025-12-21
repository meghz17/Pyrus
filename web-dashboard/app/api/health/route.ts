import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { supabase } from '@/lib/supabase';

export async function GET() {
    try {
        // 1. Try fetching from Supabase (Cloud Database)
        if (supabase) {
            const { data, error } = await supabase
                .from('health_metrics')
                .select('user_data, wife_data, timestamp')
                .order('timestamp', { ascending: false })
                .limit(1)
                .single();

            if (!error && data) {
                return NextResponse.json({
                    ...data.user_data, // Spread user_data (whoop)
                    wife: data.wife_data, // structured as wife keys
                    timestamp: data.timestamp
                });
            }
        }

        // 2. Fallback to Local File (Development / Raspberry Pi)
        const dataPath = path.join(process.cwd(), '../data/combined_health.json');
        const datePath = path.join(process.cwd(), '../data/friday_date_suggestion.json');

        let combined = {};

        if (fs.existsSync(dataPath)) {
            const fileContents = fs.readFileSync(dataPath, 'utf8');
            combined = JSON.parse(fileContents);
        }

        if (fs.existsSync(datePath)) {
            const dateContents = fs.readFileSync(datePath, 'utf8');
            (combined as any).date_suggestion = JSON.parse(dateContents);
        }

        if (Object.keys(combined).length === 0) {
            return NextResponse.json({ error: 'No data files found' }, { status: 404 });
        }

        return NextResponse.json(combined);
    } catch (error) {
        console.error('Error reading health data:', error);
        return NextResponse.json({ error: 'Failed to fetch health data' }, { status: 500 });
    }
}
