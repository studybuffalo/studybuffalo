import React from "react";
import PropTypes from 'prop-types';

class TextInput extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      valid: true,
      error_messages: []
    }

    this.handleTextChange = this.handleTextChange.bind(this);
  }

  handleTextChange(e) {
    const input = e.target;
    let errorMessages = [];

    if (this.props.required && input.value.length === 0) {
      errorMessages.push("This field is required.");
    } else if (this.props.max_length && input.value.length > this.props.max_length) {
      errorMessages.push(
        "This field must be "
        + this.props.max_length
        + this.props.max_length === 1 ? (
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


  // Disable submit until data in each field (onKeyUp)
  // onBlur validate the entered text

  render() {
    return (
      <div className={this.state.valid ? "" : "errors"}>
        <label htmlFor={this.props.id}>
          {this.props.label_text}
          {
            this.props.type.toLowerCase() === "text" ? (
              <input type="text" id={this.props.id} onChange={this.handleTextChange} />
            ) : (
              <textarea id={this.props.id} onChange={this.handleTextChange} />
            )
          }
        </label>
        <span className="errors">{this.state.error_messages.join(" ")}</span>
      </div>
    )
  }
}

TextInput.defaultProps = {
  type: "text",
  label_text: "",
  required: false,
  max_length: 0
}

TextInput.propTypes = {
  id: PropTypes.string.isRequired,
  type: PropTypes.string,
  label_text: PropTypes.string,
  required: PropTypes.bool,
  max_length: PropTypes.number
}

export default TextInput;
