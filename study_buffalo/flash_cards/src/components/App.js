import React from "react";
import ReactDOM from "react-dom";

class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {isVisible: false}

    this.handleMenuClick = this.handleMenuClick.bind(this)
  }

  handleMenuClick(e) {
    if (e.target.id==="menu-icon") {
      this.setState({isVisible: true});
    } else if (e.target.id==="menu-close-button" || e.target.id==="menu-overlay") {
      this.setState({isVisible: false});
    }
  }

  render() {
    return (
      <div>
        <button id="menu-icon" onClick={this.handleMenuClick}>Menu</button>
        <div id="side-menu" className={this.state.isVisible ? "visible" : ""}>
          <div id="menu-close-div">
            <button id="menu-close-button" onClick={this.handleMenuClick}>x</button>
          </div>
          <ul id="menu-items">
            <li>Dashboard</li>
            <li>Create &amp; Manage Cards</li>
            <li>Create &amp; Manage Decks</li>
            <li>Study Buffalo Home</li>
            <li>Logout</li>
          </ul>
        </div>
        <div id="menu-overlay" className={this.state.isVisible ? "visible" : ""} onClick={this.handleMenuClick} aria-hidden="true" >&nbsp;</div>
      </div>
    );
  }
}

function ListDisplay(prop) {
  const items = prop.items
  const listItems = items.map((item, index) =>
    <li key={item} data-id={index}>{item}</li>
  )

  return (
    <ul>{listItems}</ul>
  )
}

function App(prop) {
  return (
    <div>
      <Menu />
      <h1>Welcome {prop.name}!</h1>
      <ListDisplay items={[1,2,3]} />
    </div>
  )
}

ReactDOM.render(
  <App name="Josh" />,
  document.getElementById('root')
);
