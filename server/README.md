# server

## API Calls
Current functioning API calls are as follows:

`http://127.0.0.1:8080/initializedb`

Initializes the database User table.  
Response should be: `Database successfully initialized!`

`http://127.0.0.1:8080/add`

This is a POST request - need to test it using https://reqbin.com/.  
Request data should include  
```json
{
  "username": "comp440_test",
  "firstName": "Test",
  "lastName": "User",
  "email": "test.user.1@my.csun.edu",
  "passConfirmed": true
}
```

Response data should be  
```json
{
    "message": "User added successfully!",
    "status": 200
}
```

`http://127.0.0.1:8080/users`  

Response data should be  
```json
[
  {
    "email": "faizan.hussain.???@my.csun.edu",
    "firstName": "Faizan",
    "lastName": "Hussain",
    "username": "comp440_faizan"
  },
  {
    "email": "sabra.bilodeau.352@my.csun.edu",
    "firstName": "Sabra",
    "lastName": "Bilodeau",
    "username": "comp440_sabra"
  },
  {
    "email": "shawn.morrison.???@my.csun.edu",
    "firstName": "Shawn",
    "lastName": "Morrison",
    "username": "comp440_shawn"
  },
  {
    "email": "test.user.1@my.csun.edu",
    "firstName": "Test",
    "lastName": "User",
    "username": "comp440_test"
  }
]
```

`http://127.0.0.1:8080/user/comp440_test`  

Response data should be  
```json

{
  "email": "test.user.1@my.csun.edu",
  "firstName": "Test",
  "lastName": "User",
  "username": "comp440_test"
}
```

`http://127.0.0.1:8080/delete/comp440_test`

Delete the test user you just created

Response data should be   
```json
{
  "message": "Usercomp440_testdeleted successfully!",
  "status": 200
}
```
