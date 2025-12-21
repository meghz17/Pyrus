import { NextResponse } from 'next/server';
import { OpenAI } from 'openai';
import fs from 'fs';
import path from 'path';
import { supabase } from '@/lib/supabase';

// Initialize OpenAI client lazily or with a check to prevent build-time crashes
const getOpenAIClient = () => {
    const apiKey = process.env.AI_INTEGRATIONS_OPENAI_API_KEY || process.env.OPENAI_API_KEY;
    if (!apiKey) {
        return null;
    }
    return new OpenAI({
        apiKey,
        baseURL: process.env.AI_INTEGRATIONS_OPENAI_BASE_URL
    });
};

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
        const datePath = path.join(process.cwd(), '../data/friday_date_suggestion.json');

        let current = null;
        let dateSuggestion = null;

        if (fs.existsSync(dataPath)) {
            current = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
        }
        if (fs.existsSync(datePath)) {
            dateSuggestion = JSON.parse(fs.readFileSync(datePath, 'utf8'));
        }

        return { current, date_suggestion: dateSuggestion };
    } catch (e) {
        console.warn("Failed to read local data", e);
    }

    return { current: null, date_suggestion: null };
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
- Relationship-aware (Friday date nights are tradition)

**Current Data:**
`;

    if (healthData.current) {
        const current = healthData.current;
        prompt += `\n**Today's Metrics:**\n`;

        const you = current.you || {};
        const wife = current.wife || {};

        if (you.recovery) prompt += `- You: Recovery ${you.recovery.score}%, Sleep ${you.sleep?.hours || '--'}h, Strain ${you.strain?.current || '--'}\n`;
        if (wife.activity) prompt += `- Wife: Sleep ${wife.sleep?.total_hours || '--'}h, Steps ${wife.activity.steps || '--'}\n`;
    }

    if (healthData.date_suggestion) {
        const date = healthData.date_suggestion;
        prompt += `\n**Date Night Info:**\n`;
        prompt += `- Days since last date: ${date.last_date?.days_since || 'Unknown'}\n`;
        prompt += `- This week's energy: ${date.weekly_health?.energy_score}%\n`;
        if (date.suggested_dates?.length > 0) {
            prompt += `- Top Friday suggestion: ${date.suggested_dates[0].title}\n`;
        }
    }

    prompt += "\nProvide personalized, actionable health coaching based on this data.";
    return prompt;
}

export async function POST(req: Request) {
    try {
        const { messages } = await req.json();
        const openai = getOpenAIClient();

        if (!openai) {
            return NextResponse.json(
                { error: "OpenAI API Key not configured. Please add OPENAI_API_KEY to your environment variables." },
                { status: 500 }
            );
        }

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
