Module.register("MMM-DateNightTracker", {
    defaults: {
        updateInterval: 600000,
        animationSpeed: 1000,
        dataFile: "data/friday_date_suggestion.json"
    },

    start: function() {
        Log.info("Starting module: " + this.name);
        this.dateData = null;
        this.loaded = false;
        this.scheduleUpdate();
        this.getData();
    },

    getDom: function() {
        var wrapper = document.createElement("div");
        wrapper.className = "date-night-tracker";

        if (!this.loaded) {
            wrapper.innerHTML = '<div class="dimmed light small">Loading date suggestions...</div>';
            return wrapper;
            
        }

        if (!this.dateData) {
            wrapper.innerHTML = '<div class="dimmed light small">No date suggestions available</div>';
            return wrapper;
        }

        const container = document.createElement("div");
        container.className = "date-container";

        const header = this.createHeader();
        const suggestions = this.createSuggestions();
        const footer = this.createFooter();

        container.appendChild(header);
        container.appendChild(suggestions);
        container.appendChild(footer);

        wrapper.appendChild(container);
        return wrapper;
    },

    createHeader: function() {
        const header = document.createElement("div");
        header.className = "date-header";

        const friday = this.dateData.friday_date;
        const daysSince = this.dateData.last_date.days_since;

        let urgencyClass = "";
        if (friday.urgency === "high") urgencyClass = "urgent";
        else if (friday.urgency === "medium") urgencyClass = "warning";

        header.innerHTML = `
            <div class="friday-info ${urgencyClass}">
                <span class="bright">💑 FRIDAY DATE NIGHT</span>
                <span class="dimmed small">${daysSince} days since last date</span>
            </div>
            <div class="energy-info">
                <span class="bright">⚡ Energy: ${this.dateData.weekly_health.energy_score}%</span>
                <span class="dimmed small">(${this.dateData.weekly_health.energy_level})</span>
            </div>
        `;

        return header;
    },

    createSuggestions: function() {
        const container = document.createElement("div");
        container.className = "suggestions-list";

        const suggestions = this.dateData.suggested_dates.slice(0, 3);

        suggestions.forEach((date, index) => {
            const suggestion = document.createElement("div");
            suggestion.className = "suggestion-item";

            suggestion.innerHTML = `
                <div class="suggestion-number bright">${index + 1}</div>
                <div class="suggestion-details">
                    <div class="suggestion-title bright">${date.title}</div>
                    <div class="suggestion-meta dimmed small">
                        ${date.budget} • ${date.energy} energy
                    </div>
                </div>
            `;

            container.appendChild(suggestion);
        });

        return container;
    },

    createFooter: function() {
        const footer = document.createElement("div");
        footer.className = "date-footer dimmed small";
        footer.textContent = this.dateData.friday_date.message;
        return footer;
    },

    getData: function() {
        this.sendSocketNotification("GET_DATE_DATA", this.config.dataFile);
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === "DATE_DATA") {
            this.dateData = payload;
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
        return ["MMM-DateNightTracker.css"];
    }
});
