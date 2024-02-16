// Handles form submission to generate and display the bingo board
document.addEventListener('DOMContentLoaded', function() {
    const usernameForm = document.getElementById('username-form');
    const bingoBoard = document.getElementById('bingo-board');

    usernameForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const usernameInput = document.getElementById('username');
        const username = usernameInput.value.trim();
        if (username) {
            fetch('/generate_board', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(username)}`
            })
            .then(response => response.json())
            .then(data => {
                bingoBoard.innerHTML = generateBoardHTML(data.board);
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Please enter a username.');
        }
    });
});

// Generates HTML for the bingo board based on the data received from the server
function generateBoardHTML(board) {
    let html = '<div class="board-grid">';
    board.forEach(row => {
        html += '<div class="board-row">';
        row.forEach(cell => {
            if (cell === 'mainsquare') {
                // Special handling for 'mainsquare'
                html += `<div class="cell"><img src="/static/images/mainsquare.png" alt="Main Square" class="bingo-cell-image"></div>`;
            } else {
                // Adjust path as necessary
                html += `<div class="cell"><img src="/static/images/${cell}.png" alt="${cell}" class="bingo-cell-image"></div>`;
            }
        });
        html += '</div>'; // Close board-row
    });
    html += '</div>'; // Close board-grid
    return html;
}

// Handles the click event on images (assuming this is for marking bingo cells)
function handleImageClick(event) {
    const img = event.target;
    img.classList.toggle('stamped'); // Toggle the stamped class on the clicked image

    // Adjust the static file path as needed
    let stampElement = document.getElementById('stamp');
    if (!stampElement) {
        stampElement = document.createElement('img');
        stampElement.src = '/static/images/stamp.png'; // Ensure this path is correct
        stampElement.classList.add('stamp');
        stampElement.id = 'stamp';
        stampElement.alt = 'Stamp';
        document.body.appendChild(stampElement);
    }

    const imgRect = img.getBoundingClientRect();
    stampElement.style.top = `${imgRect.top + window.scrollY}px`;
    stampElement.style.left = `${imgRect.left + window.scrollX}px`;
    stampElement.style.display = stampElement.style.display === 'none' ? 'block' : 'none';
}

// Lazy loads images with the 'data-src' attribute
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.removeAttribute('data-src'); // Remove the attribute after loading the image
                observer.unobserve(img);
            }
        });
    }, {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    });

    images.forEach(image => {
        observer.observe(image);
    });
}

document.addEventListener('DOMContentLoaded', lazyLoadImages);
