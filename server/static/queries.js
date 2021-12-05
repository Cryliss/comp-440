"use strict";
// Adds the users details to the page, like followers, following and hobbies
function addUserDetails() {
    // Send a fetch request to our api to get all the userdata from the database
    fetch('http://127.0.0.1:5555/api/userdata').then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            // Grab our variables from the body
            let followers = body['followers'];
            let following = body['following'];
            let hobbies = body['hobbies'];

            // Create a new list item for each follower and add it to the
            // followerList list element
            let followerList = document.getElementById("followers");
            for (let i = 0; i < followers.length; i++) {
                let newItem = document.createElement("LI");
                let itemText = document.createTextNode(followers[i]);
                newItem.appendChild(itemText);
                followerList.appendChild(newItem);
            }

            // Create a new list item for each following and add it to the
            // followingList list element
            let followingList = document.getElementById("following");
            for (let i = 0; i < following.length; i++) {
                let newItem = document.createElement("LI");
                let itemText = document.createTextNode(following[i]);
                newItem.appendChild(itemText);
                followingList.appendChild(newItem);
            }

            // Create a new list item for each hobby and add it to the
            // hobbiesList list element
            let hobbiesList = document.getElementById("hobbies");
            for (let i = 0; i < hobbies.length; i++) {
                let newItem = document.createElement("LI");
                let itemText = document.createTextNode(hobbies[i]);
                newItem.appendChild(itemText);
                hobbiesList.appendChild(newItem);
            }
        }
    );
}

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
                console.log(body.message);
                return
            }
            // Do something with the blogs ..
            console.log(body.blogs);
            let queryOneResults = body.blogs;
            buildTable(queryOneResults)
        }
    );
}

function buildTable(data){
    let table = document.getElementById('queryOneTable');
    table.classList.remove('table--hidden');

    // We make a new table body so that we dont just append the results
    // to the table when we rerun the query.
    let newtb = document.createElement("TBODY");
    for (var i = 0; i < data.length; i++){
        // Create a new row element and add the columns to it
        let rowElement = document.createElement("TR");

        // Create column elements for each column and add their text nodes to it
        let idCol = document.createElement("TD")
        let idTextNode = document.createTextNode(data[i].blogid);
        idCol.appendChild(idTextNode);
        rowElement.appendChild(idCol);

        let createdCol = document.createElement("TD")
        let createdTextNode = document.createTextNode(data[i].created_by);
        createdCol.appendChild(createdTextNode);
        rowElement.appendChild(createdCol);

        let subjCol = document.createElement("TD")
        let subjTextNode = document.createTextNode(data[i].subject);
        subjCol.appendChild(subjTextNode);
        rowElement.appendChild(subjCol);

        // Grab the post date and split up at the spaces -
        // Current format: Sun, 15 Mar 2020 00:00:00 GMT
        // Desired format: Sun, 15 Mar 2020
        let pdate = data[i].pdate.split(" ");
        let post_date = pdate[0] + " " + pdate[1] + " " + pdate[2] + " " + pdate[3];

        let descCol = document.createElement("TD")
        let descTextNode = document.createTextNode(post_date);
        descCol.appendChild(descTextNode);
        rowElement.appendChild(descCol);

        let dateCol = document.createElement("TD")
        let dateTextNode = document.createTextNode(data[i].description);
        dateCol.appendChild(dateTextNode);
        rowElement.appendChild(dateCol);

        // Add the row to the table body
        newtb.appendChild(rowElement);
    }
    table.appendChild(newtb)
    if (table.childNodes.length > 3) {
        table.removeChild(table.childNodes[2])
    }
}

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
            console.log(body.users);
            let queryTwoResultsDiv = document.querySelector('#queryTwoResults');
            queryTwoResultsDiv.classList.remove("list--hidden");

            if (queryTwoResultsDiv.childNodes.length > 0) {
                for (let i=0; i < queryTwoResultsDiv.childNodes.length; i++)  {
                    queryTwoResultsDiv.removeChild(queryTwoResultsDiv.childNodes[i])
                }
            }

            let queryTwoResults = body.users;

            let queryTwoResultsList = document.createElement("UL");
            for (let i=0; i<queryTwoResults.length; i++){
                const li = document.createElement('LI');
                li.appendChild(document.createTextNode(queryTwoResults[i]));
                queryTwoResultsList.appendChild(li);
            }
            queryTwoResultsDiv.appendChild(queryTwoResultsList);
        }
    );
}

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
            console.log(body.users);
            let queryThreeResultsDiv = document.querySelector('#queryThreeResults')
            queryThreeResultsDiv.classList.remove("list--hidden");

            if (queryThreeResultsDiv.childNodes.length > 0) {
                for (let i=0; i < queryThreeResultsDiv.childNodes.length; i++)  {
                    queryThreeResultsDiv.removeChild(queryThreeResultsDiv.childNodes[i])
                }
            }

            let queryThreeResults = body.users;

            let queryThreeResultsList = document.createElement("UL");
            for (let i=0; i<queryThreeResults.length; i++){
                const li = document.createElement('li');
                li.appendChild(document.createTextNode(queryThreeResults[i]))
                queryThreeResultsList.appendChild(li);
            }
            queryThreeResultsDiv.appendChild(queryThreeResultsList);
        }
    );
}

window.onload=function() {
    addUserDetails();

    document.getElementById("query1").onsubmit=function(e){
        e.preventDefault();
        let user = document.querySelector('#query1User').value;
        console.log(user);
        query1(user);
    }

    document.getElementById("query2").onsubmit=function(e){
        e.preventDefault();
        console.log(document.querySelector('#query2Date'));
        let pdate = document.querySelector('#query2Date').value;
        console.log(pdate);
        query2(pdate);
    }

    document.getElementById("query3").onsubmit=function(e){
        e.preventDefault();
        let userx = document.querySelector('#query3User1').value;
        console.log(userx);
        let usery = document.querySelector('#query3User2').value;
        console.log(usery);
        query3(userx, usery);
    }


    document.getElementById("runQueryFourButton").addEventListener("click", function(e) {
        e.preventDefault();
        let queryFourResultsDiv = document.querySelector('#queryFourResults')
        queryFourResultsDiv.classList.remove("list--hidden");

        console.log(queryFourResultsDiv.childNodes)
        if (queryFourResultsDiv.childNodes.length > 0) {
            for (let i=0; i <= queryFourResultsDiv.childNodes.length; i++)  {
                queryFourResultsDiv.removeChild(queryFourResultsDiv.childNodes[i])
            }
        }
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
                console.log(body.users);
                let queryFourResults = body.users;

                let queryFourResultsList = document.createElement("UL");
                for (let i=0; i<queryFourResults.length; i++){
                    const li = document.createElement('LI');
                    li.appendChild(document.createTextNode(queryFourResults[i]))
                    queryFourResultsList.appendChild(li);
                }
                queryFourResultsDiv.appendChild(queryFourResultsList)
            }
        );
    });


    document.getElementById("runQueryFiveButton").addEventListener("click", function(e) {
        e.preventDefault();
        let queryFiveResultsDiv = document.querySelector('#queryFiveResults')
        queryFiveResultsDiv.classList.remove("list--hidden");

        if (queryFiveResultsDiv.childNodes.length > 0) {
            for (let i=0; i < queryFiveResultsDiv.childNodes.length; i++)  {
                queryFiveResultsDiv.removeChild(queryFiveResultsDiv.childNodes[i])
            }
        }

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
                console.log(body.users);
                let queryFiveResults = body.users;

                let queryFiveResultsList = document.createElement("UL");
                for (let i=0; i<queryFiveResults.length; i++){
                    const li = document.createElement('li');
                    li.appendChild(document.createTextNode(queryFiveResults[i]))
                    queryFiveResultsList.appendChild(li);
                }
                queryFiveResultsDiv.appendChild(queryFiveResultsList)
            }
        );
    });

    document.getElementById("runQuerySixButton").addEventListener("click", function(e) {
        e.preventDefault();
        let querySixResultsDiv = document.querySelector('#querySixResults')
        querySixResultsDiv.classList.remove("list--hidden");

        if (querySixResultsDiv.childNodes.length > 0) {
            for (let i=0; i < querySixResultsDiv.childNodes.length; i++)  {
                querySixResultsDiv.removeChild(querySixResultsDiv.childNodes[i])
            }
        }

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
                console.log(body.users);
                let querySixResults = body.users;

                let querySixResultsList = document.createElement("UL");
                for (let i=0; i<querySixResults.length; i++){
                    const li = document.createElement('li');
                    li.appendChild(document.createTextNode(querySixResults[i]))
                    querySixResultsList.appendChild(li);
                }
                querySixResultsDiv.appendChild(querySixResultsList);
            }
        );
    });

}
