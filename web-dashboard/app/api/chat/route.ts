import { NextResponse } from 'next/server';
import { OpenAI } from 'openai';
import fs from 'fs';
import path from 'path';
import { supabase } from '@/lib/supabase';

// Initialize OpenAI client
const openai = new OpenAI({
    apiKey: process.env.AI_INTEGRATIONS_OPENAI_API_KEY || process.env.OPENAI_API_KEY,
    baseURL: process.env.AI_INTEGRATIONS_OPENAI_BASE_URL
});

async function getHealthData() {
    // 1. Try Supabase
    if (supabase) {
        const { data, error } = await supabase
            .from('health_metrics')
            .select('*')
            .order('timestamp', { ascending: false })
            .limit(1)
            .single();

        if (!error && data) {
            return {
                current: {
                    you: data.user_data?.you || data.user_data, // Handle nested structure diffs
                    wife: data.wife_data?.wife || data.wife_data
                }
            };
        }
    }

    // 2. Fallback to Local Files
    try {
        const dataPath = path.join(process.cwd(), '../data/combined_health.json');
        if (fs.existsSync(dataPath)) {
            const fileContents = fs.readFileSync(dataPath, 'utf8');
            return { current: JSON.parse(fileContents) };
        }
    } catch (e) {
        console.warn("Failed to read local data", e);
    }

    return { current: null };
}

function createSystemPrompt(healthData: any) {
    let prompt = `You are Pyrus, an AI health coach for a magic mirror system. You have access to comprehensive health data from dual wearables:

**Your User (Whoop):**
- Recovery, Sleep, Strain, HRV, Resting HR

**Wife (Oura Ring):**
- Readiness, Sleep, Activity, Steps, Resting HR  

**Your Personality:**
- Warm, encouraging, and insightful
- Focus on actionable advice
- Balance health optimization with life enjoyment
- Relationship-aware

**Current Data:**
`;

    if (healthData.current) {
        const current = healthData.current;
        prompt += `\n**Today's Metrics:**\n`;

        // Safety checks for nested structures in case of slightly flexible JSON
        const you = current.you || {};
        const wife = current.wife || {};

        if (you.recovery) prompt += `- You: Recovery ${you.recovery.score}%, Sleep ${you.sleep?.hours || '--'}h, Strain ${you.strain?.current || '--'}\n`;
        if (wife.activity) prompt += `- Wife: Sleep ${wife.sleep?.total_hours || '--'}h, Steps ${wife.activity.steps || '--'}\n`;

        // Note: Can expand this to match Python script fully if 'weekly' and 'date_suggestion' files are also available/synced
    } else {
        prompt += "\n(No live health data currently available - please ask the user for context or provide general advice)\n";
    }

    prompt += "\nProvide personalized, actionable health coaching based on this data.";
    return prompt;
}

export async function POST(req: Request) {
    try {
        const { messages } = await req.json();
        const healthData = await getHealthData();
        const systemPrompt = createSystemPrompt(healthData);

        const completion = await openai.chat.completions.create({
            model: "gpt-4o",
            messages: [
                { role: "system", content: systemPrompt },
                ...messages
            ],
            temperature: 0.7,
            max_tokens: 500,
        });

        return NextResponse.json({
            role: "assistant",
            content: completion.choices[0].message.content
        });

    } catch (error: any) {
        console.error("AI Error:", error);
        return NextResponse.json(
            { error: "Failed to generate response", details: error.message },
            { status: 500 }
        );
    }
}
