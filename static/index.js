///code for messages

document.addEventListener('DOMContentLoaded', () => {


  // Connect to websocket
  const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  //work u shit

  ///code for making channel form not usable unless typing inside.

  //default submit is disabled
  document.querySelector('#channelsubmit').disabled = true;
  //enable channel submit oly if text in the field
  document.querySelector('#new_channel').onkeyup = () => {

    if (document.querySelector('#new_channel').value.length > 0)
      document.querySelector('#channelsubmit').disabled = false;
    else
      document.querySelector('#channelsubmit').disabled = true;

  };

  //code for ensuring channels cant have the same name
  function channel_verify() {
    document.querySelector('#addchannel').onsubmit = () => {

      const request = new XMLHttpRequest();

      const channel = document.querySelector("#new_channel").value;

      request.open('POST', '/channel_verify', true);

      request.onload = () => {

        const data = JSON.parse(request.responseText);

        if (data.validate == false) {
          //location.reload(true);
          window.alert(`channel name ${channel} already exists, choose a new channel name`);
          return false;
        } else {
          alert(`channel ${channel} created; entering channel: ${channel}`)
          //return false;
          //location.reload(true)

        }

      }

      const data = new FormData();
      data.append('new_channel', channel)
      request.send(data);
      //  return false;


    };
  };



  // When connected, configure form
  socket.on('connect', () => {
    // 'Enter' key on textarea also sends a message
    // https://developer.mozilla.org/en-US/docs/Web/Events/keydown
    document.querySelector('#message').addEventListener("keydown", event => {
        if (event.key == "Enter") {
            document.getElementById("messagesubmit").click();
        }
    });


    document.querySelector('#messaging').onsubmit = () => {
      const message = document.querySelector("#message").value
      const timestamp = Math.floor(Date.now() / 1000)

      const queryString = window.location.search;
      const urlParams = new URLSearchParams(queryString);
      const username = urlParams.get('username');
      const channel = urlParams.get('channel');

      socket.emit("submit message", {
        'timestamp': timestamp,
        'username': username,
        "message": message,
        "channel": channel
      })
      message.value = ''
      return false;
    };

    document.querySelector("#addchannel").onsubmit = () => {
      const channel = document.querySelector('#new_channel').value

      socket.emit("submit channel", {
        'channel': channel
      });

      document.querySelector('#new_channel').value = '';
      return false;

    };

    document.querySelector("#channel_delete").onsubmit = () => {
      const channel = document.querySelector('#deleted_channel').value

      socket.emit("delete_channel", {
        'channel': channel
      });

      document.querySelector('#deleted_channel').value = '';
      //return channel_verify();

    };



   document.querySelector('#message_delete_button').onclick = () =>{
     const username=localStorage.getItem("user");
     const queryString = window.location.search;
     const urlParams = new URLSearchParams(queryString);
     channel = urlParams.get('channel');

     socket.emit("delete_messages", {'username': username, 'channel': channel})
    ///}


  };


  socket.on('send message', data => {




    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    if (urlParams.get('channel'))
      channel = urlParams.get('channel');


    else {
      channel = localStorage.getItem('current_channel');
    }



    if (channel == data.channel) {
      const div = document.createElement('div');


      div.innerHTML = `${data.timestamp}: ${data.username}:  ${data.message} `;

      div.setAttribute('class', `message_text_${data.username}`);

      //  const row = `${data.timestamp}: ${data.username}:  ${data.message}`;

      document.querySelector('#messages').append(div);

      //document.querySelector('#messages').value += row + '\n';

      //scroll to botton of text area
      document.querySelector("#messages").scrollTop = document.getElementById("messages").scrollHeight;
      message = document.querySelector("#message").value = ''
      document.querySelector("#message").focus();

    };

    return false;

  });


  socket.on("create channel", data => {



    row = `channelhere: ${data.channel}`;
    const a = document.createElement('a');
    a.setAttribute("class", "nav-link");
    a.setAttribute('id', "channel");
    a.setAttribute('data-page', "messages")
    a.setAttribute("href", `/channel/${data.channel}`)
    a.innerHTML = `channel: ${data.channel}`;
    document.querySelector('#channels').append(a);
    alert(`hmmm channel ${data.channel} created`);

    //relock channel submit
    document.querySelector('#new_channel').value = '';
    document.querySelector('#channelsubmit').disabled = true;
    //return false;

    //  document.querySelector('#channels').append(li) ;

  });



  socket.on("channel_deleted", data => {



      var list = document.getElementById("channels");
      list.removeChild(list.childNodes[data.channel]);
      alert(`channel: ${data.channel} deleted`)
      document.querySelector('#deleted_channel').value = '';
      //return false;

//    }



    //  document.querySelector('#channels').append(li) ;

  });


    socket.on("messages_deleted", data => {

      const messages = document.querySelectorAll(`.message_text_${data.username}`);
      for (var i = 0; i < messages.length; i++) {

        console.log('message: ', messages[i]);

        messages[i].remove();

      }

      alert(`${data.username} deleted their messages in channel ${data.channel}`);



    });


});

});
