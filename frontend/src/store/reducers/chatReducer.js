const initialState = {
    "messages":[
        {
            "text":"afadsa",
            "createdAt":"324",
            "writer":"you@email.com",
        }
    ]
}

function chatReducer(state = initialState, action){
    switch(action.type){
        case "SETMESSAGE":
            state.messages.push(action.message)
            return state
        case "SETCHAT":
            state = action.chat
            return state

        default:
            return state
    }
}
export default chatReducer;