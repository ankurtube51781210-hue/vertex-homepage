// 1. Smooth scroll reveal animation
function reveal() {
    var reveals = document.querySelectorAll(".reveal");

    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = reveals[i].getBoundingClientRect().top;
        var elementVisible = 50;

        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add("active");
        }
    }
}

window.addEventListener("scroll", reveal);

// 2. The Vault Transition Logic
document.addEventListener("DOMContentLoaded", () => {
    reveal();

    const vaultOverlay = document.getElementById('vault-overlay');
    const terminalText = document.getElementById('terminal-text');
    const articleCards = document.querySelectorAll('.article-card');
    const simulatedArticle = document.getElementById('article-view');
    const closeBtn = document.getElementById('close-article');

    // Text to type out
    const msg = "[ ENCRYPTED DATASTREAM SECURED... DECRYPTING ]";

    function typeWriter(text, i, cb) {
        if (i < text.length) {
            terminalText.innerHTML += text.charAt(i);
            setTimeout(() => typeWriter(text, i + 1, cb), 40); // typing speed
        } else {
            setTimeout(cb, 500); // wait before finishing
        }
    }

    articleCards.forEach(card => {
        card.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent instant navigation
            
            // 1. Close the Vault Doors
            vaultOverlay.classList.remove('hidden');
            setTimeout(() => {
                vaultOverlay.classList.add('active');
            }, 50);

            // 2. Wait for doors to close (600ms), then type terminal text
            setTimeout(() => {
                terminalText.innerHTML = "";
                typeWriter(msg, 0, () => {
                    // 3. Show the article behind the vault.
                    simulatedArticle.classList.remove('hidden');
                    
                    // 4. Open the Vault Doors
                    vaultOverlay.classList.remove('active');
                    
                    setTimeout(() => {
                        vaultOverlay.classList.add('hidden');
                        terminalText.innerHTML = "";
                    }, 600);
                });
            }, 600);
        });
    });

    closeBtn.addEventListener('click', () => {
        simulatedArticle.classList.add('hidden');
    });

    // 3. "Cyber-Decode" Text Scramble Logic
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':,./<>?";
    
    document.querySelectorAll('.scramble-text').forEach(element => {
        element.addEventListener('mouseover', event => {
            let iteration = 0;
            const originalText = event.target.dataset.value || event.target.innerText;
            
            // Store original text
            if(!event.target.dataset.value) {
                event.target.dataset.value = originalText;
            }
            
            clearInterval(event.target.scrambleInterval);
            
            event.target.scrambleInterval = setInterval(() => {
                event.target.innerText = originalText
                    .split("")
                    .map((letter, index) => {
                        if(index < iteration) {
                            return originalText[index];
                        }
                        // Keep spaces as spaces
                        if (originalText[index] === " ") return " ";
                        return letters[Math.floor(Math.random() * letters.length)];
                    })
                    .join("");
                
                if(iteration >= originalText.length){ 
                    clearInterval(event.target.scrambleInterval);
                }
                
                iteration += 1 / 3; // speed of decryption
            }, 30);
        });
    });
});
