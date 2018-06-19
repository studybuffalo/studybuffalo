import React from "react";
import { Link } from "react-router-dom";

import CardForm from "./CardForm";


function CardsCreate() {
  return (
    <React.Fragment>
      <h1>Create new deck</h1>
      <Link to="/flash-cards/cards/">Back to deck list</Link>
      <CardForm new />
    </React.Fragment>

  )
}

export default CardsCreate;
