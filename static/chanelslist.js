///code for chanel creation

document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port, {transports: ['websocket']});

socket.on('connect', () => {

  document.querySelector("#addchanel").onsubmit = () => {

    const chanel = document.querySelector('#new_chanel').value
    socket.emit("submit chanel", { 'chanel': chanel})
    document.querySelector('#new_chanel').value = '';


  //  return false;
  };

});

// data below is what what emited from (emit("create_chanel"))
//that is key word 'chanel':
socket.on('create chanel', data => {

const li = document.createElement('li');\

li.innerHTML= `ewrwer: ${data.chanel}`

li.innerHTML = `chanel: ${data.chanel}`;


document.querySelector('#chanels').append(chanel);


});
});
