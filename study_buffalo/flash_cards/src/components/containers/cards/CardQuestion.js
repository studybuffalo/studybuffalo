import React from "react";

import ContentPart from "./ContentPart";

class CardQuestion extends React.Component {
  constructor(props) {
    super(props);

    // TODO:
    //  State needs to record number of question parts, order, type
    //  This can be passed as param to ContentPart
    this.state = {
      parts: []
    }

    this.addText = this.addText.bind(this);
  }

  addText(e) {
    e.preventDefault();

    this.setState({
      parts: [
        ...this.state.parts,
        {
          type: "text",
          order: this.state.parts.length + 1
        }
      ]
    })
  }

  render() {
    let questionParts = this.state.parts.map((part) => {
      return <ContentPart key={part.order} type={part.type} />
    })

    return (
      <div id="question">
        <div id="question-parts">
          {questionParts}
        </div>
        <button onClick={this.addText}>Add text</button>
        <button>Add media</button>
      </div>
    );
  }
}

export default CardQuestion;
