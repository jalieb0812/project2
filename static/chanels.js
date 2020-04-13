
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

///code for adding a chanel


  document.querySelector('#addchanel').onsubmit = ()=> {
    //initilize new request
    const request = new XMLHttpRequest();
    const chanel =  document.querySelector('#newchanel').value;
  //  const new_chanel_name = document.querySelector('#newchanel').value;
    request.open('GET', '/createchanel');

    //callback function for when request completes
    //request.onload = ()=> {

    //add new chanel
    //chanel.innerHTML = new_chanel_name;
  //  document.querySelector('#chanels').append(chanel);


//  }

    //add data to send with requests
    const data = new FormData();
    data.append('chanel', chanel)

    //send requests
    request.send(data);
    ///clear the form
  //  document.querySelector('#newchanel').value = '';
    /// set chanel subit back to disabled
    document.querySelector('#chanelsubmit').disabled = true;

//   return false;
  };
});
