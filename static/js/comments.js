// comments.js - SQUAD COMM-LINK LOGIC

document.addEventListener('DOMContentLoaded', () => {
    // Buttons aur inputs ko dhoondho
    const sendBtn = document.getElementById('sendCommentBtn');
    const chatContainer = document.querySelector('.chat-container');

    // Agar hum strategy wale page par hain tabhi ye code chalega
    if (sendBtn && chatContainer) {
        sendBtn.addEventListener('click', () => {
            const nameInput = document.getElementById('playerName');
            const msgInput = document.getElementById('playerMessage');

            const name = nameInput.value.trim();
            const msg = msgInput.value.trim();

            // Check karo ki inputs khali toh nahi hain
            if (name !== '' && msg !== '') {
                
                // Aaj ka time nikalo (e.g. 10:45 AM)
                const now = new Date();
                let timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                // Naya comment box design karo HTML mein
                const newComment = document.createElement('div');
                newComment.className = 'comment-box glass-panel';
                newComment.style.borderLeft = '4px solid #00ff00'; // Naye comments green dikhenge
                
                newComment.innerHTML = `
                    <strong style="color: #00ff00;">${name}</strong> 
                    <span style="color: #555; font-size: 12px; margin-left: 10px;">Today at ${timeString}</span>
                    <p style="color: #ccc; margin-top: 8px;">${msg}</p>
                `;

                // Naye comment ko chat list mein sabse upar (top par) add kar do
                chatContainer.insertBefore(newComment, chatContainer.firstChild);

                // Type karne ke baad box wapas khali kar do
                msgInput.value = '';
            } else {
                alert("⚠️ Intel Alert: Name aur Message dono field bharna zaroori hai!");
            }
        });
    }
});