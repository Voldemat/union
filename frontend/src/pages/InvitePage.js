import React from 'react';

import { useParams } from 'react-router-dom';

export default function InvitePage(){
    const params = useParams()
    console.log(params)
    return (<>

        <h1>InvitePage</h1>
    </>)
}