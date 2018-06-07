import React from "react";
import PropTypes from 'prop-types';
import axios from 'axios';
import { withRouter } from 'react-router-dom';

import TextInput from './Inputs';


class DeckForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      errors: false,
    };

    this.formErrorCheck = this.formErrorCheck.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  // Disable submit until no errors - will need to pass in
  // functions to children to retrieve error status
  formErrorCheck() {
    const formChildren = document.getElementById("Deck-Form").childNodes;
    let isValid = true;

    for (let child of formChildren){
      if (
        (child.dataset.required && !child.dataset.changed) ||
        (child.dataset.required && child.dataset.changed && child.classList.contains("errors")) ||
        (child.classList.contains("errors"))
      ) {
        isValid = false
      }
    }

    this.setState({errors: !isValid});
  }

  handleSubmit(e) {
    e.preventDefault();

    this.formErrorCheck();
    // Collect data for form submissions
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const data = {
      deck_name: document.getElementById("deck-name").value
    }

    if (this.state.errors) {
      // handle errors
    } else {
      // Submit form

      axios.post("/flash-cards/api/v1/decks/", data, {headers: {"X-CSRFToken": csrfToken}})
        .then((response) => {
          console.log(response);
          console.log(response.data);

          // Change URL to the new view
          this.props.history.push(`/flash-cards/decks/${response.data.id}/`);
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
  }

  render() {
    return (
      <form
        id="Deck-Form"
        onSubmit={this.handleSubmit}
        className={this.state.errors ? "errors": ""}
      >
        <TextInput
          id="deck-name"
          type="text"
          labelText="Deck name*"
          maxLength={255}
          formErrorCheck={this.formErrorCheck}
          required
        />
        <TextInput
          id="deck-description"
          type="text"
          labelText="Description"
          maxLength={255}
          formErrorCheck={this.formErrorCheck}
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
          <button onClick={this.handleSubmit}>Add deck</button>
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

export default withRouter(DeckForm);
