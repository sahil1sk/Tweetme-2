import {backendLookup} from '../lookup/index'

// this fucntion is used to crete the api
export function apiTweetCreate(newTweet, callback){
  backendLookup("POST", "/tweets/create/", callback, {content: newTweet})
}

// this function is used to do like unlike and retweet
export function apiTweetAction(tweetId, action, callback) {
  const data = {id: tweetId, action:action}
  backendLookup("POST", "/tweets/action/", callback,data)
}  

// this function we make to show the detail of each tweet
export function apiTweetDetail(tweetId, callback){
  backendLookup("GET", `/tweets/${tweetId}`, callback)
}

// this function is used to load the api
export function apiTweetList(username, callback, nextUrl) { // nextUrl is basically for pagination
  let endpoint = "/tweets/"
  if (username){
    endpoint = `/tweets/?username=${username}`              // to get data match with that username we use this way
  }
  // here if we have next url then we pass end point as next url
  if(nextUrl !== null && nextUrl !== undefined){
    endpoint = nextUrl.replace("http://127.0.0.1:8000/api","")  // so here we are replacing the "http://127.0.0.1:8000/api this part becuase that part we handle in backend componenet
  }

  backendLookup("GET", endpoint, callback)
}