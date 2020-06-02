import React from 'react'
import {apiTweetAction} from './lookup' // here we get the data from our lookup.js


// this function will help to create the action buttton
export function ActionBtn(props){          
    const {tweet, action, didPerformAction} = props  
    const likes = tweet.likes ? tweet.likes : 0   
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'      // if action.dispaly exists then use action.display otherwise action
    
    const handleActionBackendEvent = (response, status) => {
      console.log(response);
      if((status === 200 || status===201) && didPerformAction ){
        didPerformAction(response,status)            // so here we send the props which contain response
      }
    }
  
    const handleClick = (event) => {
      event.preventDefault()
      apiTweetAction(tweet.id, action.type, handleActionBackendEvent)  
       
    }
    const display = action.type === 'like' ?  `${likes} ${actionDisplay}` : actionDisplay  // if action type is like then show count of like also otherwise normally display action
    return <button className={className} onClick={handleClick}>{display}</button>
  }
  