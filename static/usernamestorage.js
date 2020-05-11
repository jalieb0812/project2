///function for the alert

///    document.addEventListener('DOMContentLoaded', () => {
///      const person = prompt("Please enter your name", "Name");
///      if (person != null) {
///        document.getElementById("demo").innerHTML =
///      "Hello " + person + "! How are you today?";
///    }
///    })

// local storage use to Remember user


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
    //enable channel submit oly if text in the field
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

      /// set channel subit back to disabled
      document.querySelector('#messagesubmit').disabled = true;
      return false;
    }
  })
