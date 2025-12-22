Module.register("MMM-HealthDashboard", {
    defaults: {
        updateInterval: 60000,
        animationSpeed: 1000,
        dataFile: "data/combined_health.json",
        whoopColor: "#FF0050",
        ouraColor: "#0090FF"
    },

    start: function() {
        Log.info("Starting module: " + this.name);
        this.healthData = null;
        this.loaded = false;
        this.scheduleUpdate();
        this.getData();
    },

    getDom: function() {
        var wrapper = document.createElement("div");
        wrapper.className = "health-dashboard";

        if (!this.loaded) {
            wrapper.innerHTML = '<div class="dimmed light small">Loading health data...</div>';
            return wrapper;
        }

        if (!this.healthData) {
            wrapper.innerHTML = '<div class="dimmed light small">No health data available</div>';
            return wrapper;
        }

        const container = document.createElement("div");
        container.className = "health-container";

        const youSection = this.createPersonSection("you", "YOU (WHOOP)", this.config.whoopColor);
        const wifeSection = this.createPersonSection("wife", "WIFE (OURA)", this.config.ouraColor);

        container.appendChild(youSection);
        container.appendChild(this.createDivider());
        container.appendChild(wifeSection);

        wrapper.appendChild(container);
        return wrapper;
    },

    createPersonSection: function(person, title, color) {
        const section = document.createElement("div");
        section.className = "person-section";

        const header = document.createElement("div");
        header.className = "person-header";
        header.style.borderBottom = `3px solid ${color}`;
        header.innerHTML = `<span class="bright">${title}</span>`;
        section.appendChild(header);

        const data = this.healthData[person];
        if (!data) {
            section.innerHTML += '<div class="dimmed small">No data available</div>';
            return section;
        }

        const metrics = document.createElement("div");
        metrics.className = "metrics";

        if (person === "you") {
            metrics.appendChild(this.createMetric("💚 Recovery", data.recovery_score, "%", color));
            metrics.appendChild(this.createMetric("😴 Sleep", data.sleep_hours, "h", color));
            metrics.appendChild(this.createMetric("🔥 Strain", data.strain, "", color));
            metrics.appendChild(this.createMetric("💓 Resting HR", data.resting_hr, "bpm", color));
            metrics.appendChild(this.createMetric("📊 HRV", data.hrv, "ms", color));
        } else {
            metrics.appendChild(this.createMetric("🎯 Readiness", data.readiness_score, "%", color));
            metrics.appendChild(this.createMetric("😴 Sleep", data.sleep_hours, "h", color));
            metrics.appendChild(this.createMetric("🏃 Activity", data.activity_score, "%", color));
            metrics.appendChild(this.createMetric("👟 Steps", data.steps, "", color));
            metrics.appendChild(this.createMetric("💓 Resting HR", data.resting_hr, "bpm", color));
        }

        section.appendChild(metrics);
        return section;
    },

    createMetric: function(label, value, unit, color) {
        const metric = document.createElement("div");
        metric.className = "metric-row";

        const labelSpan = document.createElement("span");
        labelSpan.className = "metric-label dimmed";
        labelSpan.textContent = label;

        const valueSpan = document.createElement("span");
        valueSpan.className = "metric-value bright";
        valueSpan.style.color = color;

        if (value !== null && value !== undefined) {
            valueSpan.textContent = `${value}${unit}`;
        } else {
            valueSpan.textContent = "N/A";
            valueSpan.className += " dimmed";
        }

        metric.appendChild(labelSpan);
        metric.appendChild(valueSpan);
        return metric;
    },

    createDivider: function() {
        const divider = document.createElement("div");
        divider.className = "health-divider";
        return divider;
    },

    getData: function() {
        this.sendSocketNotification("GET_HEALTH_DATA", this.config.dataFile);
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === "HEALTH_DATA") {
            this.healthData = payload;
            this.loaded = true;
            this.updateDom(this.config.animationSpeed);
        }
    },

    scheduleUpdate: function() {
        var self = this;
        setInterval(function() {
            self.getData();
        }, this.config.updateInterval);
    },

    getStyles: function() {
        return ["MMM-HealthDashboard.css"];
    }
});
