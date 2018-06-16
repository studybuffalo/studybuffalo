import PropTypes from 'prop-types';
import React from "react";

import { withRouter, Link } from 'react-router-dom';


class DeckList extends React.PureComponent {
  render() {
    return (
      <div>
        <ul>
          {
            this.props.data.map(deck => {
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
  }
}

DeckList.defaultProps = {
  data: [],
}

DeckList.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string,
    deck_name: PropTypes.string,
    deck_description: PropTypes.string
  })),
}

export default withRouter(DeckList);
