import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route, NavLink } from 'react-router-dom'

// TODO: Remove eslint rule for Link component when next ESLint edition released

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
      <div>
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

function Dashboard() {
  return (
    <React.Fragment>
      <h1>Study Buffalo Flashcards</h1>
      <DashboardNews />
    </React.Fragment>
  )
}

function DashboardNews() {
  return (
    <div>News &amp; Announcements</div>
  )
}

function Decks() {
  return (
    <Switch>
      <Route exact path="/flash-cards/decks/" component={DecksDashboard} />
      <Route exact path="/flash-cards/decks/create/" component={DecksCreate} />
    </Switch>
  )
}

function DecksDashboard() {
  return (
    <h1>Flash Card Decks</h1>
  )
}

function DecksCreate() {
  return (
    <h1>Create new deck</h1>
  )
}

function Cards() {
  return (
    <h1>Flash Card Management</h1>
  )
}
function Main() {
  return (
    <Switch>
      <Route exact path="/flash-cards/" component={Dashboard} />
      <Route path="/flash-cards/decks/" component={Decks} />
      <Route path="/flash-cards/cards/" component={Cards} />
    </Switch>
  )
}

function App() {
  return (
    <React.Fragment>
      <Menu />
      <Main />
    </React.Fragment>
  )
}

ReactDOM.render(
  (
    <BrowserRouter>
      <App name="Josh" />
    </BrowserRouter>
  ),
  document.getElementById('app')
);
