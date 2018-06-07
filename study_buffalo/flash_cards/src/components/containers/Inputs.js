import React from "react";
import PropTypes from 'prop-types';

class TextInput extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      valid: true,
      changed: false,
      error_messages: []
    }

    this.handleTextChange = this.handleTextChange.bind(this);
    this.handleInitialChange = this.handleInitialChange.bind(this);
  }

  handleInitialChange() {
    if (!this.state.changed) {
      this.setState({changed: true})
    }
  }

  handleTextChange(e) {
    const input = e.target;
    let errorMessages = [];

    if (this.props.required && input.value.length === 0) {
      errorMessages.push("This field is required.");
    } else if (this.props.maxLength && input.value.length > this.props.maxLength) {
      errorMessages.push(
        "This field must be "
        + this.props.maxLength
        + this.props.maxLength === 1 ? (
          "character long."
        ) : (
          "characters long or less."
        )
      );
    }

    if (errorMessages.length) {
      this.setState({
        valid: false,
        error_messages: errorMessages
      });
    } else {
      this.setState({
        valid: true,
        error_messages: errorMessages
      });
    }
  }

  render() {
    return (
      <div
        className={!this.state.valid ? "errors" : ""}
        data-changed={this.state.changed}
        data-required={this.props.required}
      >
        {
          this.props.type.toLowerCase() === "text" ? (
            <label htmlFor={this.props.id}>
              <span>{this.props.labelText}</span>
              <input
                type="text"
                id={this.props.id}
                onKeyUp={(e) => {
                  this.handleTextChange(e); this.props.formErrorCheck(e)
                }}
                onBlur={this.handleInitialChange}
              />
            </label>
          ) : (
            <label htmlFor={this.props.id}>
              {this.props.labelText}
              <textarea
                id={this.props.id}
                onKeyUp={this.handleTextChange}
                onBlur={this.props.formErrorCheck}
              />
            </label>
          )
        }
        <span className="errors">{this.state.error_messages.join(" ")}</span>
      </div>
    )
  }
}

TextInput.defaultProps = {
  type: "text",
  labelText: "",
  required: false,
  maxLength: 0,
  formErrorCheck: null
}

TextInput.propTypes = {
  id: PropTypes.string.isRequired,
  type: PropTypes.string,
  labelText: PropTypes.string,
  required: PropTypes.bool,
  maxLength: PropTypes.number,
  formErrorCheck: PropTypes.func
}

export default TextInput;
