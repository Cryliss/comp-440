"use strict";
window.onload=function() {
    document.getElementById("createDatabaseButton").addEventListener("click", function(e) {
        e.preventDefault();

        // Send a fetch request to our api to initialize the database
        fetch('http://127.0.0.1:5555/api/initializedb').then(response => response.json())
            .then((body) => {
                // Log the request body
                console.log(body);

                // Did we successfully initialize the database?
                if (body.status != 200) {
                    // No, create an error message an let the user know why
                    document.querySelector('.msg').classList.add('error');
                    document.querySelector('.msg').innerHTML = body.message;
                }
                // Yep, let's create a success message for the user.
                document.querySelector('.msg').classList.add('success');
                document.querySelector('.msg').innerHTML = body.message;
            }
        );
    });
}
