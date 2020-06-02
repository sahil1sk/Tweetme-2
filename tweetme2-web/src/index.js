import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {TweetsComponent} from './tweets/index'
import * as serviceWorker from './serviceWorker';


// Normally we get the root id from index.html file but we change id root to tweetme-2
const appEl = document.getElementById('root')

// using if it will check if the element is there then it will render otherwise no
if (appEl) {
  ReactDOM.render(
    <React.StrictMode><App /></React.StrictMode>,appEl
  );
}

// so we get the id from index.html file where we set id is tweetme-2 instead of
// root so it will check if the element is there then it will render otherwise no
const e = React.createElement // so here we create the element 
const tweetsEl = document.getElementById("tweetme-2");
if (tweetsEl) {
  // so we fetch the dataset that is written in index.html file div
  console.log(tweetsEl.dataset);
  const MyComponent = e(TweetsComponent, tweetsEl.dataset); // so this is the also way to give all the data  to the component
  ReactDOM.render(MyComponent, tweetsEl);
}

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

