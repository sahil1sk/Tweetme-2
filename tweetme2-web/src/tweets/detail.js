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
      
      const path = window.location.pathname                   // so here we get the urlpath
      const match = path.match(/(?<tweetid>\d+)/)            // here we match the path with regex
      const urlTweetId = match ? match.groups.tweetid : -1  // so if the path match then we get the id otherwise we get -1

      const isDetail = `${tweet.id}` === `${urlTweetId}`;  // so now we check if the tweet id match with url tweetid then it's true then we not showing the view button
      
      // this function will help to set the id on the url 
      // so that it will detect in the index.html file  
      const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/${tweet.id}` 
      }

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
          <div className='btn btn-group'>

            {(actionTweet && hideActions !== true) && <>     {/*didPerformAction will get the props back with which help we update the tweet*/}
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"like", display:"Likes"}}/>            {/*Calling for making the button we are calling function ActionButton*/}
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"unlike", display:"Unlike"}}/>
                <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:"retweet", display:"Retweet"}}/>
                </>
            }

            {/*Because we want to show the detail of both the parent and child tweet that's why we make detail button it outside div*/}
            {/*so when we are on the detail view then we make it nul so that now this button will not shown*/}
            {isDetail === true ? null: <button className='btn btn-outline-primary' onClick={handleLink}>View</button>}    {/*We make button to view the detail of the tweet*/}

          </div>
          
        </div>
      );
  }
  