document.addEventListener('DOMContentLoaded', function () {
    // Select the form
    const mentorForm = document.getElementById('mentorForm');

    // Add an event listener for form submission
    mentorForm.addEventListener('submit', function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Define the user role

        // Collect other form data (optional, based on server needs)
        const formData = new FormData(mentorForm);
        const data = {
            role: "mentor",
            username: formData.get('username'),
            email: formData.get('email'),
            age: formData.get('age'),
            occupation: formData.get('occupation'),
            nationality: formData.get('nationality'),
            county: formData.get('county'),
            interests: formData.get('interests'),
            password: formData.get('password'),
        };

        localStorage.setItem('userProfile', JSON.stringify(data));

        let allUsers = JSON.parse(localStorage.getItem('allUsers')) || [];

        allUsers.push(data);

        localStorage.setItem('allUsers', JSON.stringify(allUsers));


        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.text())
        .then(data => {
            // Replace the page content with the server's response
            document.body.innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const userForm = document.getElementById('userForm');

    userForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(userForm);
        const data = {
            role: "user",
            username: formData.get('username'),
            email: formData.get('email'),
            age: formData.get('age'),
            occupation: formData.get('occupation'),
            nationality: formData.get('nationality'),
            county: formData.get('county'),
            interests: formData.get('interests'),
            password: formData.get('password'),
        };

        localStorage.setItem('userProfile', JSON.stringify(data));

        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.text())
        .then(data => {
            document.body.innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});