import axios from 'axios';

import React from "react";
import { Link } from 'react-router-dom';
import ReactModal from 'react-modal';

import DeckList from './DeckList';


ReactModal.setAppElement("#app");

class DecksDashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      owner: "",
      text: "",
      data: [],
      errors: "",
      showModal: false
    };

    this.updateOwner = this.updateOwner.bind(this);
    this.updateText = this.updateText.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
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

  handleCloseModal () {
    this.setState({showModal: false});
  }

  retrieveDecks() {
    axios.get("/flash-cards/api/v1/deck/", {
      params: {
        owner: this.state.owner,
        text_filter: this.state.text
      }
    })
      .then((response) => {
        this.setState({data: response.data});
      })
      .catch((error) => {
        // Set state to no data
        this.setState({data: []});
        this.setState({showModal: true});

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

        <ReactModal
          isOpen={this.state.showModal}
          contentLabel="Error retrieving data"
          onRequestClose={this.handleCloseModal}
        >
          {this.state.errors}
          <button onClick={this.handleCloseModal}>Close Modal</button>
        </ReactModal>
      </React.Fragment>
    )
  }
}

export default DecksDashboard;
