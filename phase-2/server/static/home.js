"use strict";

// Function for creating a new blog post
function createBlogElement(blog) {
    // Get the blogs column
    let blogsCol = document.getElementById('blogs');

    // Create a new div and add the class "well" to it
    let div = document.createElement("DIV");
    div.classList.add('well');

    // Create a new node for the subject and add it to div
    let subjNode = document.createElement("H3");
    let subjText = document.createTextNode(blog["subject"]);
    subjNode.appendChild(subjText);
    div.appendChild(subjNode);

    // Create a new node for the poster information and add it to div
    let posterNode = document.createElement("P");

    // Grab the post date and split up at the spaces -
    // Current format: Sun, 15 Mar 2020 00:00:00 GMT
    // Desired format: Sun, 15 Mar 2020
    let pdate = blog["pdate"].split(" ");
    let post_date = pdate[0] + " " + pdate[1] + " " + pdate[2] + " " + pdate[3];

    // Create a string stating who posted the blog and when
    let poster = blog["created_by"] + " on " + post_date;

    // Create a new text node and add it to the poster node
    let posterText = document.createTextNode(poster);
    posterNode.appendChild(posterText);
    div.appendChild(posterNode);

    // Create a new paragraph element and add the description text to it
    let descNode = document.createElement("P");
    let descText = document.createTextNode(blog["description"]);
    descNode.appendChild(descText);
    div.appendChild(descNode);

    // Create a new node for the tags
    // Tags are already returned from the Python server in the correct format.
    let tagsNode = document.createElement("P");
    let tagsText = document.createTextNode(blog["tags"]);
    tagsNode.appendChild(tagsText);
    div.appendChild(tagsNode);

    // Add a paragraph element to create a gap between the post and its comments
    div.appendChild(document.createElement("P"));

    // Grab the blogs comments
    let comments = blog["comments"];
    // If we actually have some comments, let's make some elements for them.
    if (comments.length != 0) {
        for (let i = 0; i < comments.length; i++) {
            let commentsDiv = createCommentElement(comments[i]);
            div.appendChild(commentsDiv);
        }
    }

    // Next, let's add some elememts that allow the user to create a new comment.

    // Create a comment button and it to the div
    let commentButton = document.createElement("BUTTON");
    let commentText = document.createTextNode("Comment ");
    commentButton.appendChild(commentText);
    div.appendChild(commentButton);

    // TODO: CREATE SOME FIELDS FOR THE USERS COMMENT
    // NEED: DROPDOWN LIST FOR SENTIMENT, TEXTBOX FOR DESCRIPTION

    blogsCol.appendChild(div);
}

// Function for creating a new comment element on a blog
function createCommentElement(c) {
    // Create a new holding div for the comments
    let commentsDiv = document.createElement("DIV");
    commentsDiv.classList.add("well");

    // Grab the comment date and split up at the spaces -
    // Current format: Sun, 15 Mar 2020 00:00:00 GMT
    // Desired format: Sun, 15 Mar 2020
    let cdate = String(c.cdate).split(" ");
    let comment_date = cdate[0] + " " + cdate[1] + " " + cdate[2] + " " + cdate[3];
    let commenter = c.posted_by + " on " + comment_date;
    let commenterText = document.createTextNode(commenter);

    // Create a H4 element for the commenter information
    let commenterDiv = document.createElement("H4");
    commenterDiv.appendChild(commenterText);
    commentsDiv.appendChild(commenterDiv);

    // Create a new paragraph element for the sentiment
    let sentimentNode = document.createElement("P");
    let sentimentText = "Sentiment: "+c.sentiment;
    sentimentNode.appendChild(document.createTextNode(sentimentText));
    commentsDiv.appendChild(sentimentNode);

    // Create a new paragraph element for the description
    let descNode = document.createElement("P");
    descNode.appendChild(document.createTextNode(c.description));
    commentsDiv.appendChild(descNode);

    return commentsDiv;
}

// Adds the blogs to the page
function addBlogs() {
    // Send a fetch request to our api to get all the blogs from the database
    fetch('http://127.0.0.1:5555/api/blogs').then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);


            // Yep, let's go ahead and display those blogs
            for (let i = 0; i < body.length; i++) {
                createBlogElement(body[i])
            }

        }
    );
}

// Adds the users details to the page, like followers, following and hobbies
function addUserDetails() {
    // Send a fetch request to our api to get all the userdata from the database
    fetch('http://127.0.0.1:5555/api/userdata').then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            let followers = body['followers'];
            let following = body['following'];
            let hobbies = body['hobbies'];

            let followerList = document.getElementById("followers");
            for (let i = 0; i < followers.length; i++) {
                let newItem = document.createElement("LI");
                let itemText = document.createTextNode(followers[i]);
                newItem.appendChild(itemText);
                followerList.appendChild(newItem);
            }

            let followingList = document.getElementById("following");
            for (let i = 0; i < following.length; i++) {
                let newItem = document.createElement("LI");
                let itemText = document.createTextNode(following[i]);
                newItem.appendChild(itemText);
                followingList.appendChild(newItem);
            }

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

window.onload=function() {
    addBlogs();
    addUserDetails();

    // Event listener for creaing a new post
    document.getElementById("createPostButton").addEventListener("click", function(e) {
        e.preventDefault();

        // Get the post fields
        let subject = document.getElementById('#subjectField').innerHTML;
        let description = document.getElementById('#descField').innerHTML;
        let tags = document.getElementById('#tagsField').innerHTML;

        // Check some constraints
        if (subject == '' || description == '' ||  tags == '') {
            document.querySelector('.msg').classList.add('error');
            document.querySelector('.msg').innerHTML = 'Please fill out all fields';
        } else if (subject.length > 50) {
            document.querySelector('.msg').classList.add('error');
            document.querySelector('.msg').innerHTML = 'Subject is too long';
        } else if (description.length > 250) {
            document.querySelector('.msg').classList.add('error');
            document.querySelector('.msg').innerHTML = 'Blog post is too long, maximum 250 characters';
        } else {
            // Check the tags length and make sure they match what the database allows
            let tArr = tags.split(",");
            for (var i = 0; i < tArr.length; i++) {
                if (tArr[i].length > 20) {
                    document.querySelector('.msg').classList.add('error');
                    document.querySelector('.msg').innerHTML = 'All tags must be less than or equal to 20 characters. Please fix tag ' + tArr[i];
                    return
                }
            }

            // Create a new data object
            let data = {
                subject: subject,
                description: description,
                tags: tags
            }

            // Create a new request object and add our data to it
            let req = {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }

            // Print out our request message to the console for debbuging
            console.log(req)

            // Send a fetch request to our api to initialize the database
            fetch('http://127.0.0.1:5555/api/newpost', req).then(response => response.json())
                .then((body) => {
                    // Log the request body
                    console.log(body);

                    // Did we successfully initialize the database?
                    if (body.status != 200) {
                        // No, create an error message an let the user know why
                        document.querySelector('.msg').classList.add('error');
                        document.querySelector('.msg').innerHTML = body.message;
                        return
                    }
                    // Yep, let's create a success message for the user.
                    document.querySelector('.msg').classList.add('success');
                    let message = body.dbmessage + " Blog ID# " + body.blogid;
                    document.querySelector('.msg').innerHTML = message;


                    addNewBlog(body.blogid);
                }
            );
        }

    });
}
