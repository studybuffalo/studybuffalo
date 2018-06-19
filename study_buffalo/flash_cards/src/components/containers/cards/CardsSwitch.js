import React from "react";
import { Switch, Route } from 'react-router-dom';

import CardsCreate from "./CardsCreate";
import CardsDashboard from "./CardsDashboard";
import CardsEdit from "./CardsEdit";

function CardsSwitch() {
  return (
    <Switch>
      <Route exact path="/flash-cards/cards/" component={CardsDashboard} />
      <Route exact path="/flash-cards/cards/create/" component={CardsCreate} />
      <Route exact path="/flash-cards/cards/:id/" component={CardsEdit} />
    </Switch>
  )
}

export default CardsSwitch;
