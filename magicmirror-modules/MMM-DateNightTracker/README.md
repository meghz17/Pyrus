# MMM-DateNightTracker

A MagicMirror² module that displays Friday date night suggestions based on weekly health analysis from dual wearables.

## Features

- **Smart Suggestions**: Shows top 3 date ideas based on combined energy levels
- **Energy-Aware**: Adapts recommendations to your weekly health trends
- **Urgency Alerts**: Visual indicators when it's been too long since last date
- **Beautiful Display**: Clean, modern interface with emoji indicators

## Installation

```bash
cd ~/MagicMirror/modules
git clone https://github.com/yourusername/MMM-DateNightTracker.git
```

## Configuration

```javascript
{
    module: "MMM-DateNightTracker",
    position: "bottom_left",
    config: {
        updateInterval: 600000,  // Update every 10 minutes
        dataFile: "data/friday_date_suggestion.json"
    }
}
```

## Data Format

Expects JSON from the Friday date suggester:
```json
{
  "friday_date": {
    "urgency": "none",
    "message": "You had a date 4 days ago..."
  },
  "last_date": {
    "days_since": 4
  },
  "weekly_health": {
    "energy_score": 73.4,
    "energy_level": "high"
  },
  "suggested_dates": [...]
}
```

## License

MIT
