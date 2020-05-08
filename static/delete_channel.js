document.addEventListener('DOMContentLoaded', () => {

function delete_channel() {

  document.querySelector('#delete_channel').onclick = () => {

    const request = new XMLHttpRequest();

    const channel = localStorage.getItem('current_channel');

    request.open('POST', '/delete_channel', true);

    request.onload = () => {

      if (data.success == true) {

        window.alert("channel deleted");
        window.location.assign("chanels.html");

      };

    };

    const data = new FormData();
    data.append("delete_channel", channel)
    request.send(data)

  };
};
})
