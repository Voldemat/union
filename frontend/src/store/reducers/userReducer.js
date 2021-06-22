const initialState = {
    "id":null,
    "token":"c84075889cb5ecc765f317b4415178b58da6249e",
    "email":"you@email.com",
    "avatar":"/media/users/avatars/joseph-barrientos-tT6hv8y4Iz8-unsplash_1.jpg"

}
function userReducer(state = initialState, action){
    switch(action.type){
        case "SET":
            return state = action.newObject

        case "CHANGETOKEN":
            Object.defineProperty(state, "token", {
                "value":action.token
            })
            return state

        default:
            return state
    }
}

export default userReducer;