import React, {useEffect, useState} from 'react'
import { apiTweetList } from './lookup' // apiTweetList will help to fetch all the tweets
import {Tweet} from './detail'

// NOTE this will get data from component.js

// in this function all the things will implement this will load the data
// and then calll
// this will get data from tweet.component
export function TweetsList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [tweetsDidSet, setTweetsDisSet] = useState(false)

    useEffect(() => {
      const final = [...props.newTweets].concat(tweetsInit) //... will hep to copy the state means making as that props so here we concating the new tweet which we get through props
      if (final.length !== tweets.length){
        setTweets(final)
      }    
    },[props.newTweets, tweets,tweetsInit]) // so we are passing this as dependency because we need that 

    // useEffect will help to implement all the function which we are able to implement in the class component    
    // here using the given useEffect we load all the data
    useEffect(() => {
      if (tweetsDidSet === false){                  // we make this if after getting the data it the given function will not call again
        const handleTweetListLookup = (response, status) => {
          if (status === 200){
            setTweetsInit(response)       //here we are setting the data in the setTweets
            setTweetsDisSet(true)
          } else {
            alert("There was an error")
          }
        }             // we are passing  the username now time for checking
        apiTweetList(props.username, handleTweetListLookup)    // loadTweets import this will provide data
      }
    }, [tweetsDidSet,setTweetsDisSet, props.username])  // we have to passing the props.username as dependecncy because we have to use this 

    // this function will help to handle the retweet
    const handleDidRetweet = (newTweet) => {
      const updateTweetsInit = [...tweetsInit]    // so here we just make copy of tweetsInit state
      updateTweetsInit.unshift(newTweet)          // we are adding newTweet means retweet in unshift mode so that it will come first
      setTweetsInit(updateTweetsInit)         // and here we finally set the retweet
    
      const updateFinalTweets = [...tweets]   // so here we again make the state copy
      updateFinalTweets.unshift(tweets)       // so here we set the tweets 
      setTweets(updateFinalTweets)            // and finally setting the data

      //NOTE we do this with both tweets and tweetInit so that it length will matched 
      // Because on upper useEffect we make condition if (final.length !== tweets.length) the length is not matched then set the tweet 
        
    }

    // we are getting the data in tweets through setTweets
    return tweets.map((item, index)=>{
      return( 
        <Tweet 
        tweet={item} 
        didRetweet={handleDidRetweet} 
        className='my-5 py-5 border bg-white text-dark' 
        key={`${index}-{item.id}`} 
        /> // here we are calling the tweet function 
      );    
    })
}
