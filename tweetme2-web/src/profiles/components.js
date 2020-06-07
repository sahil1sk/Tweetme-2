import React from 'react'

// NOTE this file will get data from list.js

// this function is used to send to the page where the username all tweets exists
export function UserLink (props){
  const {username} = props
  
  const handleUserLink = (event) => {
    window.location.href = `/profile/${username}`
  }
  
  return(
      // pointer class we add ourself in the index.css it's not from bootstrap
      <span className='pointer' onClick={handleUserLink}>
        {props.children}
      </span>
  )
}


// this function is used to display the name of the user
export function UserDisplay(props){
  const {user, includeFullName, hideLink} = props
  const nameDisplay = includeFullName === true ? `${user.first_name} ${user.last_name} ` : null

  return(
    <>
      {nameDisplay}
      { hideLink ? `@${user.username}` : <UserLink username={user.username}>@{user.username}</UserLink>}
    </>
  )  
}


// this function is used to display the picture of the user
export function UserPicture (props){
  const {user, hideLink} = props 
  const userIdSpan = <span className='mx-1 px-3 py-2 rounded-circle bg-dark text-white'>{user.username[0]}</span>
  return( // this means if there is hide link passed by props then not need to show the link this is only possible when user see it's profile
     hideLink ? userIdSpan : <UserLink username={user.username}>
      {userIdSpan}   
    </UserLink> 
  );
}
