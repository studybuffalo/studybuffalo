import PropTypes from 'prop-types';
import React from "react";
import ReactModal from 'react-modal';


ReactModal.setAppElement("#app");

class ErrorModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      showModal: false
    }

    this.handleCloseModal = this.handleCloseModal.bind(this);
  }

  componentWillMount() {
    if (this.props.errors) {
      this.setState({showModal: true});
    } else {
      this.setState({showModal: false});
    }
  }

  handleCloseModal () {
    this.setState({showModal: false});
  }

  render() {
    return (
      <ReactModal
        isOpen={this.state.showModal}
        contentLabel="Error retrieving data"
        onRequestClose={this.handleCloseModal}
      >
        <div>
          {this.props.errors}
        </div>
        <button onClick={this.handleCloseModal}>Close Modal</button>
      </ReactModal>
    )
  }
}

ErrorModal.defaultProps = {
  errors: "",
}

ErrorModal.propTypes = {
  errors: PropTypes.string
}

export default ErrorModal;
