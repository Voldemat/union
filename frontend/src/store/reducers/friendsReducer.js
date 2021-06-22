const initialState = []
function friendsReducer(state = initialState, action){
    switch(action.type){
        case "SETFRIENDS":
            return state = action.friends

        default:
            return state
    }
}

export default friendsReducer;