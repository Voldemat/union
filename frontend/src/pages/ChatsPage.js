import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import {Route, Link, useHistory} from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';


import Chat from '../components/Chat.js';
import '../styles/chats.css';


function ChatsPage(props){
    
    const apiUrls = useSelector(state => state.api)
    
    const user = useSelector(state => state.user)
    const chat = useSelector(state => state.chat)

    const history = useHistory()

    const [chats, setChats] = useState([])

    const form = useRef()

    useEffect(() => {
        if (user.token === null){
            history.push('/login')
        }
        axios.get(apiUrls.chats,{
          headers: {
            'Authorization': `Token ${user.token}`
          }
        })
            .then(response => {
                setChats(state => [...state, ...response.data])
            })
            .catch(error => {
                console.error(error)
            })
        
    }, [])


    return (
            <>
                <section className="chats-grid">

                    <section className="navbar">
                        <div className="search">
                            Search
                        </div>
                        {chats == null ? '' : chats.map(chat => {
                            return <Link className="chatlink" to={`/home/${chat.id}/`} key={chat.id}>{chat.name === '' || chat.name === undefined ? chat.id : chat.name}</Link>
                        })}
                    </section>
                <Route path="/home/:chatId/" component={Chat} exact/>      
                </section>


            </>
    )
    


}


export default ChatsPage