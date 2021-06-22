import React, { useState, useEffect, useRef } from 'react';
// Import components
import Message from './Message.js';
import { useSelector } from 'react-redux';
import scrollButtonArrowImage from '../images/scrollButtonArrow.png';


function Chat(props){
    const [messages, setMessages] = useState([])
    const [buttonTag, setButtonTag] = useState(false)
    const user = useSelector(state => state.user)


    const inputRef = useRef()
    const submitRef = useRef()
    const scrollRef = useRef()


    function catchScroll(){
        const element = scrollRef.current;
        if (element.scrollHeight - element.scrollTop === element.clientHeight)
        {
            // code if bottom
            setButtonTag(false);

        }
        else{
            // code if scroll higher
            setButtonTag(true);
        }
    }
    function scrollDown(){
        const messagesHTMLCollection = scrollRef.current.children;
        const scrollValue = scrollRef.current.scrollHeight - messagesHTMLCollection[messagesHTMLCollection.length - 1].scrollHeight;
        scrollRef.current.scrollTop = scrollValue;
    }

    function startWebsocket(chatId){
        const socket = new WebSocket(`ws://localhost:8000/ws/chats/${chatId}/`);
        socket.onmessage = (response) => {
            let data = JSON.parse(response.data);

            if (Array.isArray(data)){
                setMessages(data);
            }
            else{
                setMessages(messages => {
                    return [...messages, data]
                })
            }
            // scroll to last message
            scrollDown();
        }
        socket.onerror = (response) => {
            console.error(JSON.parse(response));
        }
        return socket
    }
    
    
    useEffect(() => {
        const chatId = props.match.params.chatId
        const socket = startWebsocket(chatId);
        function sendMessage(event){
            if (inputRef.current.value === '') return
            socket.send(JSON.stringify({
                "message":inputRef.current.value,
                "token":user.token
            }))
            inputRef.current.value = '';
        }
        submitRef.current.addEventListener("click", sendMessage)
        return () => {
            socket.close()
        }


    }, [props.match])

    return (
            <>
                <article ref={scrollRef} onScroll={catchScroll}>
                    {messages === null ? '': messages.map(msg => {
                        return <Message message={msg} key={msg.id}/>
                    })}
                    <img src={scrollButtonArrowImage} className={`scroll-button ${buttonTag === true ? "button-appear" : ""}`} onClick={scrollDown} />
                </article>
                <form id="messageForm" onSubmit={(e) => e.preventDefault()}>
                    <input id="messageInput" ref={inputRef} type="text" placeholder="message..." />
                    <input ref={submitRef} type="submit" value="send"/>
                </form>
            </>
        )
    
}
export default Chat;