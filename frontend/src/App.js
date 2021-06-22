import React from 'react';
// import routing features
import {
    Route,
    Switch,
    Redirect
} from 'react-router-dom';
import { BrowserRouter as Router } from 'react-router-dom';


// Import components
import Header           from './components/Header.js';
import ChatsPage        from './pages/ChatsPage.js';
import LoggingPage      from './pages/LoggingPage';
import LogOutPage       from './pages/LogoutPage.js';
import RegistrationPage from './pages/RegistrationPage.js';
import FriendsPage      from './pages/FriendsPage.js';

// import state requirements
import { useSelector, useDispatch } from 'react-redux';
import setToken from './store/actions/setToken.js';





// import app styles
import './styles/app.css';


function App(){
    const user = useSelector(state => state.user);
    return (
            
            <Router>
                <Header />
                
                <Switch>
                    <Route path="/home" component={ChatsPage} />
                    <Route path="/friends" component={FriendsPage} />
                    {/*
                        <Route path="/chats/:chatId/" component={Chat} exact/>  
                        This route is defined in ChatsPage render method,
                        here it don`t work
                    */}
                    <Route path="/login" component={LoggingPage} exact/>
                    <Route path="/logout" component={LogOutPage} exact/>
                    <Route path="/registration" component={RegistrationPage} exact />
                    <Redirect from="/" to="/home" />
                </Switch>
                {user.token === null || user.token === undefined ? <Redirect to="/login" /> : ""}
            </Router>
            
        )
}
export default App;