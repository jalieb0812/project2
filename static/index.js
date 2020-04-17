


///code for messages

document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure form
    socket.on('connect', () => {

      document.querySelector('#messaging').onsubmit = () => {
        const message = document.querySelector("#message").value
        const timestamp = Math.floor(Date.now() / 1000)
        socket.emit("submit message", { 'timestamp': timestamp, 'username': username, "message": message })
        message.value = ''
        return false;
      };
        });


    socket.on('send message', data => {
      //const row = document.createElement('row');
      document.querySelector("#newmessage").innerHTML= `${data.timestamp}: ${data.username}: ${data.message}`
      const row = `${data.timestamp}: ${data.username}:  ${data.message}`;
      document.querySelector('#messages').value += row + '\n';
      message = document.querySelector("#message").value= ''
      //return false;

      });

    });


  ///code for making message form not usable unless typing inside.
  document.addEventListener('DOMContentLoaded', () => {
    //default submit is disabled
    document.querySelector('#messagesubmit').disabled = true;
    //enable chanel submit oly if text in the field
     document.querySelector('#message').onkeyup = () => {

      if (document.querySelector('#message').value.length > 0)
          document.querySelector('#messagesubmit').disabled = false;
      else
          document.querySelector('#messagesubmit').disabled = true;
    };

    document.querySelector('#messaging').onsubmit = ()=> {
      const li = document.createElement('li');
      li.innerHTML = document.querySelector('#message').value;
      document.querySelector('#messages').append(li);

      ///clear the form
      document.querySelector('#message').value = '';

      /// set chanel subit back to disabled
      document.querySelector('#messagesubmit').disabled = true;
      return false;
    }
  })
