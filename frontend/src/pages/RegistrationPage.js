import React, { useRef, useState } from 'react';

import axios from 'axios';

import { useHistory } from 'react-router-dom';
import { useSelector } from 'react-redux';

import Error from '../components/Error.js';
import '../styles/registration.css'

export default function RegistrationPage(){

    const [error, setError] = useState({})
    const apiUrls   = useSelector(state => state.api)

    const history = useHistory()

    function createUser(event){
        event.preventDefault()

        const form = event.target


        let data = new FormData(event.target);

        axios.post(apiUrls.users + "/", data, {
                "headers": {
                    "Content-Type": false
                },
            })
        .then(response => {
            console.log(response.data)
            history.push("/login")
        })
        .catch(error => {
            console.error(error)
            setError(error)
        })

        setError({})
        form.reset()

    }
    return (
        <>
            <h1>RegistrationPage</h1>
            <section className="errors">
                {error !== {} ? <Error error={error} /> : ""}
            </section>
            <form onSubmit={createUser}>
                <input type="email" name="email"/>
                <input type="file" name="avatar"/>
                <input type="text" name="first_name"/>
                <input type="text" name="last_name"/>
                <input type="date" name="birth_date"/>
                <input type="textarea" name="about_me"/>
                <input type="password" name="password"/>
                <input type="submit" />
            </form>
        </>
    )
}