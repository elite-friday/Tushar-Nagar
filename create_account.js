document.querySelector('.register-form').addEventListener('submit', function(e) {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    
    if (username.length < 3) {
        alert("Username must be at least 3 characters long!");
        e.preventDefault();
    }
    
    console.log("Registering player: " + username);
});

// js for google auth can be added later
document.getElementById('googleLoginBtn').addEventListener('click', function() {
    // 1. Popup ki width aur height set karein
    const width = 500;
    const height = 600;
    
    // 2. Screen ke center mein popup ko position karein
    const left = (window.innerWidth / 2) - (width / 2);
    const top = (window.innerHeight / 2) - (height / 2);

    // 3. Google OAuth URL (Abhi ke liye placeholder hai)
    // Real app mein yahan aapka Google Client ID wala URL aayega
    const url = "https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URL&response_type=token&scope=email%20profile";

    // 4. Window open command
    window.open(
        url, 
        "GoogleLogin", 
        `width=${width},height=${height},top=${top},left=${left},resizable=yes,scrollbars=yes`
    );
});