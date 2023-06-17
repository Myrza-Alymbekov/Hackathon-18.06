// chat/static/index.js

console.log("Sanity check from index.js.");

// redirect to '/room/<roomSelect>/'
document.querySelector("#roomSelect").onchange = function() {
    let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
    window.location.pathname = "chat/room/" + roomName + "/";
}

// redirect to '/create_private_chat/<username>/'
document.querySelector("#privateSelect").onclick = function() {
    let username = document.querySelector("#privateSelect").value;
    window.location.pathname = "chat/create_private_chat/" + username + "/";
}