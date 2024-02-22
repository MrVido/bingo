document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registration-form');
    const bingoBoardContainer = document.getElementById('bingo-board-container'); // Make sure this ID matches your HTML

    registrationForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const sessionId = document.getElementById('session-id').value;
        const username = document.getElementById('username').value;

        // Register the user
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `session_id=${encodeURIComponent(sessionId)}&username=${encodeURIComponent(username)}`
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to register');
            return response.json();
        })
        .then(data => {
            // Fetch and display the bingo board after successful registration
            fetchBingoBoard(username);
        })
        .catch(error => {
            console.error('Registration failed:', error);
            alert('Failed to register. Please try again.');
        });
    });

    function fetchBingoBoard(username) {
        fetch('/generate_board', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}`
        })
        .then(response => response.json())
        .then(data => {
            displayBingoBoard(data.board);
        })
        .catch(error => {
            console.error('Failed to load bingo board:', error);
            alert('Failed to load bingo board. Please try again.');
        });
    }
    function displayBingoBoard(board) {
        let html = '<div class="board-grid">';
        board.forEach(row => {
            html += '<div class="board-row">';
            row.forEach(cell => {
                if (cell === 'mainsquare') {
                    // Ensure you're using backticks here
                    html += `<div class="cell"><img src="/static/images/mainsquare.png" alt="Main Square"></div>`;
                } else {
                    // Ensure you're using backticks here and correctly reference your images directory and file extension if necessary
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
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.addEventListener('click', function() {
                this.classList.toggle('stamped');
            });
        });
    }
});
