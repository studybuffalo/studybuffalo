import React from "react";
import { Link } from "react-router-dom";

import DeckForm from "./DeckForm";


function DecksEdit() {
  return(
    <React.Fragment>
      <h1>Modify deck</h1>
      <Link to="/flash-cards/decks/">Back to deck list</Link>
      <DeckForm />
    </React.Fragment>
  )
}

export default DecksEdit;
