import React from "react";
import ReactDOM from "react-dom";

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
      <h1>Welcome {prop.name}</h1>
      <ListDisplay items={[1,2,3]} />
    </div>
  )
}

ReactDOM.render(
  <App name="Josh" />,
  document.getElementById('root')
);
