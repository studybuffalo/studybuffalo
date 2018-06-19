import React from "react";
import { Link } from "react-router-dom";

import DeckForm from "./DeckForm";


function DecksCreate() {
  return (
    <React.Fragment>
      <h1>Create new deck</h1>
      <Link to="/flash-cards/decks/">Back to deck list</Link>
      <DeckForm new />
    </React.Fragment>

  )
}

export default DecksCreate;
