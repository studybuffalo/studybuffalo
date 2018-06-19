import React from "react";

import DashboardNews from "./DashboardNews";
import UnfinishedDecks from "./UnfinishedDecks";
import UserStats from "./UserStats";

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

export default Dashboard;
