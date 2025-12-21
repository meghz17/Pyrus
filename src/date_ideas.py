"""
Date Idea Generator - Comprehensive date suggestions with smart filtering
"""

from typing import List, Dict, Any, Optional
import random


# Comprehensive database of 100+ date ideas
DATE_IDEAS = [
    # ROMANTIC IDEAS (20+ ideas)
    {
        "id": 1,
        "title": "Candlelit Dinner at Home",
        "description": "Cook a romantic meal together with candles, soft music, and no distractions",
        "type": "romantic",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 2,
        "title": "Sunset Picnic",
        "description": "Pack a basket with wine and cheese, find a scenic spot, and watch the sunset together",
        "type": "romantic",
        "budget": "budget",
        "energy": "low",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 3,
        "title": "Couples Massage",
        "description": "Relax together with a professional couples massage at a spa",
        "type": "romantic",
        "budget": "splurge",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 4,
        "title": "Wine Tasting",
        "description": "Visit a local winery or wine bar to sample different wines and learn together",
        "type": "romantic",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 5,
        "title": "Stargazing Night",
        "description": "Drive to a dark spot away from city lights, bring blankets, and stargaze together",
        "type": "romantic",
        "budget": "free",
        "energy": "low",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 6,
        "title": "Breakfast in Bed",
        "description": "Surprise your partner with a homemade breakfast served in bed",
        "type": "romantic",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 7,
        "title": "Beach Sunset Walk",
        "description": "Walk hand-in-hand along the beach during golden hour",
        "type": "romantic",
        "budget": "free",
        "energy": "low",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "quick"
    },
    {
        "id": 8,
        "title": "Couples Cooking Class",
        "description": "Learn to cook a new cuisine together in a professional cooking class",
        "type": "romantic",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 9,
        "title": "Rose Petal Bath",
        "description": "Draw a warm bath with rose petals, candles, and champagne",
        "type": "romantic",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 10,
        "title": "Fancy Restaurant Date",
        "description": "Dress up and enjoy a multi-course meal at an upscale restaurant",
        "type": "romantic",
        "budget": "splurge",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 11,
        "title": "Love Letter Exchange",
        "description": "Write heartfelt letters to each other and exchange them over coffee",
        "type": "romantic",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 12,
        "title": "Hot Air Balloon Ride",
        "description": "Float above the landscape together in a romantic hot air balloon",
        "type": "romantic",
        "budget": "splurge",
        "energy": "low",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 13,
        "title": "Couples Dance Class",
        "description": "Learn salsa, tango, or ballroom dancing together",
        "type": "romantic",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 14,
        "title": "Bookstore Coffee Date",
        "description": "Browse a bookstore together, then discuss your finds over coffee",
        "type": "romantic",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 15,
        "title": "Memory Lane Drive",
        "description": "Visit places that are meaningful to your relationship: first date spot, first kiss, etc.",
        "type": "romantic",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 16,
        "title": "Weekend Getaway",
        "description": "Escape to a romantic bed and breakfast or boutique hotel for the weekend",
        "type": "romantic",
        "budget": "splurge",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "both",
        "duration": "full_day"
    },
    {
        "id": 17,
        "title": "Chocolate Tasting",
        "description": "Visit a chocolatier or create your own chocolate tasting at home",
        "type": "romantic",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 18,
        "title": "Sunrise Coffee Date",
        "description": "Wake up early to watch the sunrise together with coffee and pastries",
        "type": "romantic",
        "budget": "budget",
        "energy": "medium",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "quick"
    },
    {
        "id": 19,
        "title": "Couples Photoshoot",
        "description": "Hire a photographer or do a DIY photoshoot to capture your love",
        "type": "romantic",
        "budget": "moderate",
        "energy": "medium",
        "season": "spring",
        "indoor_outdoor": "both",
        "duration": "evening"
    },
    {
        "id": 20,
        "title": "Private Movie Screening",
        "description": "Rent out a small theater or create your own with a projector and blanket fort",
        "type": "romantic",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 21,
        "title": "Couples Spa Day",
        "description": "Spend the day at a spa with massages, facials, and hot tubs",
        "type": "romantic",
        "budget": "splurge",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "half_day"
    },
    {
        "id": 22,
        "title": "Flower Picking",
        "description": "Visit a flower farm or garden to pick fresh flowers together",
        "type": "romantic",
        "budget": "budget",
        "energy": "low",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    
    # ACTIVE IDEAS (15+ ideas)
    {
        "id": 23,
        "title": "Hiking Adventure",
        "description": "Explore a scenic hiking trail and enjoy nature together",
        "type": "active",
        "budget": "free",
        "energy": "high",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 24,
        "title": "Bike Ride",
        "description": "Cycle through town or on a scenic bike trail",
        "type": "active",
        "budget": "free",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 25,
        "title": "Rock Climbing",
        "description": "Try indoor rock climbing or outdoor bouldering together",
        "type": "active",
        "budget": "moderate",
        "energy": "high",
        "season": "any",
        "indoor_outdoor": "both",
        "duration": "evening"
    },
    {
        "id": 26,
        "title": "Kayaking",
        "description": "Paddle together on a lake, river, or ocean",
        "type": "active",
        "budget": "moderate",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 27,
        "title": "Dance the Night Away",
        "description": "Go dancing at a club or attend a live music venue with a dance floor",
        "type": "active",
        "budget": "budget",
        "energy": "high",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 28,
        "title": "Tennis Match",
        "description": "Play a friendly game of tennis at a local court",
        "type": "active",
        "budget": "free",
        "energy": "high",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "quick"
    },
    {
        "id": 29,
        "title": "Rollerblading",
        "description": "Rollerblade through the park or along the beach boardwalk",
        "type": "active",
        "budget": "budget",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 30,
        "title": "Surfing Lesson",
        "description": "Take a surfing lesson together at the beach",
        "type": "active",
        "budget": "moderate",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 31,
        "title": "Frisbee Golf",
        "description": "Play disc golf at a local course",
        "type": "active",
        "budget": "free",
        "energy": "medium",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 32,
        "title": "Swimming",
        "description": "Swim laps or play in the pool together",
        "type": "active",
        "budget": "budget",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "both",
        "duration": "evening"
    },
    {
        "id": 33,
        "title": "Paddleboarding",
        "description": "Try stand-up paddleboarding on calm waters",
        "type": "active",
        "budget": "moderate",
        "energy": "medium",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 34,
        "title": "Trampoline Park",
        "description": "Jump and play at an indoor trampoline park",
        "type": "active",
        "budget": "budget",
        "energy": "high",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 35,
        "title": "Skiing or Snowboarding",
        "description": "Hit the slopes together for winter sports",
        "type": "active",
        "budget": "splurge",
        "energy": "high",
        "season": "winter",
        "indoor_outdoor": "outdoor",
        "duration": "full_day"
    },
    {
        "id": 36,
        "title": "Yoga Class",
        "description": "Take a couples yoga or acro-yoga class",
        "type": "active",
        "budget": "budget",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 37,
        "title": "Running Together",
        "description": "Go for a scenic jog or run in a park or trail",
        "type": "active",
        "budget": "free",
        "energy": "high",
        "season": "any",
        "indoor_outdoor": "outdoor",
        "duration": "quick"
    },
    {
        "id": 38,
        "title": "Obstacle Course Race",
        "description": "Sign up for a mud run or obstacle course challenge together",
        "type": "active",
        "budget": "moderate",
        "energy": "high",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    
    # RELAXING IDEAS (15+ ideas)
    {
        "id": 39,
        "title": "Spa Day at Home",
        "description": "Create a spa experience at home with face masks, massages, and relaxation",
        "type": "relaxing",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 40,
        "title": "Beach Day",
        "description": "Relax on the beach with a good book and sun",
        "type": "relaxing",
        "budget": "free",
        "energy": "low",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "full_day"
    },
    {
        "id": 41,
        "title": "Movie Marathon",
        "description": "Binge-watch a series or trilogy with snacks and blankets",
        "type": "relaxing",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "half_day"
    },
    {
        "id": 42,
        "title": "Stargazing",
        "description": "Lie under the stars and identify constellations together",
        "type": "relaxing",
        "budget": "free",
        "energy": "low",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 43,
        "title": "Meditation Session",
        "description": "Practice meditation or mindfulness together",
        "type": "relaxing",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "both",
        "duration": "quick"
    },
    {
        "id": 44,
        "title": "Hammock Lounging",
        "description": "Relax in a hammock together, reading or napping",
        "type": "relaxing",
        "budget": "budget",
        "energy": "low",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 45,
        "title": "Botanical Garden Stroll",
        "description": "Walk slowly through beautiful gardens and enjoy the plants",
        "type": "relaxing",
        "budget": "budget",
        "energy": "low",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 46,
        "title": "Coffee Shop Relaxation",
        "description": "Spend hours at a cozy coffee shop reading, talking, or working on laptops",
        "type": "relaxing",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 47,
        "title": "Scenic Drive",
        "description": "Take a leisurely drive through beautiful countryside or coastal roads",
        "type": "relaxing",
        "budget": "budget",
        "energy": "low",
        "season": "fall",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 48,
        "title": "Afternoon Tea",
        "description": "Enjoy a proper afternoon tea service with scones and finger sandwiches",
        "type": "relaxing",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 49,
        "title": "Puzzle Together",
        "description": "Work on a large jigsaw puzzle over several hours or days",
        "type": "relaxing",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 50,
        "title": "Float Therapy",
        "description": "Try sensory deprivation float tanks for deep relaxation",
        "type": "relaxing",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 51,
        "title": "Bird Watching",
        "description": "Bring binoculars and observe birds in nature",
        "type": "relaxing",
        "budget": "free",
        "energy": "low",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 52,
        "title": "Lake Day",
        "description": "Relax by a peaceful lake, maybe with a picnic",
        "type": "relaxing",
        "budget": "free",
        "energy": "low",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 53,
        "title": "Fireplace Evening",
        "description": "Cuddle by the fireplace with hot cocoa and conversation",
        "type": "relaxing",
        "budget": "free",
        "energy": "low",
        "season": "winter",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    
    # ADVENTURE IDEAS (10+ ideas)
    {
        "id": 54,
        "title": "Road Trip",
        "description": "Take an impromptu road trip to somewhere you've never been",
        "type": "adventure",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "outdoor",
        "duration": "full_day"
    },
    {
        "id": 55,
        "title": "Escape Room",
        "description": "Solve puzzles and work together to escape a themed room",
        "type": "adventure",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 56,
        "title": "Zip Lining",
        "description": "Soar through the treetops on a zip line course",
        "type": "adventure",
        "budget": "moderate",
        "energy": "high",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 57,
        "title": "White Water Rafting",
        "description": "Navigate rapids together in a raft",
        "type": "adventure",
        "budget": "moderate",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 58,
        "title": "Skydiving",
        "description": "Jump out of a plane together (tandem jumps available)",
        "type": "adventure",
        "budget": "splurge",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 59,
        "title": "Haunted House",
        "description": "Brave a haunted house attraction together",
        "type": "adventure",
        "budget": "budget",
        "energy": "medium",
        "season": "fall",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 60,
        "title": "Scuba Diving",
        "description": "Explore underwater worlds together",
        "type": "adventure",
        "budget": "splurge",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "full_day"
    },
    {
        "id": 61,
        "title": "Camping Trip",
        "description": "Spend a night or two camping in the wilderness",
        "type": "adventure",
        "budget": "budget",
        "energy": "medium",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "full_day"
    },
    {
        "id": 62,
        "title": "Cave Exploration",
        "description": "Go spelunking or tour underground caves",
        "type": "adventure",
        "budget": "moderate",
        "energy": "high",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "half_day"
    },
    {
        "id": 63,
        "title": "Parasailing",
        "description": "Fly high above the water while parasailing",
        "type": "adventure",
        "budget": "moderate",
        "energy": "medium",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "quick"
    },
    {
        "id": 64,
        "title": "ATV Riding",
        "description": "Ride all-terrain vehicles through trails",
        "type": "adventure",
        "budget": "moderate",
        "energy": "high",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 65,
        "title": "Bungee Jumping",
        "description": "Take the leap together from a bungee platform",
        "type": "adventure",
        "budget": "moderate",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "quick"
    },
    
    # CULTURAL IDEAS (15+ ideas)
    {
        "id": 66,
        "title": "Art Museum Visit",
        "description": "Explore an art museum and discuss your favorite pieces",
        "type": "cultural",
        "budget": "budget",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 67,
        "title": "Live Concert",
        "description": "See a band or orchestra perform live",
        "type": "cultural",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 68,
        "title": "Theater Show",
        "description": "Watch a play, musical, or comedy show",
        "type": "cultural",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 69,
        "title": "Art Gallery Opening",
        "description": "Attend a local art gallery opening with wine and appetizers",
        "type": "cultural",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 70,
        "title": "Cooking Class",
        "description": "Learn to make a new cuisine from a chef",
        "type": "cultural",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 71,
        "title": "Historical Site Tour",
        "description": "Visit a historical landmark or take a guided heritage tour",
        "type": "cultural",
        "budget": "budget",
        "energy": "medium",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 72,
        "title": "Poetry Reading",
        "description": "Attend a poetry slam or reading at a local venue",
        "type": "cultural",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 73,
        "title": "Science Museum",
        "description": "Explore interactive exhibits at a science museum",
        "type": "cultural",
        "budget": "budget",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 74,
        "title": "Food Festival",
        "description": "Sample diverse foods at a local food festival or fair",
        "type": "cultural",
        "budget": "moderate",
        "energy": "medium",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 75,
        "title": "Jazz Club Night",
        "description": "Enjoy live jazz music at an intimate club",
        "type": "cultural",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 76,
        "title": "Pottery Class",
        "description": "Create pottery together on a pottery wheel",
        "type": "cultural",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 77,
        "title": "Cultural Festival",
        "description": "Experience a cultural festival celebrating different traditions",
        "type": "cultural",
        "budget": "budget",
        "energy": "medium",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 78,
        "title": "Symphony Orchestra",
        "description": "Dress up for a classical music performance",
        "type": "cultural",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 79,
        "title": "Architecture Tour",
        "description": "Take a walking tour focused on local architecture",
        "type": "cultural",
        "budget": "free",
        "energy": "medium",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 80,
        "title": "Documentary Screening",
        "description": "Watch a thought-provoking documentary and discuss it",
        "type": "cultural",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 81,
        "title": "Library Event",
        "description": "Attend a book reading, lecture, or author event at the library",
        "type": "cultural",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    
    # FUN IDEAS (15+ ideas)
    {
        "id": 82,
        "title": "Bowling Night",
        "description": "Bowl a few games and enjoy classic arcade fun",
        "type": "fun",
        "budget": "budget",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 83,
        "title": "Mini Golf",
        "description": "Play mini golf and compete for the lowest score",
        "type": "fun",
        "budget": "budget",
        "energy": "low",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "quick"
    },
    {
        "id": 84,
        "title": "Arcade Games",
        "description": "Compete at classic and modern arcade games",
        "type": "fun",
        "budget": "budget",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 85,
        "title": "Karaoke Night",
        "description": "Sing your hearts out at a karaoke bar or private room",
        "type": "fun",
        "budget": "budget",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 86,
        "title": "Board Game Cafe",
        "description": "Try new board games at a cafe dedicated to gaming",
        "type": "fun",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 87,
        "title": "Go-Kart Racing",
        "description": "Race each other on a go-kart track",
        "type": "fun",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "both",
        "duration": "quick"
    },
    {
        "id": 88,
        "title": "Comedy Show",
        "description": "Laugh together at a stand-up comedy performance",
        "type": "fun",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 89,
        "title": "Farmers Market",
        "description": "Browse local produce and artisan goods at a farmers market",
        "type": "fun",
        "budget": "budget",
        "energy": "medium",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "quick"
    },
    {
        "id": 90,
        "title": "Trivia Night",
        "description": "Team up for trivia night at a local bar or restaurant",
        "type": "fun",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 91,
        "title": "Amusement Park",
        "description": "Ride roller coasters and enjoy carnival games",
        "type": "fun",
        "budget": "moderate",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "full_day"
    },
    {
        "id": 92,
        "title": "Water Park",
        "description": "Splash around on water slides and in wave pools",
        "type": "fun",
        "budget": "moderate",
        "energy": "high",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "half_day"
    },
    {
        "id": 93,
        "title": "Laser Tag",
        "description": "Battle it out in a laser tag arena",
        "type": "fun",
        "budget": "budget",
        "energy": "high",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 94,
        "title": "Drive-In Movie",
        "description": "Watch a movie from the comfort of your car at a drive-in theater",
        "type": "fun",
        "budget": "budget",
        "energy": "low",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 95,
        "title": "Ice Skating",
        "description": "Skate together at an ice rink",
        "type": "fun",
        "budget": "budget",
        "energy": "medium",
        "season": "winter",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 96,
        "title": "Painting and Sipping",
        "description": "Create art together while enjoying wine at a paint-and-sip studio",
        "type": "fun",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 97,
        "title": "Scavenger Hunt",
        "description": "Create or join a city-wide scavenger hunt adventure",
        "type": "fun",
        "budget": "free",
        "energy": "medium",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    
    # HOME IDEAS (15+ ideas)
    {
        "id": 98,
        "title": "Cook a New Recipe Together",
        "description": "Choose a challenging recipe and cook it together from scratch",
        "type": "home",
        "budget": "budget",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 99,
        "title": "Board Game Night",
        "description": "Play your favorite board games or try new ones at home",
        "type": "home",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 100,
        "title": "Movie Night at Home",
        "description": "Create a theater experience with popcorn, candy, and comfy seating",
        "type": "home",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 101,
        "title": "DIY Project",
        "description": "Build or create something together: furniture, art, or home decor",
        "type": "home",
        "budget": "moderate",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "half_day"
    },
    {
        "id": 102,
        "title": "Gardening Together",
        "description": "Plant flowers, vegetables, or herbs in your garden or pots",
        "type": "home",
        "budget": "budget",
        "energy": "medium",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 103,
        "title": "Video Game Marathon",
        "description": "Play co-op or competitive video games together",
        "type": "home",
        "budget": "free",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 104,
        "title": "Baking Challenge",
        "description": "Bake cookies, cakes, or pastries together",
        "type": "home",
        "budget": "budget",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 105,
        "title": "Home Workout Session",
        "description": "Exercise together with online videos or create your own routine",
        "type": "home",
        "budget": "free",
        "energy": "high",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
    {
        "id": 106,
        "title": "Backyard Camping",
        "description": "Set up a tent in your backyard and camp under the stars",
        "type": "home",
        "budget": "free",
        "energy": "low",
        "season": "summer",
        "indoor_outdoor": "outdoor",
        "duration": "full_day"
    },
    {
        "id": 107,
        "title": "Wine and Cheese Tasting",
        "description": "Create a tasting experience at home with different wines and cheeses",
        "type": "home",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 108,
        "title": "Photo Album Creation",
        "description": "Organize and create a photo album or scrapbook of memories",
        "type": "home",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 109,
        "title": "Karaoke at Home",
        "description": "Sing along to your favorite songs with a karaoke app or YouTube",
        "type": "home",
        "budget": "free",
        "energy": "medium",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 110,
        "title": "Porch/Patio Dinner",
        "description": "Set up a nice dinner on your porch or patio with string lights",
        "type": "home",
        "budget": "budget",
        "energy": "low",
        "season": "spring",
        "indoor_outdoor": "outdoor",
        "duration": "evening"
    },
    {
        "id": 111,
        "title": "Arts and Crafts",
        "description": "Get creative with painting, drawing, or other craft projects",
        "type": "home",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 112,
        "title": "Home Spa Night",
        "description": "Give each other massages, facials, and foot soaks at home",
        "type": "home",
        "budget": "budget",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "evening"
    },
    {
        "id": 113,
        "title": "Cocktail Making",
        "description": "Learn to make new cocktails together and host your own bar",
        "type": "home",
        "budget": "moderate",
        "energy": "low",
        "season": "any",
        "indoor_outdoor": "indoor",
        "duration": "quick"
    },
]


def get_all_ideas() -> List[Dict[str, Any]]:
    """Return all date ideas"""
    return DATE_IDEAS.copy()


def filter_by_budget(budget: str, ideas: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Filter ideas by budget category
    
    Args:
        budget: Budget category (free, budget, moderate, splurge)
        ideas: Optional list of ideas to filter from. If None, uses all ideas.
    
    Returns:
        List of filtered date ideas
    """
    if ideas is None:
        ideas = DATE_IDEAS
    
    return [idea for idea in ideas if idea["budget"] == budget]


def filter_by_energy(energy: str, ideas: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Filter ideas by energy level
    
    Args:
        energy: Energy level (low, medium, high)
        ideas: Optional list of ideas to filter from. If None, uses all ideas.
    
    Returns:
        List of filtered date ideas
    """
    if ideas is None:
        ideas = DATE_IDEAS
    
    return [idea for idea in ideas if idea["energy"] == energy]


def filter_by_type(date_type: str, ideas: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Filter ideas by type
    
    Args:
        date_type: Type of date (romantic, active, relaxing, adventure, cultural, fun, home)
        ideas: Optional list of ideas to filter from. If None, uses all ideas.
    
    Returns:
        List of filtered date ideas
    """
    if ideas is None:
        ideas = DATE_IDEAS
    
    return [idea for idea in ideas if idea["type"] == date_type]


def filter_by_season(season: str, ideas: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Filter ideas by season
    
    Args:
        season: Season (any, spring, summer, fall, winter)
        ideas: Optional list of ideas to filter from. If None, uses all ideas.
    
    Returns:
        List of filtered date ideas
    """
    if ideas is None:
        ideas = DATE_IDEAS
    
    # Return ideas that work for the specified season or work for "any" season
    return [idea for idea in ideas if idea["season"] == season or idea["season"] == "any"]


def filter_by_indoor_outdoor(location: str, ideas: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Filter ideas by indoor/outdoor setting
    
    Args:
        location: Location type (indoor, outdoor, both)
        ideas: Optional list of ideas to filter from. If None, uses all ideas.
    
    Returns:
        List of filtered date ideas
    """
    if ideas is None:
        ideas = DATE_IDEAS
    
    # Return ideas that match the location or work for "both"
    return [idea for idea in ideas if idea["indoor_outdoor"] == location or idea["indoor_outdoor"] == "both"]


def filter_by_duration(duration: str, ideas: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Filter ideas by duration
    
    Args:
        duration: Duration (quick, evening, half_day, full_day)
        ideas: Optional list of ideas to filter from. If None, uses all ideas.
    
    Returns:
        List of filtered date ideas
    """
    if ideas is None:
        ideas = DATE_IDEAS
    
    return [idea for idea in ideas if idea["duration"] == duration]


def get_random_ideas(count: int = 3, filters: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """
    Get random date ideas with optional filters
    
    Args:
        count: Number of random ideas to return
        filters: Optional dictionary of filters to apply
                Keys can be: type, budget, energy, season, indoor_outdoor, duration
    
    Returns:
        List of random date ideas
    """
    ideas = DATE_IDEAS.copy()
    
    # Apply filters if provided
    if filters:
        if "type" in filters:
            ideas = filter_by_type(filters["type"], ideas)
        if "budget" in filters:
            ideas = filter_by_budget(filters["budget"], ideas)
        if "energy" in filters:
            ideas = filter_by_energy(filters["energy"], ideas)
        if "season" in filters:
            ideas = filter_by_season(filters["season"], ideas)
        if "indoor_outdoor" in filters:
            ideas = filter_by_indoor_outdoor(filters["indoor_outdoor"], ideas)
        if "duration" in filters:
            ideas = filter_by_duration(filters["duration"], ideas)
    
    # Return random sample
    return random.sample(ideas, min(count, len(ideas)))


def search_ideas(query: str) -> List[Dict[str, Any]]:
    """
    Search ideas by keyword in title or description
    
    Args:
        query: Search query string
    
    Returns:
        List of matching date ideas
    """
    query_lower = query.lower()
    return [
        idea for idea in DATE_IDEAS 
        if query_lower in idea["title"].lower() or query_lower in idea["description"].lower()
    ]


def suggest_based_on_energy(recovery_score: float, readiness_score: Optional[float] = None) -> List[Dict[str, Any]]:
    """
    Suggest date ideas based on health/energy levels from Whoop or Oura data
    
    Args:
        recovery_score: Recovery/readiness score as percentage (0-100)
        readiness_score: Optional second score to average (0-100)
    
    Returns:
        List of suggested date ideas based on energy levels
    """
    # Calculate average score if both are provided
    if readiness_score is not None:
        avg_score = (recovery_score + readiness_score) / 2
    else:
        avg_score = recovery_score
    
    # Determine energy level and appropriate date types
    if avg_score >= 70:
        # High energy - suggest active or adventure dates
        energy_filter = "high"
        types = ["active", "adventure"]
        print(f"🔥 High energy detected ({avg_score:.1f}%)! Suggesting active/adventure dates.")
    elif avg_score >= 50:
        # Medium energy - suggest moderate activities
        energy_filter = "medium"
        types = ["cultural", "fun", "romantic"]
        print(f"⚡ Medium energy ({avg_score:.1f}%). Suggesting cultural/fun dates.")
    else:
        # Low energy - suggest relaxing or home activities
        energy_filter = "low"
        types = ["relaxing", "home", "romantic"]
        print(f"😴 Low energy ({avg_score:.1f}%). Suggesting relaxing/home dates.")
    
    # Get ideas matching the energy level
    ideas = filter_by_energy(energy_filter)
    
    # Further filter by preferred types
    type_filtered = [idea for idea in ideas if idea["type"] in types]
    
    # If we have enough filtered ideas, use those; otherwise fall back to all energy-matched ideas
    if len(type_filtered) >= 5:
        suggestions = type_filtered
    else:
        suggestions = ideas
    
    # Return random selection of 5 suggestions
    return random.sample(suggestions, min(5, len(suggestions)))


def get_statistics() -> Dict[str, Any]:
    """
    Get statistics about the date idea database
    
    Returns:
        Dictionary with statistics about the ideas
    """
    stats = {
        "total_ideas": len(DATE_IDEAS),
        "by_type": {},
        "by_budget": {},
        "by_energy": {},
        "by_season": {},
        "by_indoor_outdoor": {},
        "by_duration": {}
    }
    
    # Count by each category
    for idea in DATE_IDEAS:
        # Count by type
        stats["by_type"][idea["type"]] = stats["by_type"].get(idea["type"], 0) + 1
        
        # Count by budget
        stats["by_budget"][idea["budget"]] = stats["by_budget"].get(idea["budget"], 0) + 1
        
        # Count by energy
        stats["by_energy"][idea["energy"]] = stats["by_energy"].get(idea["energy"], 0) + 1
        
        # Count by season
        stats["by_season"][idea["season"]] = stats["by_season"].get(idea["season"], 0) + 1
        
        # Count by indoor/outdoor
        stats["by_indoor_outdoor"][idea["indoor_outdoor"]] = stats["by_indoor_outdoor"].get(idea["indoor_outdoor"], 0) + 1
        
        # Count by duration
        stats["by_duration"][idea["duration"]] = stats["by_duration"].get(idea["duration"], 0) + 1
    
    return stats


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("DATE IDEA GENERATOR - Testing and Examples")
    print("=" * 60)
    
    # Show statistics
    stats = get_statistics()
    print(f"\n📊 DATABASE STATISTICS:")
    print(f"Total Ideas: {stats['total_ideas']}")
    print(f"\nBy Type: {stats['by_type']}")
    print(f"By Budget: {stats['by_budget']}")
    print(f"By Energy: {stats['by_energy']}")
    print(f"By Season: {stats['by_season']}")
    
    # Test filtering
    print("\n" + "=" * 60)
    print("🔍 FILTERING EXAMPLES:")
    print("=" * 60)
    
    romantic_ideas = filter_by_type("romantic")
    print(f"\n💕 Romantic Ideas: {len(romantic_ideas)} found")
    for idea in romantic_ideas[:3]:
        print(f"  - {idea['title']} ({idea['budget']}, {idea['energy']} energy)")
    
    free_ideas = filter_by_budget("free")
    print(f"\n💰 Free Ideas: {len(free_ideas)} found")
    for idea in free_ideas[:3]:
        print(f"  - {idea['title']} ({idea['type']})")
    
    # Test random with filters
    print("\n" + "=" * 60)
    print("🎲 RANDOM SUGGESTIONS:")
    print("=" * 60)
    
    random_ideas = get_random_ideas(3, {"budget": "budget", "energy": "low"})
    print(f"\n3 Budget-friendly, low-energy ideas:")
    for idea in random_ideas:
        print(f"  - {idea['title']}")
        print(f"    {idea['description']}")
    
    # Test search
    print("\n" + "=" * 60)
    print("🔎 SEARCH EXAMPLES:")
    print("=" * 60)
    
    search_results = search_ideas("music")
    print(f"\nSearching for 'music': {len(search_results)} results")
    for idea in search_results:
        print(f"  - {idea['title']}")
    
    # Test energy-based suggestions
    print("\n" + "=" * 60)
    print("⚡ ENERGY-BASED SUGGESTIONS:")
    print("=" * 60)
    
    print("\nHigh energy scenario (recovery: 85%):")
    high_energy_ideas = suggest_based_on_energy(85)
    for idea in high_energy_ideas:
        print(f"  - {idea['title']} ({idea['type']}, {idea['energy']} energy)")
    
    print("\nLow energy scenario (recovery: 40%):")
    low_energy_ideas = suggest_based_on_energy(40)
    for idea in low_energy_ideas:
        print(f"  - {idea['title']} ({idea['type']}, {idea['energy']} energy)")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
