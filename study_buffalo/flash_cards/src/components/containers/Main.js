import React from "react";
import { Switch, Route } from "react-router-dom";

import CardsSwitch from "./cards/CardsSwitch";
import Dashboard from "./dashboard/Dashboard";
import DecksSwitch from "./decks/DecksSwitch";

function Main() {
  return (
    <div id="main">
      <Switch>
        <Route exact path="/flash-cards/" component={Dashboard} />
        <Route path="/flash-cards/decks/" component={DecksSwitch} />
        <Route path="/flash-cards/cards/" component={CardsSwitch} />
      </Switch>
    </div>
  )
}

export default Main;
