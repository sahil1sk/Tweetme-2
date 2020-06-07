import {backendLookup} from '../lookup/index'


// so in this function we get the profile detail of the user which we give
export function apiProfileDetail(username, callback) {
    backendLookup("GET", `/profiles/${username}/`, callback)
}

// this function will help to add and remove follow
export function apiProfileFollowToggle(username, action, callback) {
    const data = {action: `${action && action }`.toLowerCase()}; // so here if there is action then convert to lowecase otherwise normally null
    backendLookup("POST", `/profiles/${username}/follow/`, callback, data)
}