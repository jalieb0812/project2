function del_messages(){

document.querySelector('#message_delete_button').onclick =() =>{
  const username = localStorage.getItem('user');


  const messages = document.querySelectorAll(`.message_text_${username}`);
	for (var i = 0; i < messages.length; i++) {

    console.log('message: ', messages[i]);

    messages[i].remove();

	}




}

}
