document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch game data from the server
    function fetchGameData() {
        fetch('/game_data')  // Update URL to match Flask server endpoint
            .then(response => response.json())
            .then(data => {
                // Update UI with game statistics
                updateGameStatistics(data);
            })
            .catch(error => console.error('Error:', error));
    }

    // Function to update the UI with game statistics
    function updateGameStatistics(data) {
        // Display game statistics in the admin panel
        const activePlayersCount = data.active_players;
        const gameStatus = data.game_status;

        // Update HTML elements with the fetched data
        document.getElementById('active-players').innerText = activePlayersCount;
        document.getElementById('game-status').innerText = gameStatus;
    }

    // Fetch game data when the page loads
    fetchGameData();
});
