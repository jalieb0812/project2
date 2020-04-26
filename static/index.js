


///code for messages

document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure form
    socket.on('connect', () => {

      document.querySelector('#messaging').onsubmit = () => {
        const message = document.querySelector("#message").value
        const timestamp = Math.floor(Date.now() / 1000)

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const username = urlParams.get('username')

        socket.emit("submit message", { 'timestamp': timestamp, 'username': username, "message": message })
        message.value = ''
        return false;
      };
        });


    socket.on('send message', data => {
      //const row = document.createElement('row');
    //  document.querySelector("#newmessage").innerHTML= `${data.timestamp}: ${data.username}: ${data.message}`
      const row = `${data.timestamp}: ${data.username}:  ${data.message}`;

      document.querySelector('#messages').value += row + '\n';

      //scroll to botton of text area
      document.querySelector("#messages").scrollTop = document.getElementById("messages").scrollHeight
      message = document.querySelector("#message").value= ''
        return false;


      });
  return false;
    });
