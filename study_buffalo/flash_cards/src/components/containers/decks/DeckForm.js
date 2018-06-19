import React from "react";
import PropTypes from 'prop-types';
import axios from 'axios';
import { withRouter } from 'react-router-dom';

import TextInput from '../Inputs';


class DeckForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      errors: false,
    };

    this.formErrorCheck = this.formErrorCheck.bind(this);
    this.handleCreate = this.handleCreate.bind(this);
    this.handleUpdate = this.handleUpdate.bind(this);
  }

  componentDidMount() {
    // Load initial data to form
    if (!this.props.new) {
      // Get the new API path
      const path = this.props.location.pathname;
      const apiPath = path.replace('/flash-cards/decks/', '/flash-cards/api/v1/decks/');

      axios.get(apiPath)
        .then((response) => {
          document.getElementById('deck-name').value = response.data.deck_name;
          document.getElementById('description').value = response.data.description;

          if (response.data.active) {
            document.getElementsByClassName('active')[0].checked = true;
          } else {
            document.getElementsByClassName('active')[1].checked = true;
          }
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
        })
    }
  }

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

  handleCreate(e) {
    // Prevent form submission
    e.preventDefault();

    // Run error checking
    this.formErrorCheck();

    // Collect data for form submissions
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const data = {
      deck_name: document.getElementById("deck-name").value,
      description: document.getElementById("description").value
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

  handleUpdate(e) {
    // Prevent form submission
    e.preventDefault();

    // Run error checking
    this.formErrorCheck();

    // Get the API path
    const path = this.props.location.pathname;
    const apiPath = path.replace('/flash-cards/decks/', '/flash-cards/api/v1/decks/');

    // Collect data for form submissions
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const data = {
      deck_name: document.getElementById("deck-name").value,
      description: document.getElementById("description").value,
      active: document.getElementsByClassName("active")[0].checked ? true: false
    }

    if (this.state.errors) {
      // handle errors
    } else {
      // Submit form
      axios.put(apiPath, data, {headers: {"X-CSRFToken": csrfToken}})
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
    !this.props.new
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
          id="description"
          type="text"
          labelText="Description"
          maxLength={500}
          formErrorCheck={this.formErrorCheck}
        />

        {!this.props.new &&
          <div>
            Active?
            <label htmlFor="deck-active-1">
              <input
                type="radio"
                name="deck-active"
                id="deck-active-1"
                className="active"
                defaultChecked
              />
              Yes
            </label>
            <label htmlFor="deck-active-2">
              <input
                type="radio"
                name="deck-active"
                id="deck-active-2"
                className="active"
              />
              No
            </label>
            <span className="errors" />
          </div>
        }

        <div>
          {
            this.props.new ?
            (
              <button onClick={this.handleCreate}>Add deck</button>
            ) : (
              <button onClick={this.handleUpdate}>Update deck</button>
            )
          }
        </div>
      </form>
    );
  }
}

DeckForm.defaultProps = {
  new: false
}

DeckForm.propTypes = {
  new: PropTypes.bool,
  location: PropTypes.shape({
    pathname: PropTypes.string.isRequired,
  }).isRequired,
}

export default withRouter(DeckForm);
