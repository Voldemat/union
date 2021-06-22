import React, { useRef, useState } from 'react';
import axios from 'axios';

import { useHistory, Redirect, Link } from "react-router-dom";

import { useSelector, useDispatch } from 'react-redux';
import setToken from '../store/actions/setToken.js'
import setObject from '../store/actions/setObject.js'

import Error from '../components/Error.js';




export default function LoggingPage(){
    const [error, setError] = useState(null)

    const user = useSelector(state => state.user)
    const dispatch = useDispatch()

    const history = useHistory()


    function logIn(event){
        event.preventDefault()

        const formData = new FormData(event.target)

        window.formData = formData
        const data = {
            "username":formData.get("email"),
            "password":formData.get("password")
        }
        window.data = data
        axios.post("http://localhost:8000/api/v1/token-auth/", data)
            .then(response => {
                dispatch(setObject(response.data))
                setError(null)
                history.push("/")
            })
            .catch(error => {
                setError(error)
                console.error(error)
            })

    }
    return (
        <>
            <section>
                <h1>Logging Page</h1>
                <section className="errors">
                    {error !== null ? "": ""}
                </section>
                <form id="loginform" onSubmit={logIn}>
                    <input type="email" name="email"/>
                    <input type="password" name="password"/>
                    <input type="submit" value="Login" />
                </form>
                <p>If you don't have account yet, <Link to="/registration">create new!</Link></p>
            </section>
            
        </>
    )
}