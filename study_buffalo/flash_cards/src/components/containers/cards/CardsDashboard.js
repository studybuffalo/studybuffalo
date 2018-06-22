import axios from 'axios';

import React from "react";
import { Link } from 'react-router-dom';

import CardList from './CardsList';
import ErrorModal from '../ErrorModal';

class CardsDashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      owner: "",
      text: "",
      data: [],
      errors: ""
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
        this.setState({
          data: response.data,
          errors: ""
        });
      })
      .catch((error) => {
        // Set state to no data
        this.setState({data: []});

        if (error.response) {
          // Request made, but server returned error
          if (error.response.status === 404) {
            this.setState({errors: "Requested API endpoint not found"});
          } else {
            this.setState({errors: "Unable to retrieve requested data"});
          }

          Raven.captureException(error.Resresponseponse);

        } else if (error.request) {
          // Request made, but no response received
          this.setState({errors: error.request});

          Raven.captureException(error.request);
        } else {
          // Request not sent
          this.setState({errors: error.message});

          Raven.captureException(error.message);
        }
      });
  }


  render() {
    return (
      <React.Fragment>
        <h1>Flash Cards</h1>

        <Link to="/flash-cards/cards/create/" id="app-card">
          <span className="icon">+</span>
          <span>Create new card</span>
        </Link>

        <h2>Modify an existing card</h2>
        <div>
          <label htmlFor="owner-1">
            <input type="radio" name="owner" id="owner-1" value="owner" onChange={this.updateOwner} defaultChecked />
            Cards I have created/modified
          </label>
          <label htmlFor="owner-2">
            <input type="radio" name="owner" id="owner-2" value="" onChange={this.updateOwner} />
            All cards
          </label>
        </div>

        <div>
          <label htmlFor="deck-search">
            Card text
            <input type="text" id="deck-search" onChange={this.updateText} />
          </label>
        </div>

        <CardList data={this.state.data} />

        {this.state.errors && <ErrorModal errors={this.state.errors} />}
      </React.Fragment>
    )
  }
}

export default CardsDashboard;
