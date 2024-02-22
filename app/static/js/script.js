document.addEventListener('DOMContentLoaded', function() {
    // Establish a connection to the Socket.IO server
    const socket = io.connect('http://127.0.0.1:5000');


    const registrationForm = document.getElementById('registration-form');
    const bingoBoardContainer = document.getElementById('bingo-board-container');

    registrationForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const sessionId = document.getElementById('session-id').value;
        const username = document.getElementById('username').value;

        // Emit a registration event to the server with session ID and username
        socket.emit('register', { sessionId, username });

        // After successful registration, request the bingo board from the server via Socket.IO
        socket.emit('request_board', { username });

        // Listen for a response from the server to confirm registration and board generation
        socket.on('board_generated', function(data) {
            // Check if board generation was successful and display it
            if (data.success && data.board) {
                displayBingoBoard(data.board);
            } else {
                // Handle board generation failure
                alert('Failed to load bingo board. Please try again.');
            }
        });
    });

    function displayBingoBoard(board) {
        let html = '<div class="board-grid">';
        board.forEach(row => {
            html += '<div class="board-row">';
            row.forEach(cell => {
                if (cell === 'mainsquare') {
                    html += `<div class="cell"><img src="/static/images/mainsquare.png" alt="Main Square"></div>`;
                } else {
                    html += `<div class="cell"><img src="/static/images/${cell}.png" alt="${cell}"></div>`;
                }
            });
            html += '</div>'; // Close board-row
        });
        html += '</div>'; // Close board-grid
        bingoBoardContainer.innerHTML = html;
        addClickEventToCells();
    }

    // Function to attach click events to each cell of the bingo board
    function addClickEventToCells() {
        const cells = document.querySelectorAll('.cell img');
        cells.forEach(cell => {
            cell.addEventListener('click', function() {
                this.classList.toggle('marked');
            });
        });
    }

    // Listen for real-time bingo calls from the server
    socket.on('bingo_call', function(data) {
        console.log('New bingo call:', data.item);
        // Update your UI based on the new bingo call
    });

    // Additional Socket.IO event listeners and emits as needed
});





// document.addEventListener('DOMContentLoaded', function() {
//     const registrationForm = document.getElementById('registration-form');
//     const bingoBoardContainer = document.getElementById('bingo-board-container'); // Make sure this ID matches your HTML

//     registrationForm.addEventListener('submit', function(event) {
//         event.preventDefault();
//         const sessionId = document.getElementById('session-id').value;
//         const username = document.getElementById('username').value;

//         // Register the user
//         fetch('/register', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//             },
//             body: `session_id=${encodeURIComponent(sessionId)}&username=${encodeURIComponent(username)}`
//         })
//         .then(response => {
//             if (!response.ok) throw new Error('Failed to register');
//             return response.json();
//         })
//         .then(data => {
//             // Fetch and display the bingo board after successful registration
//             fetchBingoBoard(username);
//         })
//         .catch(error => {
//             console.error('Registration failed:', error);
//             alert('Failed to register. Please try again.');
//         });
//     });

    

