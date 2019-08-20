import React from 'react';
import {Router, Link} from "@reach/router";
function App() {
  return (<Router>
    <SplashPage path="/" exact={true}/>
  </Router>);

}

export default App;
