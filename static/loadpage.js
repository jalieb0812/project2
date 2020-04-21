document.addEventListener('DOMContentLoaded', () => {

  ///start by loading index.innerHTML
  load_page('/');

  //set links up to load new pages.
  document.querySelectorAll('.nav-link').forEach(link => {
    link.onclick = () => {
      load_page(link.dataset.page);
      return false;
    };
  });
});

/// popstate means press back buttion on the window
/// 'e' parameter for the event that just took place; state is the state
// of whatever was just poped off
/// the data is the java script object that had title and text wanted on the page.
//update text by poping state
window.onpopstate = e => {
  const data = e.state;
  document.title = data.title; // will become title of new html page
  document.querySelector('#messagespage').innerHTML = data.text; /// this is text to fill into body of next page
};

//renders conetns of new page in main viewport

function load_page(name) {
  const request = new XMLHttpRequest();
  request.open('GET', `/messages`);
  request.onload = () => {
    const response = request.responseText;
    document.querySelector('#messagespage').innerHTML = response;

    // Push state to URL.
    document.title = name;
    /// first json obejct is the data that you are pushing to the next page
    //first 'name' is title of the page; 2nd 'name' is the url of the page.
    history.pushState({'title': name, 'text': response}, name, name);
  };
  request.send();

}
