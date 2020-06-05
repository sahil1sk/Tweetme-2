import React, {useState} from 'react'
import {ActionBtn} from './buttons'

import {
  UserDisplay,
  UserPicture,
} from '../profiles/index'

// NOTE this file will get data from list.js


// this function will help to show the parent tweet
export function ParentTweet(props) {
    const {tweet} = props
    return(
      // here we do condition if tweet has any parent then we will show that otherwise we will show null
      tweet.parent ? <Tweet retweeter={props.reTweeter} isRetweet hideActions className={' '} tweet={tweet.parent} />: null
    );
  }
  

  // this function will call in map for formatting the tweets
  export function Tweet(props) {                        // retweeter is for who is actully doing retweet for itself
      const {tweet, didRetweet, hideActions, isRetweet, retweeter} = props   //const {tweet} = props === tweet = props.tweet
      const [actionTweet, setActionTweet] = useState(props.tweet ? props.tweet : null)
      let className = props.className ? props.className : "col-10 mx-auto-md-6"
      className = isRetweet === true ? `${className} p-2 border rounded` : className  // so here we change the above className data if is retweet
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
          {isRetweet && 
            <div className='mb-2'>
              <span className='small text-muted'>Retweet via <UserDisplay user={retweeter}/></span>
            </div>} {/*if is retweet the we show the span is retweet*/}
        
          <div className='d-flex'>    
            <div className='col-1'>
              <UserPicture user={tweet.user} />
            </div>

            <div className='col-11'>
              <div>
              
                <p>
                  <UserDisplay includeFullName user={tweet.user}/>  {/* this will help to show the username*/}
                </p>
                <p>{tweet.content}</p>
                
                <ParentTweet tweet={tweet} reTweeter={tweet.user}/>      {/* so here we call the parent tweet if there is any parent tweet so we will show othwerwise we will return null */}
              </div>
  
              {/* hide action will equal to true when it come from parents function so then it will not showing that function */}
              <div className='btn btn-group px-0'>

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
            </div>  
        </div>
      );
  }
  