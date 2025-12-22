/* MagicMirror² Pyrus Configuration
 *
 * Custom configuration for the Pyrus Magic Mirror system
 * Displays dual wearable health data, AI coaching, and date night suggestions
 *
 * Installation:
 * 1. Copy this file to ~/MagicMirror/config/config.js
 * 2. Copy custom modules to ~/MagicMirror/modules/
 * 3. Copy data directory to ~/MagicMirror/data/
 * 4. Setup cron jobs for data fetchers
 */

let config = {
	address: "0.0.0.0",
	port: 8080,
	basePath: "/",
	ipWhitelist: [],

	useHttps: false,
	httpsPrivateKey: "",
	httpsPublicKey: "",

	language: "en",
	locale: "en-US",
	logLevel: ["INFO", "LOG", "WARN", "ERROR"],
	timeFormat: 24,
	units: "metric",

	modules: [
		{
			module: "alert",
		},
		{
			module: "updatenotification",
			position: "top_bar"
		},
		{
			module: "clock",
			position: "top_left",
			config: {
				displaySeconds: false,
				showDate: true,
				showWeek: true
			}
		},
		{
			module: "calendar",
			header: "Calendar",
			position: "top_left",
			config: {
				calendars: [
					{
						fetchInterval: 7 * 24 * 60 * 60 * 1000,
						symbol: "calendar-check",
						url: "YOUR_GOOGLE_CALENDAR_URL"
					}
				]
			}
		},
		{
			module: "compliments",
			position: "lower_third",
			config: {
				compliments: {
					anytime: [
						"Looking good today!",
						"Ready to crush it!",
						"Your energy is amazing!",
						"Perfect day for an adventure!"
					]
				}
			}
		},
		{
			module: "weather",
			position: "top_right",
			config: {
				weatherProvider: "openweathermap",
				type: "current",
				location: "YOUR_CITY",
				locationID: "YOUR_LOCATION_ID",
				apiKey: "YOUR_OPENWEATHERMAP_API_KEY"
			}
		},
		{
			module: "weather",
			position: "top_right",
			header: "Weather Forecast",
			config: {
				weatherProvider: "openweathermap",
				type: "forecast",
				location: "YOUR_CITY",
				locationID: "YOUR_LOCATION_ID",
				apiKey: "YOUR_OPENWEATHERMAP_API_KEY"
			}
		},
		{
			module: "MMM-HealthDashboard",
			position: "middle_center",
			config: {
				updateInterval: 60000,
				dataFile: "data/combined_health.json",
				whoopColor: "#FF0050",
				ouraColor: "#0090FF"
			}
		},
		{
			module: "MMM-DateNightTracker",
			position: "bottom_left",
			config: {
				updateInterval: 600000,
				dataFile: "data/friday_date_suggestion.json"
			}
		},
		{
			module: "newsfeed",
			position: "bottom_bar",
			config: {
				feeds: [
					{
						title: "BBC News",
						url: "https://feeds.bbci.co.uk/news/rss.xml"
					}
				],
				showSourceTitle: true,
				showPublishDate: true,
				broadcastNewsFeeds: true,
				broadcastNewsUpdates: true
			}
		}
	]
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
