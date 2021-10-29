import React, { useState } from "react";
import { Route, Switch } from "react-router";
import Login from "./Pages/Login/login";
import CreatePost from "./Pages/Create/create";
import Inbox from "./Pages/Inbox/inbox";
import Signup from "./Pages/Signup/signup";
import Error404 from "./Error/error404";

const Routes = () => {
	const [loggedIn, setLoggedIn] = useState(false);

	if (loggedIn) {
		return (
			<Switch>
				<Route exact path="/">
					<Inbox setLoggedIn={setLoggedIn} />
					<Route path="/CreatePost" component={CreatePost} />
				</Route>
				<Route component={Error404} />
			</Switch>
		);
	} else {
		return (
			<Switch>
				<Route exact path="/signup">
					<Signup setLoggedIn={setLoggedIn} />
				</Route>
				<Route exact path="/login">
					<Login />
				</Route>
				<Route exact path="/">
					<Login />
				</Route>
				<Route component={Error404} />
			</Switch>
		);
	}
};

export default Routes;
