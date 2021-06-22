import React, { useEffect } from 'react';

import { useDispatch } from 'react-redux';
import { Redirect } from 'react-router-dom';


import setObject from '../store/actions/setObject.js'

function LogOutPage(){
    const dispatch = useDispatch()
    useEffect(() => {
        dispatch(setObject({"token":null}))
    }, [])
    return (
        <Redirect to="/login" />
    )
}
export default LogOutPage;