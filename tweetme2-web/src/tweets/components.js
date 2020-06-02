import React, {useEffect, useState}  from 'react'
import {apiTweetDetail} from './lookup'
import {Tweet} from './detail'
import {TweetCreate} from './create'
import {TweetsList} from './list'

// so in this TweetsComponent we get props from index.js file
export function TweetsComponent(props) {
    const [newTweets, setNewTweets] = useState([])
    const canTweet = props.canTweet === "false" ? false : true  // this we get from index.js file which get from index.html file
    
    const handleNewTweet = (newTweet) =>{
      let tempNewTweets = [...newTweets]      // here we just make a copy of the state as we know
      tempNewTweets.unshift(newTweet)         // Here we set the data in variable using unshift because unshift help to shift the tweet on first side
      setNewTweets(tempNewTweets)             // here we setting the new tweet and then that is passed to TweetsList
    }

    return( 
      // {''} Replace with props.className if any styling mistake 
      <div className={''}> 
            {canTweet === true && <TweetCreate didTweet={handleNewTweet} className='col-12 mb-3' />}  {/* DidTweet will get the reponse back and then tha is handled by handleNewTweet*/}
            <TweetsList newTweets={newTweets} {...props} /> {/*...props means we send all the props to list component*/}
      </div>
    );
}

// this function will help to show the detail of the single tweet 
export function TweetDetailComponent(props){
  const {tweetId} = props
  const [didLookup, setDidLookup] = useState(false)
  const [tweet, setTweet] = useState(null)

  const handleBackendLookup = (reponse, status) => {
    if(status === 200){
      setTweet(reponse)
    } else {
      alert("There was an error while finding your tweet!");
    }
  }

  useEffect(()=>{
   if (didLookup === false){
     apiTweetDetail(tweetId, handleBackendLookup) // here we send the TweetId for getting detaill and then get callback in handledBackendLookup
     setDidLookup(true)
   } 
  }, [tweetId, didLookup, setDidLookup]) 

  return  tweet === null ? null : <Tweet tweet={tweet} className={props.className}/>  // if tweet is equal to null then we will return null otherwise return the Tweet function which will show the like and to perform all other task
}
