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

let usernameInputTemp = '';
let passwordInputTemp = '';
let passwordConfirmedInputTemp = '';
let firstNameInputTemp = '';
let lastNameInputTemp = '';
let emailInputTemp = '';

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
    } else {
        usernameInputTemp = usernameInput.value;
        passwordInputTemp = passwordInput.value;
        passwordConfirmedInputTemp = passwordConfirmedInput.value;
        firstNameInputTemp = firstNameInput.value;
        lastNameInputTemp = lastNameInput.value;
        emailInputTemp = emailInput.value;
        usernameInput.value = '';
        passwordInput.value = '';
        passwordConfirmedInput.value = '';
        firstNameInput.value = '';
        lastNameInput.value = '';
        emailInput.value = '';
        formLogIn.classList.remove("form--hidden");
        formCreateAccount.classList.add("form--hidden");

        // data = {
        //     username: usernameInputTemp,
        //     firstName: firstNameInputTemp,
        //     lastName: lastNameInputTemp,
        //     email: emailInputTemp,
        //     passConfirmed: true,
        //     password: passwordInputTemp
        //   }
        //   response = postData('http:127.0.0.1:5555/api/add', data);

    }

}


//when submit is pressed on the log in page
formLogIn.addEventListener('submit', onclick); //listens for the submit button

function onclick(e) {
    e.preventDefault();

    //add if statement to see if username and password exist
    data = {
        username: userNameLogIn.value,
        password: passwordLogIn.value
    }
    req = {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }
    //   response = postData('http://127.0.0.1:5555/api/login', data);
    console.log(req)

    fetch('http://127.0.0.1:5555/api/login', req).then(response => response.json())
        .then((body) => {
            console.log(body);
            console.log(body.status);

            if (body.status === 200) {
                formLogIn.classList.add("form--hidden");
                formCreateDatabase.classList.remove("form--hidden");
            }
    });


}

//when the create database button is clicked on create data base page
// formCreateDatabase.addEventListener('button', databaseFunc); //listens for the submit button

// function databaseFunc(e) {
//     e.preventDefault();
//     console.log("database created");
// }

document.getElementById("createDatabaseButton").addEventListener("click", function(e) {
    e.preventDefault();

    fetch('http://127.0.0.1:5555/api/initializedb').then(response => response.text())
        .then((body) => {
            console.log(body);
    });
});
