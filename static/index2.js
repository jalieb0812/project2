///function for the alert

///    document.addEventListener('DOMContentLoaded', () => {
///      const person = prompt("Please enter your name", "Name");
///      if (person != null) {
///        document.getElementById("demo").innerHTML =
///      "Hello " + person + "! How are you today?";
///    }
///    })

// local storage use to Remember user
// set username to nothing
if (!localStorage.getItem('user'))

document.addEventListener('DOMContentLoaded', () => {
// if first sign in; then welcome sign happens
    document.querySelector('#welcometext').innerHTML = "Welcome to JO Slack app. To begin, enter your username";
})

/// if already signed in previously
if(localStorage.getItem('user'))
  document.addEventListener('DOMContentLoaded', () => {
    let user = localStorage.getItem('user');
      document.querySelector('#welcometext').innerHTML = `Hi ${user}`;

      ///remove username form is signed in previously
        var usernameform = document.querySelector('#username');
         usernameform.remove();

    });


///run this code only if person has not signed in
if(!localStorage.getItem('user'));
/// function to change the greeting h1
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#username").onsubmit = () => {

      const user = document.querySelector('#user').value;

      document.querySelector('#greeting').innerHTML = `hello ${user}`;

      //set the users name in memory
      localStorage.setItem('user', user);

      ///code to add the usernames
      const li = document.createElement('li');
      li.innerHTML = document.querySelector('#user').value;

      document.querySelector('#names').append(li);
      /// clear the form
      document.querySelector('#user').value  = '';

      return false;
    }
  })



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
