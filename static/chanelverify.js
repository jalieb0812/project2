document.addEventListener('DOMContentLoaded', () => {

  document.querySelector('#create_chanel').onsubmit = () => {

    const request = new XMLHttpRequest();

    const chanel = document.querySelector("#new_chanel").value;

    request.open('GET', '/chanel_verify?chanel=' + chanel);

    request.onload = () =>{
      //console.log(JSON.parse(request.responseText))

      const chanel = document.querySelector("#new_chanel").value;

      const data = request.JSON.parse(request.responseText);

      if (data.success == false){
        location.reload(true);
        window.alert("chanel name already exists, choose a new chanel name");
      }
    }


  const data = new FormData();
  data.append('chanel', chanel)
  request.send(data);
  //return false;

  };

});
