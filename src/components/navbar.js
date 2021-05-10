import React from 'react';

class Link extends React.Component {
   constructor(props){
      super();
      this.linkName = props.linkName;
      this.href = props.href;
   }
   render(){
      return (
         <a href={this.href}>{this.linkName}</a>
      )
   }
}




class NavBar extends React.Component {
   render(){
      return (
         <nav>
            <Link linkName="Chats" href="#"/>
            <Link linkName="Friends" href="#"/>
         </nav>
      )
   }
}

export default NavBar