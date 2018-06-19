import React from "react";
import { NavLink } from 'react-router-dom';

class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {isVisible: false}

    this.handleMenuClick = this.handleMenuClick.bind(this)
  }

  handleMenuClick(e) {
    if (e.target.id==="menu-icon" || e.target.parentElement.id==="menu-icon") {
      this.setState({isVisible: true});
    } else {
      this.setState({isVisible: false});
    }
  }

  render() {
    return (
      <div id="header">
        <button id="menu-icon" onClick={this.handleMenuClick}>
          <span className="icon">&#8801;</span>
          <span>Menu</span>
        </button>
        <div id="side-menu" className={this.state.isVisible ? "visible" : ""}>
          <div id="menu-close-div">
            <button id="menu-close-button" onClick={this.handleMenuClick}>x</button>
          </div>
          <ul id="menu-items">
            <li>
              <NavLink exact to="/flash-cards/" onClick={this.handleMenuClick} activeClassName="selected">
                Dashboard
              </NavLink>
            </li>
            <li>
              <NavLink to="/flash-cards/decks/" onClick={this.handleMenuClick} activeClassName="selected">
              Create &amp; Manage Decks
              </NavLink>
            </li>
            <li>
              <NavLink to="/flash-cards/cards/" onClick={this.handleMenuClick} activeClassName="selected">
              Create &amp; Manage Cards
              </NavLink>
            </li>
            <li><a href="/">Study Buffalo Home</a></li>
            <li><a href="/accounts/logout/?next=/">Logout</a></li>
          </ul>
        </div>
        <div id="menu-overlay" className={this.state.isVisible ? "visible" : ""} onClick={this.handleMenuClick} aria-hidden="true" >&nbsp;</div>
      </div>
    );
  }
}

export default Menu;
