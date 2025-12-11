async function refreshData() {
    try {
        const response = await fetch("https://breathalyzer-api.onrender.com/status");
        const data = await response.json();

        document.getElementById("status").innerText = data.status;
        document.getElementById("timestamp").innerText = data.timestamp;

        if (data.last_image) {
            document.getElementById("img").src = data.last_image;
        }

    } catch (err) {
        console.log("Waiting for Pi updates...");
    }
}

setInterval(refreshData, 2000);
refreshData();
