import React from "react";
import PropTypes from 'prop-types';


class ContentPart extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
    }
  }

  render() {
    return (
      <div>
        {
          this.props.type === "text" ?
          (
            <div className="text-area" contentEditable />
          ) : (
            <div className="media-area" />
          )
        }
        <button>Remove</button>
      </div>
    );
  }
}

ContentPart.defaultProps = {
  type: "text"
}

ContentPart.propTypes = {
  type: PropTypes.oneOf(["text", "media"])
}

export default ContentPart;
