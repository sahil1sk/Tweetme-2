import React, {useState} from 'react'
import {ActionBtn} from './buttons'


// NOTE this file will get data from list.js

// this function will help to show the parent tweet
export function ParentTweet(props) {
    const {tweet} = props
    return(
      // here we do condition if tweet has any parent then we will show that otherwise we will show null
      tweet.parent ? <div className='row'>
        <div className='col-11 mx-auto p-3 border rounded'>
          <p className='mb-0 text-muted small'>Retweet</p>
          <Tweet hideActions className={' '} tweet={tweet.parent} />      {/*here we send the tweet.parent because we want to show from here the parent tweet but we send classname is empty because we already set the style for it*/} 
        </div>
      </div> : null
    );
  }
  

  // this function will call in map for formatting the tweets
  export function Tweet(props) {
      const {tweet, didRetweet, hideActions} = props   //const {tweet} = props === tweet = props.tweet
      const [actionTweet, setActionTweet] = useState(props.tweet ? props.tweet : null)
      const className = props.className ? props.className : "col-10 mx-auto-md-6"
     
      // here we setting the tweet which we get as props
      const handlePerformAction = (newActionTweet,status) => {
        if(status === 200){
          setActionTweet(newActionTweet)    // here we setting the tweet which we get back measns setting like or unlike
        }else if(status === 201){
          if(didRetweet){
            didRetweet(newActionTweet) // so here send to into the props to handle retweet
          }
        }
      }  
     
      return( 
        <div className={className}>
            <div>
              <p>{tweet.id}-{tweet.content}</p>
              <ParentTweet tweet={tweet} />      {/* so here we call the parent tweet if there is any parent tweet so we will show othwerwise we will return null */}
            </div>
  
          {/* hide action will equal to true when it come from parents function so then it will not showing that function */}
          {(actionTweet && hideActions !== true) && <div className='btn btn-group'>     {/*didPerformAction will get the props back with which help we update the tweet*/}
              <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"like", display:"Likes"}}/>            {/*Calling for making the button we are calling function ActionButton*/}
              <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"unlike", display:"Unlike"}}/>
              <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"retweet", display:"Retweet"}}/>
              </div>
          }
        </div>
      );
  }
  