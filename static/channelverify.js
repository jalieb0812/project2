
  function channel_verify() {

    document.querySelector('#addchannel').onsubmit = () => {

      const request = new XMLHttpRequest();

      const channel = document.querySelector("#new_channel").value;

      request.open('POST', '/channel_verify', true);

      request.onload = () => {

        const data = JSON.parse(request.responseText);

        if (data.validate == false) {
          //location.reload(true);
          window.alert(`channel name ${channel} already exists, choose a new channel name`);
          return false;
        } else {
          alert(`channel ${channel} created; entering channel: ${channel}`)
          return false;
          //location.reload(true)

        }

      }

      const data = new FormData();
      data.append('new_channel', channel)
      request.send(data);



    };
  };
