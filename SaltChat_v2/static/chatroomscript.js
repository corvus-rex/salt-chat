window.onload = function(){

    var socket = io.connect('http://127.0.0.1:5000', {transports: ['websocket']});
    var firstConnect = true;
    var myUsername = "";

    sendButtonListener(socket);

    socket.on('connect', function(){
        socket.emit('connection event');
    });

    socket.on('someone connected', function(username, avatar, onlineUsers, onlineUserAvatars){
        console.log(firstConnect)
        if(firstConnect){
            myUsername = username;
            for(var c = 0; c < onlineUsers.length; c++){
                console.log(onlineUsers[c])
                addUserToOnlineDiv(onlineUsers[c], onlineUserAvatars[c]);
                connectionBroadcast(username, true);
            }
            firstConnect = false;
        }
        else{
            addUserToOnlineDiv(username, avatar);
            connectionBroadcast(username, true);
        }
    });

    socket.on('incoming message', function(message, author, avatar){
        if(author == myUsername){
            addMessageFromSelf(author, avatar, message);
        }
        else{
            addMessageFromOtherUser(author, avatar, message);
        }
    });

    socket.on('disconnect event', function(username){
        let divToRemove = "." + username + "-user-online-div";
        $(divToRemove).remove();
        connectionBroadcast(username, false)
    });

    // https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_element_scrollleft2
    // https://stackoverflow.com/questions/31662681/flask-handle-form-with-radio-buttons/31663422
};

function sendButtonListener(socket){
    $('#send-message').on('click', function(){
        var message = $('#type-message').val()
        if (message != ""){
            socket.emit('message', message);
            $('#type-message').val('');
        }
    });
}

function addUserToOnlineDiv(displayName, avatar){
  $("#online-users").append(
    '<div class = "' + displayName + '-user-online-div">' +
    '<img class = "avatar-sidebar-img" src=static/images/' + avatar + ".png>" +
    displayName +
    '</div>')
  }

function connectionBroadcast(username, connectionEvent){
    if(connectionEvent == true){
        $("#messages").append('<div class = "connection-broadcast-message">' + displayName + " has joined the room. </div>");
    }
    else{
        $("#messages").append('<div class = "connection-broadcast-message">' + displayName + " has left the room. </div>");
    }
}

function addMessageFromSelf(author, avatar, message){
    $("#messages").append('<div class = "my-messages">' + message + "<img class = 'messages-avatar' src = static/images/" + avatar + ".png>" + '</div>'
)};

function addMessageFromOtherUser(author, avatar, message){
  $("#messages").append('<div class = "other-messages">' +
  "<img class = 'messages-avatar' src = static/images/" + avatar + ".png>" +
  author +
  ": " +
  message +
  '</div>'
)};

