


///code for messages

document.addEventListener('DOMContentLoaded', () => {


    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port, {transports: ['websocket']});
  //

  ///code for making chanel form not usable unless typing inside.

    //default submit is disabled
    document.querySelector('#chanelsubmit').disabled = true;
    //enable chanel submit oly if text in the field
     document.querySelector('#new_chanel').onkeyup = () => {

     if (document.querySelector('#new_chanel').value.length > 0)
          document.querySelector('#chanelsubmit').disabled = false;
      else
          document.querySelector('#chanelsubmit').disabled = true;

        };
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
      const div = document.createElement('div');


      div.innerHTML = `${data.timestamp}: ${data.username}:  ${data.message} `;



    //  const row = `${data.timestamp}: ${data.username}:  ${data.message}`;



      document.querySelector('#messages').append(div);





      //document.querySelector('#messages').value += row + '\n';

      //scroll to botton of text area
      document.querySelector("#messages").scrollTop = document.getElementById("messages").scrollHeight;
      message = document.querySelector("#message").value= ''
      document.querySelector("#message").focus();

        return false;

      });

      socket.on('connect', () => {
        document.querySelector("#addchanel").onsubmit = () => {
          const chanel = document.querySelector('#new_chanel').value

          socket.emit("submit chanel", { 'chanel': chanel});

          document.querySelector('#new_chanel').value = '';
          return false;

         };

      });

      socket.on("create chanel", data => {



        row = `chanelhere: ${data.chanel}`;
        const a = document.createElement('a');
        a.setAttribute("class", "nav-link" );
        a.setAttribute('id', "chanel");
        a.setAttribute('data-page', "messages")
        a.setAttribute("href", `/chanel/${data.chanel}`  )
        a.innerHTML = `chanel: ${data.chanel}`;
        document.querySelector('#chanels').append(a)
        alert(`channel ${data.channel} created`)

        //relock chanel submit
        document.querySelector('#chanelsubmit').disabled = true;

    //  document.querySelector('#chanels').append(li) ;

});



  socket.on('connect', () => {
    document.querySelector("#channel_delete").onsubmit = () => {
      const channel = document.querySelector('#deleted_channel').value

      socket.emit("delete_channel", { 'channel': channel});

      document.querySelector('#new_chanel').value = '';
      return false;

     };

  });

  socket.on("channel_deleted", data => {


    var list = document.getElementById("chanels");
    list.removeChild(list.childNodes[data.channel]);
    alert(`channel: ${data.channel} deleted`)
    document.querySelector('#deleted_channel').value = '';
      return false;


//  document.querySelector('#chanels').append(li) ;

});

});
