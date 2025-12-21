const NodeHelper = require("node_helper");
const fs = require("fs");
const path = require("path");

module.exports = NodeHelper.create({
    start: function() {
        console.log("Starting node helper for: " + this.name);
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === "GET_DATE_DATA") {
            this.getDateData(payload);
        }
    },

    getDateData: function(dataFile) {
        var self = this;
        
        const filePath = path.resolve(__dirname, "../../", dataFile);
        
        fs.readFile(filePath, "utf8", function(err, data) {
            if (err) {
                console.error("Error reading date data file:", err);
                self.sendSocketNotification("DATE_DATA", null);
                return;
            }

            try {
                const jsonData = JSON.parse(data);
                self.sendSocketNotification("DATE_DATA", jsonData);
            } catch (parseErr) {
                console.error("Error parsing date data JSON:", parseErr);
                self.sendSocketNotification("DATE_DATA", null);
            }
        });
    }
});
