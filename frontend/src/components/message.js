import React, { useRef } from 'react';
import { useSelector } from 'react-redux';


function Message(props){
    const msg = props.message
    const user = useSelector(state => state.user)
    const apiUrl = useSelector(state => state.api)

    const writerRef = useRef()

    function writerAppear(event){
        const elStyles = writerRef.current.style
        elStyles.transform = "translateX(0px)";
        elStyles.opacity = "1";

    }
    function writerDisappear(event){
        const elStyles = writerRef.current.style
        elStyles.transform = "translateX(70px)";
        elStyles.opacity = "0";
    }

    return (
            <>
                <div className={msg.writer.email === user.email ? "my-message" : "other-message"}>
                    <span ref={writerRef}>{msg.writer.first_name + " " + msg.writer.last_name}</span>
                    <img onMouseEnter={writerAppear} onMouseLeave={writerDisappear} src={apiUrl.domain + msg.writer.avatar} alt="avatar" />
                    <p>{msg.text}</p>
                    
                </div>
            </>
        )
}

export default Message;