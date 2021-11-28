# TODO
- [ ] Create a UI for the user to perform the 6 queries below.  
- [x] Create API routes to perform the queries.

Example fetch requests and sample responses are given.

# Query 1
List all the blogs of user X, such that all the comments are positive for these blogs

*Sample Request*  
```js
// Either retrieve a value from user input, OR leave the hardcoded value, "batman" here
query1("batman");

function query1(created_by) {
    let data = {
        created_by: created_by
    }

    let req = {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }

    fetch('http://127.0.0.1:5555/api/query1', req).then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            // Did we get a message back?
            if (body.status != 200) {
                // No, create an error message an let the user know why
                console.log(body.message)
                return
            }
            // Do something with the blogs ..
            console.log(body.blogs);
        }
    );
}
```

*Sample Response Body*  
```json
{
    "blogs": [{
        "blogid": 4,
        "created_by": "batman",
        "description": "To all you lowly criminals out there, this is a warning to know I am watching. I am justice. I am righteousness. I am the NIGHT.",
        "pdate": "Tue, 24 Mar 2020 00:00:00 GMT",
        "subject": "I am the night."
    }],
    "status": 200
}
```

*Sample accessing response body*
```js
let created_by = blogs["created_by"];
```

# Query 2
List all the users who posted the most number of blogs on 10/10/2021; if there is a tie, list all those have a tie.

*Sample Request*  
```js
query2("2020-03-24");

function query2(pdate) {
    let data = {
        pdate: pdate
    }

    let req = {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }

    fetch('http://127.0.0.1:5555/api/query2', req).then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            // Did we get a message back?
            if (body.status != 200) {
                // No, create an error message an let the user know why
                console.log(body.message)
                return
            }
            // Do something with the users ..
            console.log(body.user);
        }
    );
}
```

*Sample Response Body*  
```json
{
    "status": 200,
    "users": [
        "batman"
    ]
}
```


# Query 3
List users who are followed by both X and Y, where X & Y are usernames provided by the user

*Sample Request*  
```js
query3("catlover", "scooby");

function query3(x,y) {
    let data = {
        userx: x,
        usery: y
    }

    let req = {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }

    fetch('http://127.0.0.1:5555/api/query3', req).then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            // Did we get a message back?
            if (body.status != 200) {
                // No, create an error message an let the user know why
                console.log(body.message)
                return
            }
            // Do something with the users ..
            console.log(body.user);
        }
    );
}
```

*Sample Response Body*  
```json
{
    "status": 200,
    "users": [
        "batman",
        "doglover",
        "pacman"
    ]
}
```

# Query 4
Display all users who have never posted a blog

*Sample Request*  
```js
function query4() {
    fetch('http://127.0.0.1:5555/api/query4').then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            // Did we get a message back?
            if (body.status != 200) {
                // No, create an error message an let the user know why
                console.log(body.message)
                return
            }
            // Do something with the users ..
            console.log(body.user);
        }
    );
}
```

*Sample Response Body*  
```json
{
  "status": 200,
  "users": [
    "bob",
    "faizan",
    "matty",
    "sabra",
    "chryliss",
    "shawn"
  ]
}
```

# Query 5
Display all user who have only posted negative comments

*Sample Request*  
```js
function query5() {
    fetch('http://127.0.0.1:5555/api/query5').then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            // Did we get a message back?
            if (body.status != 200) {
                // No, create an error message an let the user know why
                console.log(body.message)
                return
            }
            // Do something with the users ..
            console.log(body.user);
        }
    );
}
```

*Sample Response Body*  
```json
{
  "status": 200,
  "users": [
    "catlover",
    "batman"
  ]
}
```

# Query 6
Display all users who have never received a negative comment

*Sample Request*  
```js
function query6() {
    fetch('http://127.0.0.1:5555/api/query6').then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            // Did we get a message back?
            if (body.status != 200) {
                // No, create an error message an let the user know why
                console.log(body.message)
                return
            }
            // Do something with the users ..
            console.log(body.user);
        }
    );
}
```

*Sample Response Body*  
```json
{
  "status": 200,
  "users": [
    "batman",
    "jsmith",
    "notbob",
    "pacman",
    "scooby"
  ]
}
```
