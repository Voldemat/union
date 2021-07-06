const baseUrl = "http://localhost:8000"
const initialState = {
    "domain"            :   baseUrl,
    "base"              :   baseUrl + "/api/v1",
    "chats"             :   baseUrl + "/api/v1/chats",
    "personal-chats"    :   baseUrl + "/api/v1/personal-chats",
    "users"             :   baseUrl + "/api/v1/users",
    "friends"           :   baseUrl + "/api/v1/friends"

}

function apiUrlReducer(state = initialState, action){
    switch(action.type){
        default:
            return state
    }
}
export default apiUrlReducer