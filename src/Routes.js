import React from "react";
import { Route, Switch } from "react-router";
import Login from "./Pages/Login/login";

const Routes = () => {
	return (
		<Switch>
			<Route exact path="/" component={Login} />
		</Switch>
	);
};

export default Routes;
