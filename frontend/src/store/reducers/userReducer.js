const initialState = {
    "id":null,
    "token":"48cf7f3015d3ecfde4153e6778e578a17a112488",
    "email":"viocan2005@gmail.com",
    "avatar": null

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