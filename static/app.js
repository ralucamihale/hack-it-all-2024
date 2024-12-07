document.addEventListener('DOMContentLoaded', function () {
    // Select the form
    const mentorForm = document.getElementById('mentorForm');

    // Add an event listener for form submission
    mentorForm.addEventListener('submit', function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Collect other form data (optional, based on server needs)
        const formData = new FormData(mentorForm);
        const data = {
            role: userRole,
            username: formData.get('username'),
            email: formData.get('email'),
            age: formData.get('age'),
            occupation: formData.get('occupation'),
            password: formData.get('password'),
            // Add more fields as needed
        };

        // Send the data to the server
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
