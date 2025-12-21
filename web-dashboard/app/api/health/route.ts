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

        if (!fs.existsSync(dataPath)) {
            return NextResponse.json({ error: 'Data file not found' }, { status: 404 });
        }

        const fileContents = fs.readFileSync(dataPath, 'utf8');
        const data = JSON.parse(fileContents);

        return NextResponse.json(data);
    } catch (error) {
        console.error('Error reading health data:', error);
        return NextResponse.json({ error: 'Failed to fetch health data' }, { status: 500 });
    }
}
