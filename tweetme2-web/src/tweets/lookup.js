import {BackendLookup} from '../lookup/index'

// this fucntion is used to crete the api
export function apiTweetCreate(newTweet, callback){
  BackendLookup("POST", "/tweets/create/", callback, {content: newTweet})
}

// this function is used to do like unlike and retweet
export function apiTweetAction(tweetId, action, callback) {
  const data = {id: tweetId, action:action}
  BackendLookup("POST", "/tweets/action/", callback,data)
}  

// this function is used to load the api
export function apiTweetList(callback) {
  BackendLookup("GET", "/tweets/", callback)
}