import React from "react";
import PropTypes from 'prop-types';
import TextInput from './Inputs';

class DeckForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      deck_name: "",
      deck_description: "",
      errors: false,
    };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  // Disable submit until data in each field (onKeyUp)
  // onBlur validate the entered text


  handleSubmit() {
    this.setState({
      deck_name: "",
      deck_description: ""
    });
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} className={this.state.errors ? "errors": ""}>
        <TextInput
          id="deck-name"
          type="text"
          label_text="Deck name:"
          max_length={255}
          required
        />
        <TextInput
          id="deck-description"
          type="text"
          label_text="Description:"
          max_length={255}
        />

        {!this.props.new &&
          <div>
            Active?
            <label htmlFor="deck-active-1">
              <input type="radio" name="deck-active" id="deck-active-1" defaultChecked />
              Yes
            </label>
            <label htmlFor="deck-active-2">
              <input type="radio" name="deck-active" id="deck-active-2" />
              No
            </label>
            <span className="errors" />
          </div>
        }
        <div>
          <button>Add deck</button>
        </div>
      </form>
    );
  }
}

DeckForm.defaultProps = {
  new: false
}

DeckForm.propTypes = {
  new: PropTypes.bool
}

export default DeckForm;
