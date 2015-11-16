console.log(window.swampdragon_settings.config_name); // output bar
// ouput http://localhost:9999 assuming you are running your server on that url
console.log(window.swampdragon_host);

swampdragon.ready(function () {
    subscribe();
});

function subscribe(){
    swampdragon.subscribe('chat', 'chatroom', null, function (context, data) {
            //this.dataMapper = new DataMapper(data);
        });
}
swampdragon.onChannelMessage(function (channels, data) {
    console.log(channels + data.data.name + "," + data.data.message);
    $("#chats").append(data.data.name + "," + data.data.message + "</br>");
});

function sendMessage (name, message) {

    // Send message
    swampdragon.callRouter('chat', 'chat', {name:name, message:message}, null, function (e, error) {
        console.log(e);
    });
}

function sumbitMessage(){
    sendMessage($("#txtNmae").val(), $("#txtMessage").val());
}