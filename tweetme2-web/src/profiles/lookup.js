import {backendLookup} from '../lookup/index'


// so in this function we get the profile detail of the user which we give
export function apiProfileDetail(username, callback) {
    backendLookup("GET", `/profiles/${username}/`, callback)
}