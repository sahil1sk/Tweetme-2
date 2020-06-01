import React, {useEffect, useState} from 'react'
import {
  apiTweetCreate, 
  apiTweetList,
  apiTweetAction
} from './lookup' // here we get the data from our lookup.js

// this function is help to making new tweets
export function TweetsComponent(props) {

  // here we creating ref for the textarea we see another way in our react website  
  const textAreaRef = React.createRef()
  const [newTweets, setNewTweets] = useState([])    // here we make set state for adding new component
  
  // this funtion is called when we get response and status from tthe createTweet function and this 
  // help to setting up the new tweet state
  const handleBackendUpdate = (response, status) => {
    let tempNewTweets = [...newTweets] // ... just help to copy the state
    if(status === 201){
      tempNewTweets.unshift(response)         // here we use unshift so that it will come on first
      setNewTweets(tempNewTweets)             // here we are setting the tweet  
    }else{
      alert("An error occured please try again later");
      console.log(response);
    }
  }
  
  const handleSubmit = (event) => {
    event.preventDefault()
    const newVal = textAreaRef.current.value 
    // create tweet is the function which we export from lookup which help to create the new tweet
    apiTweetCreate(newVal, handleBackendUpdate)            // so here we are passing the newvalue in the fun and getting back the response and status whcih we then handle in upperfunction
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
    const [tweetsDidSet, setTweetsDisSet] = useState(false)

    useEffect(() => {
      const final = [...props.newTweets].concat(tweetsInit) //... will hep to copy the state means making as that props so here we concating the new tweet which we get through props
      if (final.length !== tweets.length){
        setTweets(final)
      }    
    },[props.newTweets, tweets,tweetsInit]) // so we are passing this as dependency because we need that 

    // useEffect will help to implement all the function which we are able to implement in the class component    
    // here using the given useEffect we load all the data
    useEffect(() => {
      if (tweetsDidSet === false){                  // we make this if after getting the data it the given function will not call again
        const handleTweetListLookup = (response, status) => {
          if (status === 200){
            setTweetsInit(response)       //here we are setting the data in the setTweets
            setTweetsDisSet(true)
          } else {
            alert("There was an error")
          }
        }
        apiTweetList(handleTweetListLookup)    // loadTweets import this will provide data
      }
    }, [tweetsDidSet,setTweetsDisSet]) 

    // we are getting the data in tweets through setTweets
    return tweets.map((item, index)=>{
      return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`} /> // here we are calling the tweet function 
    })
}

// this function will help to create the action buttton
export function ActionBtn(props){          
  const {tweet, action} = props  
  let [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0)   // if there is tweet.likes exists then take otherwise if not means undefined then take zero
  //let [userLike, setUserLike] = useState(tweet.userLike === true ? true : false)
  const className = props.className ? props.className : 'btn btn-primary btn-sm'
  const actionDisplay = action.display ? action.display : 'Action'      // if action.dispaly exists then use action.display otherwise action
  
  const handleActionBackendEvent = (response, status) => {
    console.log("Here is it",response,status);
    if(status === 200){
      setLikes(response.likes)
    //  setUserLike(true)
    }
  }

  const handleClick = (event) => {
    event.preventDefault()
    apiTweetAction(tweet.id, action.type, handleActionBackendEvent)  
     
  }
  const display = action.type === 'like' ?  `${likes} ${actionDisplay}` : actionDisplay  // if action type is like then show count of like also otherwise normally display action
  return <button className={className} onClick={handleClick}>{display}</button>
}

// this function will help to show the parent tweet
export function ParentTweet(props) {
  const {tweet} = props
  return(
    // here we do condition if tweet has any parent then we will show that otherwise we will show null
    tweet.parent ? <div className='row'>
      <div className='col-11 mx-auto p-3 border rounded'>
        <p className='mb-0 text-muted small'>Retweet</p>
        <Tweet className={' '} tweet={tweet.parent} />      {/*here we send the tweet.parent because we want to show from here the parent tweet*/}
      </div>
    </div> : null
  );
}



// this function will call in map for formatting the tweets
export function Tweet(props) {
    const {tweet} = props   //const {tweet} = props === tweet = props.tweet
    const className = props.className ? props.className : "col-10 mx-auto-md-6"
    return <div className={className}>
        <div>
          <p>{tweet.id}-{tweet.content}</p>
          <ParentTweet tweet={tweet} />      {/* so here we call the parent tweet if there is any parent tweet so we will show othwerwise we will return null */}
        </div>

        <div className='btn btn-group'>
        <ActionBtn tweet={tweet} action={{type:"like", display:"Likes"}}/>            {/*Calling for making the button we are calling function ActionButton*/}
        <ActionBtn tweet={tweet} action={{type:"unlike", display:"Unlike"}}/>
        <ActionBtn tweet={tweet} action={{type:"retweet", display:"Retweet"}}/>
        </div>
    </div>
}
  

  
