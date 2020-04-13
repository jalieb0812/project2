


///code for messages

document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure form
    socket.on('connect', () => {

      document.querySelector('#messaging').onsubmit = () => {
        const message = document.querySelector("#message").value
        socket.emit("submit message", {"message": message, "username": username})
        message.value = ''
        return false;
      };
        });


    socket.on('send message', data => {
      const li = document.createElement('li');
      document.querySelector("#newmessage").innerHTML= `newest message ${data.message}`
      li.innerHTML = ` ${data.username}:  ${data.message}`;
      document.querySelector('#messages').append(li);
      message = document.querySelector("#message").value= ''
      return false;

      });

        });



/// code for geting userwelcome greeting

document.addEventListener('DOMContentLoaded', () => {

  document.querySelector('#users').onsubmit = () => {

    //initilize new request
    const request = new XMLHttpRequest();
    const username = document.querySelector('#username').value;
    request.open('POST', '/username');

    //callback function for whn request completes
    request.onload = () => {

      //extract json database
      //const data = JSON.parse(request.responseText);

      // update result of h3 header
      // if (data.success) {
      const initial_greeting = `Hello ${username}, welcome to JOSlack`;
      document.querySelector('#userwelcome').innerHTML = initial_greeting;
      //}
      //else {
        //document.querySelector('#userwelcome').innerHTML = 'oops. error. something went wrong'
      //}
    }

    //add data to send with requests
    const data = new FormData();
    data.append('username', username)

    //send request
    request.send(data);
    document.querySelector('#username').innerHTML= ''
    //return false;
  };
});







///code for making chanel form not usable unless typing inside.
document.addEventListener('DOMContentLoaded', () => {
  //default submit is disabled
  document.querySelector('#chanelsubmit').disabled = true;
  //enable chanel submit oly if text in the field
   document.querySelector('#newchanel').onkeyup = () => {

    if (document.querySelector('#newchanel').value.length > 0)
        document.querySelector('#chanelsubmit').disabled = false;
    else
        document.querySelector('#chanelsubmit').disabled = true;
  };

  document.querySelector('#addchanel').onsubmit = ()=> {
    const chanel = document.createElement('li');
    chanel.innerHTML = document.querySelector('#newchanel').value;
    document.querySelector('#chanel').append(chanel);

    ///clear the form
    document.querySelector('#newchanel').value = '';

    /// set chanel subit back to disabled
    document.querySelector('#chanelsubmit').disabled = true;
    return false;
  }
})
