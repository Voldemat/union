const initialState = {
    "token"  : null,
    "email"  : null,
    "avatar" : null
}
function userReducer(state = initialState, action){
    switch(action.type){
        case "SET":
            state = action.newObject
            window.localStorage.setItem("user", JSON.stringify(state))
            console.log(window.localStorage.getItem("user"))
            return state 

        case "CHANGETOKEN":
            Object.defineProperty(state, "token", {
                "value":action.token
            })

            window.localStorage.setItem("user", JSON.stringify(state))
            console.log(window.localStorage.getItem("user"))
            return state

        default:
            try{
                state = JSON.parse(window.localStorage.getItem("user"))
            }
            catch(error){}

            finally{
                return state
            }
    }
}

export default userReducer;