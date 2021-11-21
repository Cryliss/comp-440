"use strict";

/*  HOME PAGE
*
*   Functions for dynamically creating blog elements on the home page
*
*   Calls the server to get the user and blog data, then creates new elements
*   using document.createElement(), passing the name of the element we want
*   to create in all caps.
*
*   Adds any attributes we need to the newly created element, and then creates
*   any child elements (nodes) we may need and appends them to the main element. s
*/

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

                    //addNewBlog(body.blogid);
                }
            );
        }
    });
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

/*  Function for creating a new blog post
*
*   Generated HTML:
*   NOTE: {name} means a value that we retrieve from the return blog data
*
*   <div class="well" id={blogid}>
*     <H3>{subject}</H3>
*     <p>{created_by} on {pdate}</p>
*     <p>{Description}</p>
*     <p>{tags}</p>
*     <p></p>
*     {for each comment ..}
*     <div class="well">
*       <H4>{commenter_name} on {comment_date}</H4>
*       <p>{description}</p>
*     </div>
*     {end for loop}
*
*     <form id={blogid}>
*       <div class="form-group">
*         <label for="sentimentSelect">Sentiment</label>
*         <select>
*           <option>positive</option>
*           <option>negative</option>
*         </select>
*       </div>
*       <div class="form-group">
*         <label for="cDescField">Sentiment</label>
*         <textarea class="form-control" type="text"></textarea>
*       </div>
*       <button class="btn" type="submit">Comment</button>
*     </form>
*   </div>
*/
function createBlogElement(blog) {
    // Get the blogs column we created in the HTML file
    let blogsCol = document.getElementById("blogs");

    let div = document.createElement("DIV");    // Create a new div element
    div.setAttribute("class", "well");          // Add the class well to it
    div.setAttribute("id", blog["blogid"]);     // Make its ID the same as the blogs

    // Create a new text node for the subject
    let subjText = document.createTextNode(blog["subject"]);
    let subjNode = document.createElement("H3"); // Create a new H3 element
    subjNode.appendChild(subjText);              // Add the text node to it
    div.appendChild(subjNode);                   // Add the subject to the main div

    // Grab the post date and split up at the spaces -
    // Current format: Sun, 15 Mar 2020 00:00:00 GMT
    // Desired format: Sun, 15 Mar 2020
    let pdate = blog["pdate"].split(" ");
    let post_date = pdate[0] + " " + pdate[1] + " " + pdate[2] + " " + pdate[3];

    // Create a string stating who posted the blog and when
    let poster = blog["created_by"] + " on " + post_date;

    // Create a new text node using the poster string we just declared
    let posterText = document.createTextNode(poster);

    // Create a new paragraph element for the poster information
    let posterNode = document.createElement("P");
    posterNode.appendChild(posterText);         // Add the text node to it
    div.appendChild(posterNode);                // Add the poster info to the div

    // Create a new text node for the description
    let descText = document.createTextNode(blog["description"]);
    let descNode = document.createElement("P"); // Create a new P element for it
    descNode.appendChild(descText);             // Add the text node to the p
    div.appendChild(descNode);                  // Add description to the main div

    // Create a new text node for the tags
    // Tags are already returned from the Python server in the correct format.
    let tagsText = document.createTextNode(blog["tags"]);
    let tagsNode = document.createElement("P"); // Create a n P element for it
    tagsNode.appendChild(tagsText);             // Add the text node to the p
    div.appendChild(tagsNode);                  // Add tags to the main div

    // Add a paragraph element the main div to create a gap between the post
    // and its comments (I'm not actually sure if this is happening?)
    div.appendChild(document.createElement("P"));

    // Grab the blogs comments
    let comments = blog["comments"];

    // If we actually have some comments, let's make some elements for them.
    if (comments.length != 0) {
        // For each comment, call the createCommentElement function to make
        // a new comment div and add it to our main div.
        for (let i = 0; i < comments.length; i++) {
            let commentsDiv = createCommentElement(comments[i]);
            div.appendChild(commentsDiv);
        }
    }

    // Next, create a div for the user to a post a comment with using our
    // createNewCommentElement function
    let newCommentDiv = createNewCommentElement(blog["blogid"]);
    newCommentDiv.setAttribute('class', 'well'); // Set the class attribute to be well
    div.appendChild(newCommentDiv);             // Add it to our main div

    // Add the fully formed blog div to the blogs column, that holds all the blogs
    blogsCol.appendChild(div);
}

// Function for creating a new comment element on a blog
// See above for generated HTML code
function createCommentElement(c) {
    // Create a new div well for the comments
    let commentsDiv = document.createElement("DIV");
    commentsDiv.setAttribute("class", "well");

    // Grab the comment date and split up at the spaces -
    // Current format: Sun, 15 Mar 2020 00:00:00 GMT
    // Desired format: Sun, 15 Mar 2020
    let cdate = String(c.cdate).split(" ");
    let comment_date = cdate[0] + " " + cdate[1] + " " + cdate[2] + " " + cdate[3];
    let commenter = c.posted_by + " on " + comment_date;

    // Create a text node for the commenter string we just created
    let commenterText = document.createTextNode(commenter);

    // Create a H4 element for the commenter information
    let commenterDiv = document.createElement("H4");
    commenterDiv.appendChild(commenterText);    // Add the text node to it
    commentsDiv.appendChild(commenterDiv);      // Add it to the main comments div

    // Create a string to display the sentiment
    let sentimentText = "Sentiment: "+c.sentiment;

    // Create a new paragraph element for the sentiment
    let sentimentNode = document.createElement("P");

    // Add a text node to it using the sentimentText
    sentimentNode.appendChild(document.createTextNode(sentimentText));
    commentsDiv.appendChild(sentimentNode);     // Add it to the main comments div

    // Create a new paragraph element for the description
    let descNode = document.createElement("P");
    descNode.appendChild(document.createTextNode(c.description));
    commentsDiv.appendChild(descNode);          // Add it to the main comments div

    return commentsDiv;
}

// Creates and returns a new comment element
function createNewCommentElement(blogid) {
    let form = document.createElement("FORM");   // Create a new form elemnt
    form.setAttribute("id", blogid);             // Set its ID = to the blog its posted on

    let sentiment = document.createElement("DIV"); // Create a new div for the sentiment
    sentiment.setAttribute("class", "form-group"); // Set its class

    let label = document.createElement("LABEL");   // Create a new label element
    label.setAttribute("for", "sentimentSelect");  // Set what the label is for
    label.appendChild(document.createTextNode("Sentiment")) // Add a text node to it
    sentiment.appendChild(label);                  // Add the label to the sentiment div

    let select = document.createElement("SELECT"); // Create a new select element
    select.setAttribute('class', 'form-control');  // Set its class
    select.setAttribute('id', 'sentimentSelect');  // Set its ID

    let posNode = document.createElement("OPTION"); // Create an option element
    let posText = document.createTextNode("positive"); // Create a text node
    posNode.appendChild(posText);                  // Add the text node to the element
    select.appendChild(posNode);                   // Add that to the select element

    // Repeat above but for the negative sentiment
    let negNode = document.createElement("OPTION");
    let negText = document.createTextNode("negative");
    negNode.appendChild(negText);                  // Add text node to the option element
    select.appendChild(negNode);                   // Add the negative option to the select
    sentiment.appendChild(select);                 // Add the select to the sentiment div
    form.appendChild(sentiment);                   // Add the sentiment div to the form

    let comment = document.createElement("DIV"); // Create a new div for the comment its self
    comment.setAttribute("class", "form-group"); // Set its class

    let labelc = document.createElement("LABEL"); // Create a new label element for it
    labelc.setAttribute("for", "cDescField")      // Set what the label is for
    labelc.appendChild(document.createTextNode("Description")) // Add a text node to id
    comment.appendChild(labelc);                  // Add the label to the comment div

    // Create a textarea element for the user to write their comment in
    let description = document.createElement("TEXTAREA");
    description.setAttribute("class", "form-control"); // Set its class
    description.setAttribute("type", "text");          // Set its type
    comment.appendChild(description);                  // Add it to the comment div
    form.appendChild(comment);                         // Add the comment div to the form

    // Create a comment button and it to the form
    let commentButton = document.createElement("BUTTON");  // Create comment element
    let commentText = document.createTextNode("Comment "); // Create text node
    commentButton.appendChild(commentText);                // Add it to the comment
    commentButton.setAttribute("type", "submit");          // Set its type
    commentButton.setAttribute("class", "btn");            // Set its class
    form.appendChild(commentButton);                       // Add the button to the form

    // Add an event listener to the form for when the user hits submit
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        // Get our sentiment node
        let divS = this.childNodes[0];
        let selectS = divS.childNodes[1];
        let sentiment = selectS.value;
        console.log(sentiment);

        // Hard coded values for sentiment!! Make sure hackers can't change it :)
        if (sentiment === "positive" || sentiment === "negative") {
            // Get our description node
            let divD = this.childNodes[1];
            let descText = divD.childNodes[1];
            let description = descText.value;

            // Did we get a value?
            if (description === "") {
                // TODO: Replace console.log with an actual error message to the user.
                console.log("Need to enter in a description!");
                alert("Please enter a description!");
                return
            }
            // Yep, so let's go ahead and try to add the comment to the database
            postComment(this.id, sentiment, description)
            window.location.reload()
            return
        }
        // >.>
        alert("Please only use the drop down for sentiment.");
    });

    return form;
}

// Sends a new post request to the server to add a new comment.
function postComment(blogid, sentiment, description) {
    // Create a new data object with the information we want to send
    let data = {
        blogid: blogid,
        sentiment: sentiment,
        description: description
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
    fetch('http://127.0.0.1:5555/api/newcomment', req).then(response => response.json())
        .then((body) => {
            // Log the request body
            console.log(body);

            // Did we successfully initialize the database?
            if (body.status != 200) {
                // No, create an error message an let the user know why
                console.log(body.message)
                let msg = "Comment not posted! "+ body.message
                alert(msg)
                return
            }
            // Yep, let's create a success message for the user.
            console.log(body.message);
            //alert("Comment successfully added! Please refresh to see it.");
            //addNewComment(blogid, body.commentid);
        }
    );
}
