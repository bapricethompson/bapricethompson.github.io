console.log("Hello World");

var myVacations = [];


var h1element = document.querySelector("#my-heading");
console.log("my h1 element", h1element);


var myButton = document.querySelector("#add-vacation-button");
console.log("my button element", myButton);

myButton.onclick = function () {
    console.log("my button was clicked");
    var VacationLocationInput = document.querySelector("#vacation-location");
    console.log("my input element:", VacationLocationInput);
    console.log("input element text:", VacationLocationInput.value)

    var VacationActivityInput = document.querySelector("#vacation-activity");
    console.log("my input element:", VacationActivityInput);
    console.log("input element text:", VacationActivityInput.value)

    var VacationClimateInput = document.querySelector("#vacation-climate");
    console.log("my input element:", VacationClimateInput);
    console.log("input element text:", VacationClimateInput.value)

    var VacationCostInput = document.querySelector("#vacation-cost");
    console.log("my input element:", VacationCostInput);
    console.log("input element text:", VacationCostInput.value)

    var VacationLengthInput = document.querySelector("#vacation-length");
    console.log("my input element:", VacationLengthInput);
    console.log("input element text:", VacationLengthInput.value)

    createVacationOnServer(VacationLocationInput.value, VacationActivityInput.value, VacationClimateInput.value, VacationCostInput.value, VacationLengthInput.value);

    VacationLocationInput.value = "";
    VacationActivityInput.value = "";
    VacationClimateInput.value = "";
    VacationCostInput.value = "";
    VacationLengthInput.value = "";
};

var clearButton = document.querySelector("#clear-button");
clearButton.onclick = function () {

    var VacationLocationInput = document.querySelector("#vacation-location");
    console.log("my input element:", VacationLocationInput);
    console.log("input element text:", VacationLocationInput.value);
    VacationLocationInput.value = "";
    var VacationActivityInput = document.querySelector("#vacation-activity");
    VacationActivityInput.value = "";
    var VacationClimateInput = document.querySelector("#vacation-climate");
    VacationClimateInput.value = "";
    var VacationCostInput = document.querySelector("#vacation-cost");
    VacationCostInput.value = "";
    var VacationLengthInput = document.querySelector("#vacation-length");
    VacationLengthInput.value = "";
    var myButton = document.querySelector("#add-vacation-button");
    myButton.innerHTML = "Add Vacation";
    myButton.onclick = function () {
        console.log("my button was clicked");
        var VacationLocationInput = document.querySelector("#vacation-location");
        console.log("my input element:", VacationLocationInput);
        console.log("input element text:", VacationLocationInput.value)

        var VacationActivityInput = document.querySelector("#vacation-activity");
        console.log("my input element:", VacationActivityInput);
        console.log("input element text:", VacationActivityInput.value)

        var VacationClimateInput = document.querySelector("#vacation-climate");
        console.log("my input element:", VacationClimateInput);
        console.log("input element text:", VacationClimateInput.value)

        var VacationCostInput = document.querySelector("#vacation-cost");
        console.log("my input element:", VacationCostInput);
        console.log("input element text:", VacationCostInput.value)

        var VacationLengthInput = document.querySelector("#vacation-length");
        console.log("my input element:", VacationLengthInput);
        console.log("input element text:", VacationLengthInput.value)

        createVacationOnServer(VacationLocationInput.value, VacationActivityInput.value, VacationClimateInput.value, VacationCostInput.value, VacationLengthInput.value);

        VacationLocationInput.value = "";
        VacationActivityInput.value = "";
        VacationClimateInput.value = "";
        VacationCostInput.value = "";
        VacationLengthInput.value = "";

    }

}


//var randomButton = document.querySelector("#random-vacation-button");
//console.log("my random button element", randomButton);

//randomButton.onclick = function () {
//    console.log("my random button was clicked");
//    var randomIndex = Math.floor(Math.random() * myVacations.length);
//    var randomName = myVacations[randomIndex];
//    var randomNameSpan = document.querySelector("#random-vacation-name");
//    randomNameSpan.innerHTML = randomName + " was picked.";
//};




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
                var locationDiv = document.createElement("h1");
                locationDiv.innerHTML = vacation.location;
                locationDiv.classList.add("vacation-location");
                newItem.appendChild(locationDiv);

                var activityDiv = document.createElement("div");
                activityDiv.innerHTML = vacation.activity;
                activityDiv.classList.add("vacation-activity");
                newItem.appendChild(activityDiv);

                var climateDiv = document.createElement("div");
                climateDiv.innerHTML = vacation.climate;
                climateDiv.classList.add("vacation-climate");
                newItem.appendChild(climateDiv);

                var costDiv = document.createElement("div");
                costDiv.innerHTML = vacation.cost;
                costDiv.classList.add("vacation-cost");
                newItem.appendChild(costDiv);

                var lengthDiv = document.createElement("div");
                lengthDiv.innerHTML = vacation.length;
                lengthDiv.classList.add("vacation-length");
                newItem.appendChild(lengthDiv);

                var deleteButton = document.createElement("button");
                deleteButton.innerHTML = "Delete";
                deleteButton.onclick = function () {
                    console.log("delete button clicked", vacation.location);
                    if (confirm("Are you sure?")) {
                        deleteVacationFromServer(vacation.id);
                    }
                };
                newItem.appendChild(deleteButton)

                var editButton = document.createElement("button");
                editButton.innerHTML = "Edit";
                editButton.onclick = function () {
                    console.log("edit button clicked", vacation.id);
                    var VacationLocationInput = document.querySelector("#vacation-location");
                    console.log("my input element:", VacationLocationInput);
                    console.log("input element text:", VacationLocationInput.value);
                    VacationLocationInput.value = vacation.location;
                    var VacationActivityInput = document.querySelector("#vacation-activity");
                    VacationActivityInput.value = vacation.activity;
                    var VacationClimateInput = document.querySelector("#vacation-climate");
                    VacationClimateInput.value = vacation.climate;
                    var VacationCostInput = document.querySelector("#vacation-cost");
                    VacationCostInput.value = vacation.cost;
                    var VacationLengthInput = document.querySelector("#vacation-length");
                    VacationLengthInput.value = vacation.length;
                    var myButton = document.querySelector("#add-vacation-button");
                    myButton.innerHTML = "Save";
                    myButton.onclick = function () {
                        updateVacationFromServer(vacation.id, VacationLocationInput.value, VacationActivityInput.value, VacationClimateInput.value, VacationCostInput.value, VacationLengthInput.value)

                    }

                };
                newItem.appendChild(editButton)

                myList.appendChild(newItem);
            });

        });
    });
}

function createVacationOnServer(vacationLocation, vacationActivity, vacationClimate, vacationCost, vacationLength) {
    console.log("attempting to create", vacationLocation, "on server");

    var data = "location=" + encodeURIComponent(vacationLocation);
    data += "&activity=" + encodeURIComponent(vacationActivity);
    data += "&climate=" + encodeURIComponent(vacationClimate);
    data += "&cost=" + encodeURIComponent(vacationCost);
    data += "&length=" + encodeURIComponent(vacationLength);
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

function deleteVacationFromServer(vacationId) {
    fetch("http://localhost:8080/vacations/" + vacationId, {
        method: "DELETE",
    }).then(function (response) {
        if (response.status == 200) {
            loadVacationFromServer();
        } else {
            console.log("server responded with ", response.status)
        }
    })
}


// WORK
function updateVacationFromServer(vacationId, vacationLocation, vacationActivity, vacationClimate, vacationCost, vacationLength) {
    var data = "location=" + encodeURIComponent(vacationLocation);
    data += "&activity=" + encodeURIComponent(vacationActivity);
    data += "&climate=" + encodeURIComponent(vacationClimate);
    data += "&cost=" + encodeURIComponent(vacationCost);
    data += "&length=" + encodeURIComponent(vacationLength);
    console.log("sending data to server:", data);
    fetch("http://localhost:8080/vacations/" + vacationId, {
        method: "PUT",
        body: data,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function (response) {

        if (response.status == 200) {
            loadVacationFromServer();
            var VacationLocationInput = document.querySelector("#vacation-location");
            VacationLocationInput.value = "";
            var VacationActivityInput = document.querySelector("#vacation-activity");
            VacationActivityInput.value = "";
            var VacationClimateInput = document.querySelector("#vacation-climate");
            VacationClimateInput.value = "";
            var VacationCostInput = document.querySelector("#vacation-cost");
            VacationCostInput.value = "";
            var VacationLengthInput = document.querySelector("#vacation-length");
            VacationLengthInput.value = "";
            var myButton = document.querySelector("#add-vacation-button");
            myButton.innerHTML = "Add Vacation";
            myButton.onclick = function () {
                console.log("my button was clicked");
                var VacationLocationInput = document.querySelector("#vacation-location");
                console.log("my input element:", VacationLocationInput);
                console.log("input element text:", VacationLocationInput.value)

                var VacationActivityInput = document.querySelector("#vacation-activity");
                console.log("my input element:", VacationActivityInput);
                console.log("input element text:", VacationActivityInput.value)

                var VacationClimateInput = document.querySelector("#vacation-climate");
                console.log("my input element:", VacationClimateInput);
                console.log("input element text:", VacationClimateInput.value)

                var VacationCostInput = document.querySelector("#vacation-cost");
                console.log("my input element:", VacationCostInput);
                console.log("input element text:", VacationCostInput.value)

                var VacationLengthInput = document.querySelector("#vacation-length");
                console.log("my input element:", VacationLengthInput);
                console.log("input element text:", VacationLengthInput.value)

                createVacationOnServer(VacationLocationInput.value, VacationActivityInput.value, VacationClimateInput.value, VacationCostInput.value, VacationLengthInput.value);

                VacationLocationInput.value = "";
                VacationActivityInput.value = "";
                VacationClimateInput.value = "";
                VacationCostInput.value = "";
                VacationLengthInput.value = "";

            }

        } else {
            console.log("server responded with ", response.status)
        }
    })
}

loadVacationFromServer();