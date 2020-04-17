/// code for geting userwelcome greeting


document.addEventListener('DOMContentLoaded', () => {

  if (document.querySelector('#users')) {

    document.querySelector('#users').onsubmit = () => {

    const request = new XMLHttpRequest();

    const username = document.querySelector('#username').value;

    //add data to send with requests
    const data = new FormData();
    data.append('username', username);

    request.open('POST', '/username');

    //send request
    request.send(data);


//callback function for whn request completes
    request.onload = () => {

      let data = JSON.parse(request.responseText);
      // update result of h3 header
      if (data.success) {
      const initial_greeting = `Hello ${username}, welcome to JOSlack`;
      document.querySelector('#userwelcome').innerHTML = initial_greeting;
      var userform = document.querySelector('#users');
      userform.remove();

      }
      else {
        document.querySelector('#userwelcome').innerHTML = 'please enter a username';
        document.querySelector('#users').value = '';
      }

    }
    return false;
  }

 }

});
