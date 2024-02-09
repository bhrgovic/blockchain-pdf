// auth.js


// Function to logout the user
function logout() {
    document.cookie = 'access_token=; Max-Age=0; path=/';
    document.cookie = 'user_email=; Max-Age=0; path=/';
    window.location.href = '/login';
}

// Function to check if the user is authenticated


document.addEventListener('DOMContentLoaded', function() {
    var loginForm = document.getElementById('loginForm');
    if(loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the default form submission

            var email = document.getElementsByName('email')[0].value;
            var password = document.getElementsByName('password')[0].value;

            login(email, password);
        });
    }
});

// Function to perform login
function login(email, password) {
    fetch('/login', {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login request failed with status: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
            document.cookie = 'user_email=' + email + '; path=/';
            window.location.href = '/admin_home';
        } else {
            alert('Login failed: ' + (data.message || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Login failed. Error: ' + error.message);
    });
}


// Function to fetch protected data
function fetchSomeData(endpoint) {
    fetch(endpoint, {
        method: 'GET',
        headers: getHeaders()
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Protected data:', data);
        // You can process the data here as needed
    })
    .catch(error => {
        console.error('Error fetching protected data:', error);
    });
}



function getHeaders() {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = 'Bearer ' + token;
    }

    return headers;
}
