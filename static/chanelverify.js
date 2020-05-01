document.addEventListener('DOMContentLoaded', () => {



  ///code to check if chanel name taken
          function chanel_verify() {

              document.querySelector('#addchanel').onsubmit = () => {

                const request = new XMLHttpRequest();

                const new_chanel = document.querySelector("#new_chanel").value;

                request.open('POST', '/chanel_verify', true);

                request.onload = () => {

                  const data = JSON.parse(request.responseText);

                  if (data.validate == false){
                    //location.reload(true);
                    window.alert("chanel name already exists, choose a new chanel name");
                    return false;
                  }

                  else {
                    alert("chanel created")
                    document.getElementById("#addchanel").submit();
                  }


                }

                const data = new FormData();
                data.append('new_chanel', new_chanel)
                request.send(data);
                //return false;


                  //console.log(JSON.parse(request.responseText))

                //  const chanel = document.querySelector("#new_chanel").value;


              };
            };


});
