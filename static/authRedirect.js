// authRedirect.js
document.addEventListener('DOMContentLoaded', (event) => {
    if (window.location.pathname !== '/login' && !isAuthenticated()) {
        window.location.href = '/login'; // Redirect if not authenticated and not on login page
    } else {
        let userEmail = getEmailFromCookie();
        if (userEmail && document.getElementById('userEmail')) {
            document.getElementById('userEmail').textContent = userEmail;
        }
    }
});

function isAuthenticated() {
    const token = localStorage.getItem('access_token');
    return token != null;
}

function getEmailFromCookie() {
    let cookies = document.cookie.split(';');
    let emailCookie = cookies.find(cookie => cookie.trim().startsWith('user_email='));
    if (emailCookie) {
        return emailCookie.split('=')[1];
    }
    return null;
}


