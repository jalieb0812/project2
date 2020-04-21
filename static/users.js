/// code for geting userwelcome greeting

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector("#users").style.visibility = "hidden";


  //setInterval(count, 1000); maybe do somethign like this.

  document.querySelector('#users').onsubmit = () => {



    //initilize new request
    const request = new XMLHttpRequest();
    const username = document.querySelector('#username').value;
    request.open('POST', '/username');

    //callback function for whn request completes
    request.onload = () => {

      //extract json database
      let data = JSON.parse(request.responseText);

      // update result of h3 header
      if (data.success) {
      const initial_greeting = `Hello ${username}, welcome to JOSlack; choose or enter a chanel`;
      document.querySelector('#userwelcome').innerHTML = initial_greeting;
        document.querySelector('#username').innerHTML= '';
        document.querySelector("#users").style.visibility = "hidden";

      }
      else {
        document.querySelector('#userwelcome').innerHTML = 'oops. error. something went wrong'
          document.querySelector('#username').innerHTML= '';
      }

    }

    //add data to send with requests
      const data = new FormData();
      data.append('username', username)

    //send request
    request.send(data);
    return false;


  };

});
