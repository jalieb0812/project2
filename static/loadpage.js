document.addEventListener('DOMContentLoaded', () => {

  ///start by loading index.innerHTML
  load_page('chanels');

  //set links up to load new pages.
  document.querySelectorAll('.nav-link').forEach(link => {
    link.onclick = () => {
      load_page(link.dataset.page);
      return false;
    };
  });
});


//renders conetns of new page in main viewport

function load_page(name) {
  const request = new XMLHttpRequest();
  request.open('GET', `/${name}`);
  request.onload = () => {
    const response = request.responseText;
    document.querySelector('#messagespage').innerHTML = response;
  };
  request.send();

}
