import axios from 'axios';
import PropTypes from 'prop-types';
import React from "react";

import { withRouter, Link } from 'react-router-dom';


class DeckList extends React.Component {
  constructor(props) {
    super(props);

    this.retrieveDecks = this.retrieveDecks.bind(this);

    this.state = {
      data: []
    }
  }

  componentWillMount() {
    this.retrieveDecks();
  }

  retrieveDecks() {
    axios.get("/flash-cards/api/v1/decks/")
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
    if (this.state.data) {
      return (
        <div>
          <ul>
            {
              this.state.data.map(deck => {
                const deckLink = `/flash-cards/decks/${deck.id}/`
                return (
                  <li key={deck.id}>
                    <Link to={deckLink}>
                      {deck.deck_name} {deck.deck_description}
                    </Link>
                  </li>
                )
              })
            }
          </ul>
        </div>
      );
    } else {
      return (
        <div>
          Loading...
        </div>
      )
    }
  }
}

DeckList.defaultProps = {
  owner: "",
  tags: [],
  text: ""
}

DeckList.propTypes = {
  owner: PropTypes.string,
  tags: PropTypes.arrayOf(PropTypes.string),
  text: PropTypes.string
}

export default withRouter(DeckList);
