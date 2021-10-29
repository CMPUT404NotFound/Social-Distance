import React, { useState } from "react";
import { Route, Switch } from "react-router";
import Login from "./Pages/Login/login";
import Inbox from "./Pages/Inbox/inbox";

const Routes = () => {
	const [loggedIn, setLoggedIn] = useState(false);

	if (loggedIn) {
		return (
			<Switch>
				<Route exact path="/" component={Inbox} />
			</Switch>
		);
	} else {
		return (
			<Switch>
				<Route exact path="/" component={Login} />
			</Switch>
		);
	}
};

export default Routes;
