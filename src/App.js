import React from 'react';
import {Router, Link} from "@reach/router";
import SplashPage from './components/SplashPage';
import Form from './components/Form';

function App() {
  return (<Router>
    <SplashPage path="/" exact={true}/>
    <Form path="/form" />
  </Router>);

}

export default App;
