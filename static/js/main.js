// main.js - TEAM STAR HQ INTERACTIVITY

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Hacker-Style Console Message
    console.log("%c⚠️ COMMAND CENTER INITIALIZED ⚠️", "color: #00f3ff; font-size: 20px; font-weight: bold; text-shadow: 0 0 10px #00f3ff;");
    console.log("%cWelcome to Team Star Official Database. Access strictly monitored.", "color: #00ff00; font-size: 14px;");

    // 2. Auto-hide Flash Messages (Alerts)
    // Ye code un saare error/success boxes ko dhoondhega jo humne flash() se banaye hain
    const flashMessages = document.querySelectorAll('div[style*="border-radius: 5px; margin-bottom: 20px;"]'); 
    
    flashMessages.forEach(msg => {
        // 4000 milliseconds (4 seconds) ke baad message fade out hona shuru hoga
        setTimeout(() => {
            msg.style.transition = "opacity 0.5s ease";
            msg.style.opacity = "0";
            
            // Fade out hone ke 0.5s baad use screen se puri tarah hata do
            setTimeout(() => {
                msg.remove();
            }, 500);
        }, 4000);
    });

});