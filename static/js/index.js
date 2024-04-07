function openNav() {
    document.getElementById("myChatbotContainer").style.width = "45%";
    document.getElementById("myChatbotContainer").style.boxShadow = "20px 20px 50px 15px #030303";
    document.getElementById("main").style.marginLeft = "45%x";
    document.body.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
}

function closeNav() {
    document.getElementById("myChatbotContainer").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.body.style.backgroundColor = "transparent";
}


// Add this JavaScript code to handle the file input change event
document.getElementById("imageUpload").addEventListener("change", function (event) {
    var file = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function (e) {
        var img = document.getElementById("uploaded-image");
        img.src = e.target.result;
        document.getElementById("uploaded-image-container").style.display = "block";
    };

    reader.readAsDataURL(file);
});

document.getElementById("imageUpload").addEventListener("change", function (event) {
    var file = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function (e) {
        var img = document.getElementById("uploaded-image");
        img.src = e.target.result;
        document.getElementById("panel-container").style.display = "block"; // Show the panel
    };

    reader.readAsDataURL(file);
});

// Close panel when the close button is clicked
document.getElementById("close-panel-btn").addEventListener("click", function () {
    document.getElementById("panel-container").style.display = "none"; // Hide the panel
});


// send query to rasa api
function sendMessage(message) {
    $("#chat-widget-input").val("");
    $("#chat-widget-messages").append("<div style='display: flex; justify-content: flex-end; align-items: center;'><div style='max-width: 25vw; background-color: #ededed; border-radius: 10px; padding: 10px; margin-bottom: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'><span style='font-size: 0.85rem; font-weight: bold; color: #555;'>YOU</span><div style='color: #151515; margin-top: 5px;'>" + message + "</div></div></div><br>");
    $.ajax({
        type: "POST",
        url: "/webhook",
        contentType: "application/json",
        data: JSON.stringify({ message: message }),
        success: function (data) {
            let botResponse = data.response;
            $("#chat-widget-messages").append("<div style='display: flex; align-items: center;'><div style='max-width: 25vw; background-color: rgb(92, 161, 252); border-radius: 10px; padding: 10px; margin-bottom: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'><span style='font-size: 0.85rem; font-weight: bold; color: #fff;'>SNAKY BOT</span><div style='color: #151515; margin-top: 5px;'>" + botResponse + "</div></div></div><br>");
        },
        error: function () {
            // Handle errors here (optional)
        }
    });
}

// send msg to api and get response on keypress
function handleKeyPress(event) {
    if (event.which === 13) {
        let userMessage = $("#chat-widget-input").val();
        sendMessage(userMessage);
    }
}

var preDefinedMessage = "common_rattle_snake";

function sendMessageOnClick() {
    sendMessage(preDefinedMessage);
}

$(document).ready(function () {
    $("#chat-widget-input").keypress(handleKeyPress);
    // $("#custom-btn").click(sendMessageOnClick())
});

function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}



