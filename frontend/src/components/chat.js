import React, { useState, componentDidMount} from 'react';
import Message from './message.js';

import '../css/chat.css';
const chat_url = `ws://localhost:8000/ws/chats/7c40c1cc-d0b4-45d6-972d-a48d12e51d71/`;
const chatSocket = new WebSocket(chat_url);
function Chat(props){
   const chat_id = props.chat_id;
   

   const [messages, setMessages] = useState('');
   
   chatSocket.onmessage = async response => {
      let data = JSON.parse(response.data);
      console.log(data);
      
      if (!Array.isArray(data)){
         let new_messages = messages;
         new_messages.push(data);
         await setMessages(new_messages);
         console.log('New message')
         console.log(messages);
      }
      else{
            // window.data = data;
            // window.setMessages = setMessages;
            // data.forEach(mes => )
            await setMessages(data);
            console.log('Initial state')
            await console.log(messages);
      }
   }
   chatSocket.onerror = function(e){
      console.log(e)
   }

   chatSocket.onclose = function(e) {
      console.log('Websocket close')
   };

   return (
      <section>
         <h1>Chat</h1>
         {messages && messages.map(mes => <Message text={mes.text} writer={mes.writer} created_at={mes.created_at} />)}
         {/* {messages && messages.map(msg => <ChatMessage key={msg.id} message={msg}/>)} */}
      </section>
   )
}

export default Chat