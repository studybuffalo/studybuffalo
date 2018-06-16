import axios from 'axios';

import React from "react";
import { Link } from 'react-router-dom';

import DeckList from './DeckList';

class DecksDashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      owner: "",
      text: "",
      data: []
    };

    this.updateOwner = this.updateOwner.bind(this);
    this.updateText = this.updateText.bind(this);
    this.retrieveDecks = this.retrieveDecks.bind(this);
  }

  componentDidMount() {
    // Update the state and retrieve data
    this.updateOwner();
    this.updateText();
    this.retrieveDecks();
  }

  updateOwner() {
    // Update the owner filter
    if (document.getElementById("owner-1").checked) {
      this.setState({owner: "owner"});
    } else if (document.getElementById("owner-2").checked) {
      this.setState({owner: "modified"});
    } else {
      this.setState({owner: ""});
    }

    this.retrieveDecks();
  }

  updateText() {
    // Update the text filter
    this.setState({text: document.getElementById("deck-search").value});

    this.retrieveDecks();
  }

  retrieveDecks() {
    axios.get("/flash-cards/api/v1/decks/", {
      params: {
        owner: this.state.owner,
        text_filter: this.state.text
      }
    })
      .then((response) => {
        this.setState({data: response.data});
      })
      .catch((error) => {
        if (error.response) {
          console.warn(error.response.data);
          console.warn(error.response.status);
          console.warn(error.response.headers);
        } else if (error.request) {
          console.warn(error.request);
        } else {
          console.warn(error.message);
        }
      });
  }


  render() {
    return (
      <React.Fragment>
        <h1>Flash Card Decks</h1>

        <Link to="/flash-cards/decks/create/" id="app-card">
          <span className="icon">+</span>
          <span>Create new deck</span>
        </Link>

        <h2>Modify an existing deck</h2>
        <div>
          <label htmlFor="owner-1">
            <input type="radio" name="owner" id="owner-1" value="owner" onChange={this.updateOwner} defaultChecked />
            Decks I have created/modified
          </label>
          <label htmlFor="owner-2">
            <input type="radio" name="owner" id="owner-2" value="" onChange={this.updateOwner} />
            All decks
          </label>
        </div>

        <div>
          <label htmlFor="deck-search">
            Deck Name or Description:
            <input type="text" id="deck-search" onChange={this.updateText} />
          </label>
        </div>

        <DeckList data={this.state.data} />
      </React.Fragment>
    )
  }
}

export default DecksDashboard;
