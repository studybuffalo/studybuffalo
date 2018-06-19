import PropTypes from 'prop-types';
import React from "react";

import { withRouter, Link } from 'react-router-dom';


class CardsList extends React.PureComponent {
  render() {
    return (
      <div>
        <ul>
          {
            this.props.data.map(card => {
              const deckLink = `/flash-cards/cards/${card.id}/`
              return (
                <li key={card.id}>
                  <Link to={deckLink}>
                    {card.deck_name} {card.deck_description}
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

CardsList.defaultProps = {
  data: [],
}

CardsList.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string,
    card_name: PropTypes.string,
    card_description: PropTypes.string
  })),
}

export default withRouter(CardsList);
