// this badge.js file helps to show the profile of the user

import React, {useState, useEffect} from 'react';
import {apiProfileDetail, apiProfileFollowToggle} from './lookup';
import {UserDisplay, UserPicture} from './components';

// this function will call all the function which will help to show the user profile
// Also help to show the follow button
function ProfileBadge(props) {
  const {user, didFollowToggle, profileLoading} = props;
  let currentVerb = (user && user.is_following) ? "Unfollow" : "follow"
  currentVerb = profileLoading ? "Loading..." : currentVerb // if profileLoading is true then we will set loading.. here 

  // this function will come in action when the button is clicked
  const handleFollowToggle = (event) => {
    event.preventDefault()
    if(didFollowToggle && !profileLoading) { // this mmeans if profile loading is not true then the user is able to click the button otherwise not
      didFollowToggle(currentVerb)
    }
  }

  return user ? <div>
                  <UserPicture user={user} hideLink /> 
                  <p><UserDisplay user={user} hideLink includeFullName/></p> {/*this do for display data from UserDisplay*/}
                  <button className='btn btn-outline-primary' onClick={handleFollowToggle}>{currentVerb}</button>
                </div> 
              : null
}

// this component will help to get the data from the backend api
export function ProfileBadgeComponent (props) {
    const {username} = props
    const [didLookup, setDidLookup] = useState(false)
    const [profileLoading, setProfileLoading] = useState(false)
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

    const handleNewFollow = (actionVerb) => {
      setProfileLoading(true); //  here we set the profileLoading to true which help to toggle on the other side
      // so here we adding the follow and unfollow
      apiProfileFollowToggle(username, actionVerb, (response, status)=>{  // so we handle callback here not making any function
        if(status === 200){
          setProfile(response);   // so after getting the response we set the profile and this will help to change the follow or unfollow
        }
        setProfileLoading(false);
      })
      
    }
  
    return didLookup === false ? "Loading..." : profile ? <ProfileBadge user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading}/> : null
}