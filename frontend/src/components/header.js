import React from 'react';

// import styles
import '../css/header.css';

// import components
import Navbar from './navbar.js';

class Header extends React.Component {
   constructor(props){
      super(props);
      this.colorTheme = props.colorTheme;
   }
   render(){
     return (
        <header>
           <h1>Union</h1>
           <Navbar />
           <div className="menu"></div>
        </header>
     )
   }
}

export default Header