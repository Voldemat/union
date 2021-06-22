import React, { useState, useEffect } from 'react';

import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux'; 

import copyText from '../utils/copyText.js';


export default function Friend(props){
    const [user, setUser] = useState(props.user);

    const friends = useSelector(state => state.friends)


    useEffect(() => {
        if (props.mode === 'detail'){
            const userId = props.match.params.userId;
            const friend = friends.find(user => user.id === userId)

            setUser(friend)
        }
    }, [props.match])
    
    
    
    return (
        <>
            {props.mode === 'preview' ? (
            <div>
                <Link to={`/friends/${user.id}`} className="friend-link">
                    <div className="container">
                        <h3 className="full-name">{user.first_name + " " + user.last_name}</h3>
                        <span className="email" onClick={(event) => copyText(event.target.innerText)}>{user.email}</span>
                    </div>
                    <img src={`http://localhost:8000${user.avatar}`} alt="avatar" className="avatar"/>
                </Link>
            </div>
            ):(
                <>
                {!user ? "":(
                    <div className="detail">
                        <div className="container">
                            <h1>{user.first_name + " " + user.last_name}</h1>
                            <span className="email" onClick={(event) => copyText(event.target.innerText)}>
                                <hr className="line"/>
                                {user.email}
                            </span>
                        </div>
                        <div className="avatar">
                            <img src={`http://localhost:8000${user.avatar}`} alt="avatar"/>
                        </div>
                        <p className="about-me">
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque sed tellus quis libero iaculis convallis. Praesent eu felis et ex iaculis vestibulum. Mauris et fringilla dui. Sed scelerisque efficitur dolor at pretium. Fusce eu hendrerit justo, ac dignissim ante. Sed semper porta tempus. Nulla quis ex ac mi facilisis venenatis vitae in felis. Mauris ac bibendum eros. Morbi id ante bibendum, facilisis est vitae, volutpat tellus. Proin sit amet vehicula leo, a ultricies leo. Maecenas vel neque suscipit, egestas nisi vel, aliquet augue. Nam aliquet hendrerit neque non scelerisque.
                        </p>
                    </div>
                )}
                </>

            )}
        </>
    )
}