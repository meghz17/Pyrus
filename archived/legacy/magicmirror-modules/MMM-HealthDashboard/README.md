# MMM-HealthDashboard

A MagicMirror² module that displays dual wearable health data from Whoop (user) and Oura Ring (wife) side-by-side.

## Features

- **Dual Wearable Display**: Shows health metrics from both Whoop and Oura Ring
- **Real-time Updates**: Automatically refreshes every minute
- **Color-Coded**: Whoop data in red, Oura data in blue
- **Responsive Design**: Adapts to different screen sizes

## Installation

1. Clone this repository into your MagicMirror `modules` folder:
```bash
cd ~/MagicMirror/modules
git clone https://github.com/yourusername/MMM-HealthDashboard.git
cd MMM-HealthDashboard
npm install  # Only if you add dependencies
```

2. Add the module to your `config/config.js` file:
```javascript
{
    module: "MMM-HealthDashboard",
    position: "top_left",
    config: {
        updateInterval: 60000,  // Update every minute
        dataFile: "data/combined_health.json",
        whoopColor: "#FF0050",
        ouraColor: "#0090FF"
    }
}
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `updateInterval` | Update frequency (ms) | `60000` (1 min) |
| `dataFile` | Path to combined health data JSON | `data/combined_health.json` |
| `whoopColor` | Color for Whoop metrics | `#FF0050` (red) |
| `ouraColor` | Color for Oura metrics | `#0090FF` (blue) |

## Data Format

The module expects a JSON file with this structure:
```json
{
  "you": {
    "recovery_score": 56,
    "sleep_hours": 7.4,
    "strain": 7.7,
    "resting_hr": 62,
    "hrv": 51
  },
  "wife": {
    "readiness_score": 79,
    "sleep_hours": 4.8,
    "activity_score": 47,
    "steps": 2864,
    "resting_hr": 65
  }
}
```

## Displayed Metrics

### You (Whoop)
- 💚 Recovery Score
- 😴 Sleep Hours
- 🔥 Strain
- 💓 Resting Heart Rate
- 📊 HRV (Heart Rate Variability)

### Wife (Oura)
- 🎯 Readiness Score
- 😴 Sleep Hours
- 🏃 Activity Score
- 👟 Steps
- 💓 Resting Heart Rate

## License

MIT
