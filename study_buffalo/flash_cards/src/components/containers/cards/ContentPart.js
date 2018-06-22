import React from "react";


class ContentPart extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
    }
  }

  render() {
    return (
      <div>
        <div className="text-area" />
        or
        <div className="media-area" />
      </div>
    );
  }
}

export default ContentPart;
