import React from 'react';
import {render} from 'react-dom';


import { Provider } from 'react-redux';
import App from './App.js';

// Import store
import store from './Store.js';

render(
    <React.StrictMode>
        <Provider store={store}>
            <App/>
        </Provider>
    </React.StrictMode>,
    document.querySelector('#root')
)