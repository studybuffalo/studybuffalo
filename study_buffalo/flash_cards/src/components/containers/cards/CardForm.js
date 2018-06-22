import React from "react";
import PropTypes from 'prop-types';
import axios from 'axios';
import { withRouter } from 'react-router-dom';

import CardQuestion from "./CardQuestion";
// import TextInput from '../Inputs';


class CardForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      errors: false,
      question_parts: [],
      multiple_choice_answers: [],
      matching_answers: [],
      freeform_answer_parts: [],
      rationale_parts: [],
      reviewed: false,
      active: true,
      date_modified: "",
      date_reviewed: "",
      references: [],
      tags: [],
      decks: []
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
      const apiPath = path.replace('/flash-cards/cards/', '/flash-cards/api/v1/cards/');

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
      question_parts: this.state.question_parts,
      multiple_choice_answers: this.state.multiple_choice_answers,
      matching_answers: this.state.matching_answers,
      freeform_answer_parts: this.state.freeform_answer_parts,
      rationale_parts: this.state.rationale_parts,
      reviewed: this.state.reviewed,
      active: this.state.active,
      date_modified: this.state.date_modified,
      date_reviewed: this.state.date_reviewed,
      references: this.state.references,
      tags: this.state.tags,
      decks: this.state.decks
    }

    if (this.state.errors) {
      // handle errors
    } else {
      // Submit form
      axios.post("/flash-cards/api/v1/cards/", data, {headers: {"X-CSRFToken": csrfToken}})
        .then((response) => {
          // Change URL to the new view
          this.props.history.push(`/flash-cards/cards/${response.data.id}/`);
        })
        .catch((error) => {
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
  }

  handleUpdate(e) {
    // Prevent form submission
    e.preventDefault();

    // Run error checking
    this.formErrorCheck();

    // Get the API path
    const path = this.props.location.pathname;
    const apiPath = path.replace('/flash-cards/cards/', '/flash-cards/api/v1/decks/');

    // Collect data for form submissions
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const data = {
      question_parts: this.state.question_parts,
      multiple_choice_answers: this.state.multiple_choice_answers,
      matching_answers: this.state.matching_answers,
      freeform_answer_parts: this.state.freeform_answer_parts,
      rationale_parts: this.state.rationale_parts,
      reviewed: this.state.reviewed,
      active: this.state.active,
      date_modified: this.state.date_modified,
      date_reviewed: this.state.date_reviewed,
      references: this.state.references,
      tags: this.state.tags,
      decks: this.state.decks
    }

    if (this.state.errors) {
      // handle errors
    } else {
      // Submit form
      axios.put(apiPath, data, {headers: {"X-CSRFToken": csrfToken}})
        .then((response) => {
          // Change URL to the new view
          this.props.history.push(`/flash-cards/cards/${response.data.id}/`);
        })
        .catch((error) => {
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
  }

  render() {
    !this.props.new
    return (
      <form
        id="Card-Form"
        onSubmit={this.handleSubmit}
        className={this.state.errors ? "errors": ""}
      >

        <CardQuestion />

        <label htmlFor="answer-type">
          Answer type:
          <select id="answer-type">
            <option>Freeform</option>
            <option>Multiple choice</option>
            <option>Matching</option>
          </select>
        </label>

        <div>MC answer</div>
        <div>Matching answer</div>
        <div>Freeform answer</div>
        <div>Rationale</div>
        <div>References</div>
        <div>Tags</div>
        <div>Decks</div>

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

CardForm.defaultProps = {
  new: false
}

CardForm.propTypes = {
  new: PropTypes.bool,
  location: PropTypes.shape({
    pathname: PropTypes.string.isRequired,
  }).isRequired,
  history: PropTypes.shape({
    push: PropTypes.func
  }).isRequired
}

export default withRouter(CardForm);
