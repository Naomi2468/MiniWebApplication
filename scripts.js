// Show loading prompt when clicking button
const form = document.querySelector("form");
if (form) {
    form.addEventListener("submit", () => {
        const btn = form.querySelector("button[type='submit']");
        if (btn) {
            btn.innerHTML = "🌕 Analyzing...";
            btn.disabled = true;
        }
    });
}

// box glows when button is clicked
const textarea = document.querySelector("textarea");
if (textarea) {
    textarea.addEventListener("focus", () => {
        textarea.style.boxShadow = "0 0 20px rgba(250, 204, 21, 0.6)";
    });
    textarea.addEventListener("blur", () => {
        textarea.style.boxShadow = "none";
    });
}
