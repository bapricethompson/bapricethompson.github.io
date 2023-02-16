console.log("Hello World");

var myVacations = [];


var h1element = document.querySelector("#my-heading");
console.log("my h1 element", h1element);

var myButton = document.querySelector("#add-vacation-button");
console.log("my button element", myButton);

myButton.onclick = function () {
    console.log("my button was clicked");
    var VacationNameInput = document.querySelector("#vacation-name");
    console.log("my input element:", VacationNameInput);
    console.log("input element text:", VacationNameInput.value)

    createVacationOnServer(VacationNameInput.value);

    VacationNameInput.value = "";
};


var randomButton = document.querySelector("#random-vacation-button");
console.log("my random button element", randomButton);

randomButton.onclick = function () {
    console.log("my random button was clicked");
    var randomIndex = Math.floor(Math.random() * myVacations.length);
    var randomName = myVacations[randomIndex];
    var randomNameSpan = document.querySelector("#random-vacation-name");
    randomNameSpan.innerHTML = randomName + " was picked.";
};




function loadVacationFromServer() {
    fetch("http://localhost:8080/vacations").then(function (response) {
        response.json().then(function (data) {
            console.log("data recieved from server", data);
            myVacations = data;

            var myList = document.querySelector("#my-vacation-list");
            console.log("my list element:", myList);
            myList.innerHTML = "";

            //for vacation in myVacations
            myVacations.forEach(function (vacation) {
                var newItem = document.createElement("li");
                var nameDiv = document.createElement("div");
                nameDiv.innerHTML = vacation;
                nameDiv.classList.add("vacation-name");
                newItem.appendChild(nameDiv);


                // var nameDiv = document.createElement("div");
                //nameDiv.innerHTML = movie;
                // nameDiv.classList.add("movie-name");
                //newItem.appendChild(nameDive);
                //newItem.innerHTML = vacation;
                myList.appendChild(newItem);
            });

        });
    });
}

function createVacationOnServer(vacationName) {
    console.log("attempting to create", vacationName, "on server");

    var data = "name=" + encodeURIComponent(vacationName);
    console.log("sending data to server:", data);


    fetch("http://localhost:8080/vacations", {
        // request details
        method: "POST",
        body: data,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    }).then(function (response) {
        // when the server responds

        if (response.status == 201) {
            loadVacationFromServer();
        } else {
            console.log("server responded with", response.status)
        }


    });
}




loadVacationFromServer();