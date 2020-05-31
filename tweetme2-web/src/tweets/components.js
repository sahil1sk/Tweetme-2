import React, {useEffect, useState} from 'react'
import {loadTweets} from '../lookup'

// this function is help to making new tweets
export function TweetsComponent(props) {

  // here we creating ref for the textarea we see another way in our react website  
  const textAreaRef = React.createRef()
  const [newTweets, setNewTweets] = useState([])    // here we make set state for adding new component
  const handleSubmit = (event) => {
    event.preventDefault()
    const newVal = textAreaRef.current.value 
    let tempNewTweets = [...newTweets]        // here we just copy the state 
    tempNewTweets.unshift({                   // unshift will help to add newest tweet on begining
      content:newVal,
      likes:0,
      id: 1233
    })
    setNewTweets(tempNewTweets)             // here we setting the state normally
    textAreaRef.current.value = ''
  }

  return( 
    <div className={props.className}> 
      <div className='col-12 mb-3'>
        <form onSubmit={handleSubmit}>
          <textarea ref={textAreaRef} required={true} className="form-control" name='tweet'>
          </textarea>
          <button type='submit' className='btn btn-primary my-3'>Tweet</button>
        </form>
      </div>  
      <TweetsList newTweets={newTweets}/>     {/* so here we pass the tweet that which we make if there is no tweet then it will send empty data */}
    </div>
  );

}

// in this function all the things will implement this will load the data
// and then calll
export function TweetsList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])

    useEffect(() => {
      const final = [...props.newTweets].concat(tweetsInit) // so here we concating the new tweet which we get
      if (final.length !== tweets.length){
        setTweets(final)
      }    
    },[props.newTweets, tweets,tweetsInit]) // so we are passing this as dependency because we need that 

    // useEffect will help to implement all the function which we are able to implement in the class component    
    // here using the given useEffect we load all the data
    useEffect(() => {
      const myCallback = (response, status) => {
        if (status === 200){
          setTweetsInit(response)       //here we are setting the data in the setTweets
        } else {
          alert("There was an error")
        }
      }
      loadTweets(myCallback)    // loadTweets import this will provide data
    }, []) 

    // we are getting the data in tweets through setTweets
    return tweets.map((item, index)=>{
      return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`} /> // here we are calling the tweet function 
    })
}

// this function will help to create the action buttton
export function ActionBtn(props){          
  const {tweet, action} = props  
  let [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0)   // if there is tweet.likes exists then take otherwise if not means undefined then take zero
  let [userLike, setUserLike] = useState(tweet.userLike === true ? true : false)
  const className = props.className ? props.className : 'btn btn-primary btn-sm'
  const actionDisplay = action.display ? action.display : 'Action'      // if action.dispaly exists then use action.display otherwise action
  const handleClick = (event) => {
    event.preventDefault()
    if (action.type === 'like'){
      if(userLike === true){
        setLikes(likes - 1)       // Now here we subtracting from the current like
        setUserLike(false)
      }else{
        setLikes(likes + 1)
        setUserLike(true)
      }
    }
  }
  const display = action.type === 'like' ?  `${likes} ${actionDisplay}` : actionDisplay  // if action type is like then show count of like also otherwise normally display action
  return <button className={className} onClick={handleClick}>{display}</button>
}


// this function will call in map for formatting the tweets
export function Tweet(props) {
    const {tweet} = props   //const {tweet} = props === tweet = props.tweet
    const className = props.className ? props.className : "col-10 mx-auto-md-6"
    return <div className={className}>
        <p>{tweet.id}-{tweet.content}</p>
        <div className='btn btn-group'>
        <ActionBtn tweet={tweet} action={{type:"like", display:"Likes"}}/>            {/*Calling for making the button we are calling function ActionButton*/}
        <ActionBtn tweet={tweet} action={{type:"unlike", display:"Unlike"}}/>
        <ActionBtn tweet={tweet} action={{type:"retweet", display:"Retweet"}}/>
        </div>
    </div>
}
  

  
