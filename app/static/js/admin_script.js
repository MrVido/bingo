document.addEventListener('DOMContentLoaded', function() {
    const newSessionBtn = document.getElementById('new-session-btn');
    const startGameBtn = document.getElementById('start-game-btn');
    let currentSessionId = ''; // Initialize without a current session ID

    function updateGameStatus() {
        if (!currentSessionId) {
            console.log('No current session ID available, skipping game status update.');
            return;
        }

        fetch(`/admin/game_status?session_id=${currentSessionId}`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch game status');
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Update UI with data from server
                    document.getElementById('active-players').textContent = data.game_session.active_players;
                    document.getElementById('game-status').textContent = data.game_session.status;
                    // Additional UI updates can be done here
                } else {
                    console.error('Failed to fetch game status:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    }
    setInterval(updateGameStatus, 3000);

    newSessionBtn.addEventListener('click', function() {
        fetch('/admin/new_session', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    currentSessionId = data.session_id; // Update current session ID
                    document.getElementById('session-id').textContent = data.session_id;
                    updateGameStatus(); // Refresh game status with the new session
                } else {
                    alert('Failed to create new session: ' + data.error);
                }
            })
            .catch(error => console.error('Error creating new session:', error));
    });

    startGameBtn.addEventListener('click', function() {
        if (!currentSessionId) {
            alert('No session ID available. Please create a new session first.');
            return;
        }
    
        fetch('/admin/start_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: currentSessionId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Game started successfully');
                updateGameStatus(); // Refresh game status
            } else {
                alert('Failed to start game: ' + data.error);
            }
        })
        .catch(error => console.error('Error starting game:', error));
    });    
});






// document.addEventListener('DOMContentLoaded', function() {
//     // Fetch and display the user list
//     fetch('/users')
//         .then(response => response.json())
//         .then(data => {
//             const userList = document.getElementById('user-list');
//             userList.innerHTML = '<ul>' + data.users.map(user => `<li>${user}</li>`).join('') + '</ul>';
//         })
//         .catch(error => console.error('Error:', error));

//     const newSessionBtn = document.getElementById('new-session-btn');
//     const startGameBtn = document.getElementById('start-game-btn');
//     const activePlayersSpan = document.getElementById('active-players');
//     const gameStatusSpan = document.getElementById('game-status');

//     // Function to fetch and display game status and active players
//     function updateGameStatus() {
//         fetch('/admin/game_status')
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     const { id, unique_id, status, active_players, usernames } = data.game_session;
//                     activePlayersSpan.textContent = active_players;
//                     gameStatusSpan.textContent = status;
//                     const userList = document.getElementById('user-list');
//                     userList.innerHTML = '<ul>' + usernames.map(user => `<li>${user}</li>`).join('') + '</ul>';
//                     console.log(`Game Session ID: ${id}, Unique ID: ${unique_id}`);
//                 } else {
//                     console.error('Failed to fetch game status:', data.error);
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//     }

//     updateGameStatus(); // Call on page load

//     // Event listener for creating a new session
//     newSessionBtn.addEventListener('click', function() {
//         fetch('/admin/new_session', { method: 'POST' })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     alert('New session created: ' + data.session_id);
//                     updateGameStatus(); // Refresh the game status
//                 } else {
//                     alert('Failed to create new session: ' + data.error);
//                 }
//             })
//             .catch(error => console.error('Error creating new session:', error));
//     });


