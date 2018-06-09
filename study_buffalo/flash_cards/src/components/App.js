/* eslint react/no-multi-comp: 0 */
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route, NavLink, Link } from 'react-router-dom';

import DeckForm from './containers/DeckForm';
import DeckList from './containers/DeckList';


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

class DecksDashboard extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      owner: "",
      tags: [],
      text: ""
    };

    this.updateOwner = this.updateOwner.bind(this);
    this.updateTags = this.updateTags.bind(this);
    this.updateText = this.updateText.bind(this);
  }

  componentDidMount() {
    // Update the state to pass proper properties to list component
    this.updateOwner();
    this.updateTags();
    this.updateText();
  }

  updateOwner() {
    // Update the owner filter
    if (document.getElementById("owner-1").checked) {
      this.setState({owner: "owner"});
    } else if (document.getElementById("owner-2").checked) {
      this.setState({owner: "modified"});
    } else {
      this.setState({owner: ""});
    }
  }

  updateTags() {
    // Update the tag filter
    this.setState({tags: [document.getElementById("tag-search").value]});
  }

  updateText() {
    // Update the text filter
    this.setState({text: document.getElementById("deck-search").value});
  }

  render() {
    return (
      <React.Fragment>
        <h1>Flash Card Decks</h1>

        <Link to="/flash-cards/decks/create/" id="app-card">
          <span className="icon">+</span>
          <span>Create new deck</span>
        </Link>

        <h2>Modify an existing deck</h2>
        <div>
          <label htmlFor="owner-1">
            <input type="radio" name="owner" id="owner-1" value="owner" onChange={this.updateOwner} defaultChecked />
            Decks I created
          </label>
          <label htmlFor="owner-2">
            <input type="radio" name="owner" id="owner-2" value="modified" onChange={this.updateOwner} />
            Decks I have modified
          </label>
          <label htmlFor="owner-3">
            <input type="radio" name="owner" id="owner-3" value="" onChange={this.updateOwner} />
            All decks
          </label>
        </div>

        <div>
          <label htmlFor="tag-search">
            Tags:
            <input type="text" id="tag-search" onChange={this.updateTags} />
          </label>
        </div>

        <div>
          <label htmlFor="deck-search">
            Deck Name or Description:
            <input type="text" id="deck-search" onChange={this.updateText} />
          </label>
        </div>

        <DeckList owner={this.state.owner} tags={this.state.tags} text={this.state.text} />
      </React.Fragment>
    )
  }
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
