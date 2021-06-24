import React from 'react';
import '../styles/header.css';

import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';



function Header(){
    const user = useSelector(state => state.user)
    return (
            <header>
                <Link to="/" className="logo">
                    Union
                </Link>
                <Link to="/friends"> Friends </Link>
                {user.token === null ? <Link to="/login">
                    LogIn
                </Link>: (
                    <div>
                        <p>{user.email}</p>
                        <Link to="/logout">logout</Link>
                    </div>
                )}
            </header>
    )
}


export default Header