document.addEventListener('DOMContentLoaded', () => {



  ///code to check if channel name taken
  function channel_verify() {

    document.querySelector('#addchannel').onsubmit = () => {

      const request = new XMLHttpRequest();

      const new_channel = document.querySelector("#new_channel").value;

      request.open('POST', '/channel_verify', true);

      request.onload = () => {

        const data = JSON.parse(request.responseText);

        if (data.validate == false) {
          //location.reload(true);
          window.alert(`channel name ${new_channel} already exists, choose a new channel name`);
          return false;
        } else {

          document.getElementById("#addchannel").submit();
        }


      }

      const data = new FormData();
      data.append('new_channel', new_channel)
      request.send(data);
      //return false;


      //console.log(JSON.parse(request.responseText))

      //  const channel = document.querySelector("#new_channel").value;


    };
  };


});
