import React from 'react';
import numeral from 'numeral'; // install numerall npm instal numeral

// this function will help to show the data in good form like if 1000 then it will show 1k because of numeral
export function DisplayCount(props) {
  if(props.children <= 1000){
    return <span className={props.className}>{numeral(props.children).format("0a")}</span>  // this means if the no is less than 1000 then show in this form not in 1000.0
  }else{
    return <span className={props.className}>{numeral(props.children).format('0.0a')}</span> // this will help to show in the form of 1.0 k
  }  
}
