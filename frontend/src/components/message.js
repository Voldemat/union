import React, { useState } from 'react';


function Message({text, writer, created_at}){

   return (
      <div>{text} - {writer} - {created_at}</div>
   )
}

export default Message;