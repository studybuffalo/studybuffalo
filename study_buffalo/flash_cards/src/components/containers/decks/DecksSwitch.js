import React from "react";
import { Switch, Route } from 'react-router-dom';

import DecksCreate from './DecksCreate';
import DecksDashboard from './DecksDashboard';
import DecksEdit from './DecksEdit';

function DecksSwitch() {
  return (
    <Switch>
      <Route exact path="/flash-cards/decks/" component={DecksDashboard} />
      <Route exact path="/flash-cards/decks/create/" component={DecksCreate} />
      <Route exact path="/flash-cards/decks/:id/" component={DecksEdit} />
    </Switch>
  )
}

export default DecksSwitch;
