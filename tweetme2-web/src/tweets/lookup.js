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
export function apiTweetList(username, callback) {
  let endpoint = "/tweets/"
  if (username){
    endpoint = `/tweets/?username=${username}`              // to get data match with that username we use this way
  }
  backendLookup("GET", endpoint, callback)
}