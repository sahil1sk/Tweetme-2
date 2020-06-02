import React, {useState}  from 'react'

import {TweetCreate} from './create'
import {TweetsList} from './list'

// so in this TweetsComponent we get props from index.js file
export function TweetsComponent(props) {
    const [newTweets, setNewTweets] = useState([])
    const canTweet = props.canTweet === "false" ? true : true  // this we get from index.js file which get from index.html file
    
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