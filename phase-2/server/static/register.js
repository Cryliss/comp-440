"use strict";

window.onload=function() {
    document.getElementById("formCreateAccount").onsubmit=function(e) {
        e.preventDefault();

        // Incase we still have an error up let's remove it.
        document.querySelector('.msgCreateAccount').classList.remove('error');

        // Get our form values
        let usernameInput = document.getElementById('userName');
        let passwordInput = document.getElementById('password');
        let passwordConfirmedInput = document.getElementById('passwordConfirmed');
        let firstNameInput = document.getElementById('firstName');
        let lastNameInput = document.getElementById('lastName');
        let emailInput = document.getElementById('email');

        // Do we have any empty field?
        if(usernameInput.value === '' || passwordInput.value === ''|| passwordConfirmedInput.value === ''|| firstNameInput.value === ''|| lastNameInput.value === ''|| emailInput.value === '') {
            document.querySelector('.msgCreateAccount').classList.add('error'); //makes msg field red by calling 'error' class from CSS file
            document.querySelector('.msgCreateAccount').innerHTML = 'Please enter all fields'; //changes the empty msg to have a warning sign
        } else if (passwordInput.value != passwordConfirmedInput.value) {
            // Our password and confrim password values don't match - don't accept the input
            document.querySelector('.msgCreateAccount').classList.add('error');
            document.querySelector('.msgCreateAccount').innerHTML = 'Both passwords must match';
        } else if (!validateEmail(emailInput.value)) {
            // Our email address isn't in the correct format - don't accept the input
            document.querySelector('.msgCreateAccount').classList.add('error');
            document.querySelector('.msgCreateAccount').innerHTML = 'You must give an valid email address';
        } else if (passwordInput.value.length > 45) {
            // Our password is longer than what our database allows - don't accept the input
            document.querySelector('.msgCreateAccount').classList.add('error');
            document.querySelector('.msgCreateAccount').innerHTML = 'Password is too long';
        } else {
            // Our input has been validated, let's go ahead and create out data and request objects
            let data = {
                 username: usernameInput.value,
                 firstName: firstNameInput.value,
                 lastName: lastNameInput.value,
                 email: emailInput.value,
                 passConfirmed: true,
                 password: passwordInput.value
            }

            let req = {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }

            // Log our request message for later debbuging
            console.log(req)

            // Send a fetch request to our API to add our user
            fetch('http://127.0.0.1:5555/api/add', req).then(response => response.json())
                .then((body) => {
                    // Log the response body
                    console.log(body);
                    console.log(body.status);

                    // Did we successfully add the user?
                    if (body.status === 200) {
                        // Let's add a success message for the user and then wait 5s
                        document.querySelector('.msgCreateAccount').classList.add('success');
                        document.querySelector('.msgCreateAccount').innerHTML = "Account created!";
                        sleep(50000);

                        // Remove the message from the screen
                        document.querySelector('.msgCreateAccount').classList.remove('success')

                        // Reset our input variables
                        usernameInput.value = '';
                        passwordInput.value = '';
                        passwordConfirmedInput.value = '';
                        firstNameInput.value = '';
                        lastNameInput.value = '';
                        emailInput.value = '';

                        // Redirect the user to the login screen
                        window.location.replace("/login.html")
                    } else {
                        // User wasn't actually registered, let them know why
                        document.querySelector('.msgCreateAccount').classList.add('error')
                        document.querySelector('.msgCreateAccount').innerHTML = body.message
                    }
                }
            );
        }
    }
}

// Function to sleep so we can display success message before redirecting
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Function to check if the email address provided is in a valid format 
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
