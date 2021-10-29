import React from "react";
import { Route, Switch } from "react-router";
import Login from "./Pages/Login/login";
import CreatePost from "./Pages/Create/create";
import Inbox from "./Pages/Inbox/inbox";

const Routes = () => {
	return (
		<Switch>
			<Route exact path="/" component={Login} />
			<Route path="/CreatePost" component={CreatePost} />
			<Route path="/Inbox" component={Inbox} />
		</Switch>
	);
};

export default Routes;
