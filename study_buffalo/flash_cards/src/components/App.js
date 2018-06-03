import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom'

// TODO: Remove eslint rule for Link component when next ESLint edition released
class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {isVisible: false}

    this.handleMenuClick = this.handleMenuClick.bind(this)
  }

  handleMenuClick(e) {
    if (e.target.id==="menu-icon") {
      this.setState({isVisible: true});
    } else {
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
            <li><Link to="/flash-cards/" onClick={this.handleMenuClick}>Dashboard</Link></li>
            <li><Link to="/flash-cards/decks/" onClick={this.handleMenuClick}>Create &amp; Manage Decks</Link></li>
            <li><Link to="/flash-cards/cards/" onClick={this.handleMenuClick}>Create &amp; Manage Cards</Link></li>
            <li><a href="/">Study Buffalo Home</a></li>
            <li><a href="/accounts/logout/?next=/">Logout</a></li>
          </ul>
        </div>
        <div id="menu-overlay" className={this.state.isVisible ? "visible" : ""} onClick={this.handleMenuClick} aria-hidden="true" >&nbsp;</div>
      </div>
    );
  }
}

function Dashboard(prop) {
  return (
    <h1>Study Buffalo Flashcards</h1>
  )
}

function Decks(prop) {
  return (
    <Switch>
      <Route exact path="/flash-cards/decks/" component={DecksDashboard} />
      <Route exact path="/flash-cards/decks/create/" component={DecksCreate} />
    </Switch>
  )
}

function DecksDashboard(prop) {
  return (
    <h1>Flash Card Decks</h1>
  )
}

function DecksCreate(prop) {
  return (
    <h1>Create new deck</h1>
  )
}

function Cards(prop) {
  return (
    <h1>Flash Card Management</h1>
  )
}
function Main(prop) {
  return (
    <Switch>
      <Route exact path="/flash-cards/" component={Dashboard} />
      <Route path="/flash-cards/decks/" component={Decks} />
      <Route path="/flash-cards/cards/" component={Cards} />
    </Switch>
  )
}

// class Main extends React.Component {
//   constructor(props) {
//     super(props);
//   }

//   render() {
//     return (
//       <Switch>
//         <Route exact path="/" component={Dashboard} />
//         <Route exact path="/decks" component={Decks} />
//       </Switch>
//     )
//   }
// }
function App(prop) {
  return (
    <div>
      <Menu />
      <Main />
    </div>
  )
}

ReactDOM.render(
  (
    <BrowserRouter>
      <App name="Josh" />
    </BrowserRouter>
  ),
  document.getElementById('root')
);
