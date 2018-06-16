/* eslint react/no-multi-comp: 0 */
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route, NavLink, Link } from 'react-router-dom';

import DeckForm from './containers/deck/DeckForm';
import DecksDashboard from './containers/deck/DecksDashboard';


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

function Dashboard() {
  return (
    <React.Fragment>
      <h1>Study Buffalo Flash Cards</h1>
      <UnfinishedDecks />
      <DashboardNews />
      <div>
        Create and manage study decks
      </div>
      <div>
        Create and manage flash cards
      </div>
      <UserStats />
    </React.Fragment>
  )
}

function UnfinishedDecks() {
  return (
    <div>Unfinished decks</div>
  )
}

function DashboardNews() {
  return (
    <div>News &amp; Announcements</div>
  )
}

function UserStats() {
  return (
    <div>User stats</div>
  )
}

function Decks() {
  return (
    <Switch>
      <Route exact path="/flash-cards/decks/" component={DecksDashboard} />
      <Route exact path="/flash-cards/decks/create/" component={DecksCreate} />
      <Route exact path="/flash-cards/decks/:id/" component={DecksEdit} />
    </Switch>
  )
}

function DecksCreate() {
  return (
    <React.Fragment>
      <h1>Create new deck</h1>
      <DeckForm new />
    </React.Fragment>

  )
}

function DecksEdit() {
  return(
    <React.Fragment>
      <h1>Modify deck</h1>
      <Link to="/flash-cards/decks/">Back to deck list</Link>
      <DeckForm />
    </React.Fragment>
  )
}

function Cards() {
  return (
    <h1>Flash Card Management</h1>
  )
}

function Main() {
  return (
    <div id="main">
      <Switch>
        <Route exact path="/flash-cards/" component={Dashboard} />
        <Route path="/flash-cards/decks/" component={Decks} />
        <Route path="/flash-cards/cards/" component={Cards} />
      </Switch>
    </div>
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
