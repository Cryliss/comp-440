"use strict";

window.onload=function() {
    document.getElementById("formLogIn").onsubmit=function(e) {
        e.preventDefault();
        // Incase we still have an error up let's remove it.
        document.querySelector('.msg').classList.remove('error');

        // Get our form values
        let usernameInput = document.querySelector('#userNameLogIn').value;
        let passwordInput = document.querySelector('#passwordLogIn').value;

        // Are any of our fields empty?
        if (usernameInput === '' || passwordInput === '') {
            // Yep, let's the user know and don't accept the input
            document.querySelector('.msg').classList.add('error') //makes msg field red by calling 'error' class from CSS file
            document.querySelector('.msg').innerHTML = 'Please enter all fields'
        } else {
            // Our input was okay, let's create our data and request objects
            let data = {
                username: usernameInput,
                password: passwordInput
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

            // Send a fetch request to our API to login our user
            fetch('http://127.0.0.1:5555/api/login', req).then(response => response.json())
                .then((body) => {
                    // Log the response body
                    console.log(body);
                    console.log(body.status);

                    // Did we successfully login the user?
                    if (body.status === 200) {
                        // Yep, let's redirect to the home page
                        window.location.replace("/start.html")
                    } else {
                        // User wasn't actually logged in, let them know why
                        if (body.message === "Username does not exist!" || body.message === "Invalid password given" ) {
                            document.querySelector('.msg').classList.add('error')
                            document.querySelector('.msg').innerHTML = "Invalid username or password";
                        } else {
                            document.querySelector('.msg').classList.add('error')
                            document.querySelector('.msg').innerHTML = body.message;
                        }
                    }
                }
            );
            return false;
        }
    }
}
