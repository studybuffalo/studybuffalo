/* eslint react/no-multi-comp: 0 */

import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from 'react-router-dom';

import Main from "./containers/Main";
import Menu from "./containers/Menu";

// Setup Raven
Raven.config('https://7db3dda0b6184c6a9a279b6697cafd96@sentry.studybuffalo.com/4').install()

// TODO: Remove eslint rule for Link component when next ESLint edition released

function App() {
  return (
    <React.Fragment>
      <Menu />
      <Main />
    </React.Fragment>
  )
}

ReactDOM.render(
  (
    <BrowserRouter>
      <App name="Josh" />
    </BrowserRouter>
  ),
  document.getElementById('app')
);
