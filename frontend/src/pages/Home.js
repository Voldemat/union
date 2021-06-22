import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import {Route, Link, useHistory} from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';


import Chat from '../components/Chat.js';
import '../styles/chats.css';


function HomePage(props){
    
    return <h1>HomePage</h1>

}


export default HomePage