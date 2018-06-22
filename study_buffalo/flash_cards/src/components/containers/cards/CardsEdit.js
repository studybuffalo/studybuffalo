import React from "react";
import { Link } from "react-router-dom";

import CardForm from "./CardForm";


function CardsEdit() {
  return(
    <React.Fragment>
      <h1>Modify card</h1>
      <Link to="/flash-cards/cards/">Back to card list</Link>
      <CardForm />
    </React.Fragment>
  )
}

export default CardsEdit;
