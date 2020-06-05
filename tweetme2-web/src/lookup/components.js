// this function helps to make the api

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// this function is used to deal with api
export function backendLookup(method, endpoint, callback, data) {
  let jsonData;
  if (data){
    jsonData = JSON.stringify(data)
  }
  const xhr = new XMLHttpRequest()
  const url = `http://127.0.0.1:8000/api${endpoint}`
  xhr.responseType = "json"
  const csrftoken = getCookie('csrftoken');
  xhr.open(method, url)
  xhr.setRequestHeader("Content-Type", "application/json")

  if (csrftoken){
   // xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
  }

  xhr.onload = function() {
    if(xhr.status === 403 && xhr.response){       // if the status is 403 then it true and we check inner if
      const detail = xhr.response.detail          // so here we take the detail of the response
      if(detail === "Authentication credentials were not provided."){  // so in this if we check the detail is equal to authentication not provided then redirect the user to login page
        if(window.location.href.indexOf("login") === -1){ // this if means if there is no login at pathname then show login if there is login then not show again and again
          window.location.href = "/login?showLoginRequired=true"
        }              // we also add show login required to true
      }
    }
    callback(xhr.response, xhr.status)
  }
  xhr.onerror = function (e) {
    console.log(e)
    callback({"message": "The request was an error"}, 400)
  }
  xhr.send(jsonData)
}
