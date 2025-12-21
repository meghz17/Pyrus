import { NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';
import fs from 'fs';
import path from 'path';
import { supabase } from '@/lib/supabase';

// Initialize Gemini client lazily
const getGeminiClient = () => {
    const apiKey = process.env.GEMINI_API_KEY || process.env.AI_INTEGRATIONS_GEMINI_API_KEY;
    if (!apiKey) {
        return null;
    }
    return new GoogleGenerativeAI(apiKey);
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
                    you: data.user_data?.you || data.user_data,
                    wife: data.wife_data?.wife || data.wife_data
                },
                date_suggestion: data.date_suggestion
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

**Meghna (Oura Ring):**
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
        if (wife.activity) prompt += `- Meghna: Sleep ${wife.sleep?.total_hours || '--'}h, Steps ${wife.activity?.steps || '--'}\n`;
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
        const genAI = getGeminiClient();

        if (!genAI) {
            return NextResponse.json(
                { error: "Gemini API Key not configured. Please add GEMINI_API_KEY to your environment variables." },
                { status: 500 }
            );
        }

        const healthData = await getHealthData();
        const systemPrompt = createSystemPrompt(healthData);

        // Configure model
        const model = genAI.getGenerativeModel({
            model: "gemini-1.5-flash",
            systemInstruction: systemPrompt,
        });

        // Gemini history must be strictly validated
        // 1. Map roles: 'assistant' -> 'model', 'user' -> 'user'
        // 2. Ensure history is not empty if we are starting a chat with it
        // 3. (Crucial) The FIRST message in 'history' must be from 'user'.

        let history = messages.slice(0, -1).map((m: any) => ({
            role: m.role === 'assistant' ? 'model' : 'user',
            parts: [{ text: m.content }]
        }));

        // If history exists but starts with 'model', prepend a dummy user message or shift it.
        // For a chatbot, if the first msg in DB is assistant (greeting?), Gemini rejects it.
        if (history.length > 0 && history[0].role === 'model') {
            // Option: Filter it out or prepend context. Filtering is safer for the API error.
            // Or better: Prepend a context-setting user message if needed.
            // Let's just remove leading model messages to comply with "First content... user".
            while (history.length > 0 && history[0].role === 'model') {
                history.shift();
            }
        }

        const lastMessage = messages[messages.length - 1];

        const chat = model.startChat({
            history: history,
            generationConfig: {
                maxOutputTokens: 500,
            },
        });

        const result = await chat.sendMessage(lastMessage.content);
        const response = await result.response;
        const text = response.text();

        return NextResponse.json({
            role: "assistant",
            content: text
        });

    } catch (error: any) {
        console.error("AI Error:", error);
        return NextResponse.json(
            { error: "Failed to generate response", details: error.message },
            { status: 500 }
        );
    }
}
