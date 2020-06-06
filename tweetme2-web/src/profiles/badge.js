import React, {useState, useEffect} from 'react'
import {apiProfileDetail} from './lookup'

// this component helps to show the profile of the user

export function ProfileBadgeComponent (props) {
    const {username} = props
    const [didLookup, setDidLookup] = useState(false)
    const [profile, setProfile] = useState(null)
  
    const handleBackendLookup = (reponse, status) => {
      if(status === 200){
        setProfile(reponse)
      }
    }
  
    useEffect(()=>{
     if (didLookup === false){
        apiProfileDetail(username, handleBackendLookup) // here we send the TweetId for getting detaill and then get callback in handledBackendLookup
       setDidLookup(true)
     } 
    }, [username, didLookup, setDidLookup]) 
  
    return didLookup === false ? "Loading..." : profile ? <span>{profile.first_name}</span> : null
}