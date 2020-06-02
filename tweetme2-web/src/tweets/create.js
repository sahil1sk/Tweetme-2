import React from 'react'
import {apiTweetCreate} from './lookup'

// this function is called by component.js file

export function TweetCreate(props){
    const textAreaRef = React.createRef()
    const {didTweet} = props
    
    // it's a callback which weill give response and status
    const handleBackendUpdate = (response, status) =>{
        if (status === 201){
        didTweet(response)
        } else {
        console.log(response)
        alert("An error occured please try again")
        }
    }

    const handleSubmit = (event) => {
      event.preventDefault()
      const newVal = textAreaRef.current.value
      // backend api request
      apiTweetCreate(newVal, handleBackendUpdate) // handle Backend is just a call back
      textAreaRef.current.value = ''
    }
    
    return (
        <div className={props.className}>
            <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className='form-control' name='tweet'>

                </textarea>
                <button type='submit' className='btn btn-primary my-3'>Tweet</button>
            </form>
        </div>
    );
}