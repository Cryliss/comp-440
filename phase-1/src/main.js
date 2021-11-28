//login
const formLogIn = document.querySelector('#formLogIn');
const userNameLogIn = document.querySelector('#userNameLogIn');
const passwordLogIn = document.querySelector('#passwordLogIn');

//createAccount
const formCreateAccount = document.querySelector('#formCreateAccount')
const usernameInput = document.querySelector('#userName');
const passwordInput = document.querySelector('#password');
const passwordConfirmedInput = document.querySelector('#passwordConfirmed');
const firstNameInput = document.querySelector('#firstName');
const lastNameInput = document.querySelector('#lastName');
const emailInput = document.querySelector('#email');

//createDatabase
const formCreateDatabase = document.querySelector('#formCreateDatabase');

const msgCreateAccount = document.querySelector('.msgCreateAccount'); //to prompt any error messages to createAccount form

//to make pages hidden
document.addEventListener("DOMContentLoaded", () => {

    document.querySelector("#linkCreateAccount").addEventListener("click", e => {
        e.preventDefault();
        formLogIn.classList.add("form--hidden");
        formCreateAccount.classList.remove("form--hidden");
    });

    document.querySelector("#linkLogin").addEventListener("click", e => {
        e.preventDefault();
        formLogIn.classList.remove("form--hidden");
        formCreateAccount.classList.add("form--hidden");
    });
});


//submit button pressed on registration page
formCreateAccount.addEventListener('submit', onSubmit); //listens for the submit button

function onSubmit(e) {
    e.preventDefault();
    if(usernameInput.value === '' || passwordInput.value === ''|| passwordConfirmedInput.value === ''|| firstNameInput.value === ''|| lastNameInput.value === ''|| emailInput.value === '') {
        msgCreateAccount.classList.add('error') //makes msg field red by calling 'error' class from CSS file
        msgCreateAccount.innerHTML = 'Please enter all fields' //changes the empty msg to have a warning sign

    // }
    // if(emailInput.value.includes('@') === false){
    //     msg.classList.add('error') //makes msg field red by calling 'error' class from CSS file
    //     msg.innerHTML = 'Please enter valid email address' //changes the empty msg to have a warning sign

    //     setTimeout(() => msg.remove(), 3000)
    } else if (passwordInput.value != passwordConfirmedInput.value) {
        // Our password and confrim password values don't match - don't accept the input
        msgCreateAccount.classList.add('error') //makes msg field red by calling 'error' class from CSS file
        msgCreateAccount.innerHTML = 'Both passwords must match' //changes the empty msg to have a warning sign
    } else {
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
        console.log(req)

        fetch('http://127.0.0.1:5555/api/add', req).then(response => response.json())
            .then((body) => {
                console.log(body);
                console.log(body.status);

                if (body.status === 200) {
                    usernameInput.value = '';
                    passwordInput.value = '';
                    passwordConfirmedInput.value = '';
                    firstNameInput.value = '';
                    lastNameInput.value = '';
                    emailInput.value = '';

                    formLogIn.classList.remove("form--hidden");
                    formCreateAccount.classList.add("form--hidden");
                } else {
                    // Change this console.log to an actual message the user can see
                    if (body.status === 409) {
                        // User wasn't actually registered, log the message
                        console.log(body.message)
                    } else if (body.status === 418) {
                        // Status code 418 == someone is trying to hack us.
                        console.log(body.message)
                    }
                }
            }
        );
    }
}

//when submit is pressed on the log in page
formLogIn.addEventListener('submit', onclick); //listens for the submit button

function onclick(e) {
    e.preventDefault();

    let data = {
        username: userNameLogIn.value,
        password: passwordLogIn.value
    }
    let req = {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }
    console.log(req)

    fetch('http://127.0.0.1:5555/api/login', req).then(response => response.json())
        .then((body) => {
            console.log(body);
            console.log(body.status);

            if (body.status === 200) {
                formLogIn.classList.add("form--hidden");
                formCreateDatabase.classList.remove("form--hidden");
            } else {
                // Change this console.log to an actual message the user can see
                if (body.message === "Username does not exist!" || body.message === "Invalid password given" ) {
                    console.log("Invalid username or password")
                } else if (body.status === 418) {
                    // Status code 418 == someone is trying to hack us.
                    console.log(body.message)
                }
            }
        }
    );
}

document.getElementById("createDatabaseButton").addEventListener("click", function(e) {
    e.preventDefault();

    fetch('http://127.0.0.1:5555/api/initializedb').then(response => response.json())
        .then((body) => {
            if (body.status != 200) {
                console.log(body.message)
            }
            // Change this console.log to an actual message the user can see
            console.log("SUCCESS: "+body.message);
        }
    );
});
