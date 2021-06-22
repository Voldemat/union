import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector, useDispatch } from 'react-redux';
import { Route } from 'react-router-dom';

import setFriends from '../store/actions/setFriends.js';

import Friend from '../components/Friend.js';

import '../styles/friendspage.css'


export default function FriendsPage(){
    // defining state 
    const friends = useSelector(state => state.friends)
    const dispatch = useDispatch()
    const [error, setError]     = useState(null)

    // get state variables
    const user      = useSelector(state => state.user)
    const apiUrls   = useSelector(state => state.api)


    // requests to server
    useEffect(() => {
        axios.get(apiUrls.friends,{
            headers:{
                "Authorization":`Token ${user.token}`
            }
        })
        .then(response => {
            dispatch(setFriends(response.data))
        })
        .catch(error => {
            setError(error)
            console.error(error)
        })
    }, [user])
    return (
        <>
            <section className="friends-grid">
                <section className="friends-list">
                    {friends !== [] ? friends.map(friend => {
                        return <Friend user={friend} mode="preview" key={friend.id}/>
                    }):""}
                </section>
                <h1 className="friends-title">Friends</h1>
                <section className="friends-detail">
                    <Route path="/friends/:userId" render={(props) => {
                        return <Friend {...props} mode="detail" />
                    }} exact/>
                </section>
            </section>
        </>
    )
}