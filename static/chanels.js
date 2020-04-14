
///code for making chanel form not usable unless typing inside.
document.addEventListener('DOMContentLoaded', () => {
  //default submit is disabled
  document.querySelector('#chanelsubmit').disabled = true;
  //enable chanel submit oly if text in the field
   document.querySelector('#new_chanel').onkeyup = () => {

   if (document.querySelector('#new_chanel').value.length > 0)
        document.querySelector('#chanelsubmit').disabled = false;
    else
        document.querySelector('#chanelsubmit').disabled = true;
  };

///code for adding a chanel

  document.querySelector('#addchanel').onsubmit = ()=> {
    //initilize new request
    const request = new XMLHttpRequest();

    const li = document.createElement('li');

    const new_chanel = document.querySelector('#new_chanel').value;



    request.open('POST', '/createchanel');
    //send \


    request.onload = () => {

    const data =  JSON.parse(request.responseText);

    if (data.success) {
      const contents = `chanel is ${data['new_chanel']}`;

      document.querySelector('#chanel').innerHTML = contents;

      li.innerHTML = contents;

      document.querySelector('#chanels').append(li);
    }
    else {
        document.querySelector('#chanel').innerHTML = "there was an error";
        li.innerHTML = "opps there was an error";
        document.querySelector('#chanels').append(li);

    }
 }

   const data = new FormData();

   data.append('new_chanel', new_chanel);
   request.send(data);

  //document.querySelector('#cnelsubmit').disabled = true;
   document.querySelector('#new_chanel').value = '';
    ///clear the form
  //
    /// set chanel subit back to disabled

  };

});
