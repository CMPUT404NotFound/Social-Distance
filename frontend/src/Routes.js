import React, { useState } from "react";
import { Route, Switch } from "react-router";

// Get Pages
import Login from "./Pages/Login/login";
import CreatePost from "./Pages/Create/create";
import Main from "./Pages/Main/main";
import Inbox from "./Pages/Inbox/inbox";
import Signup from "./Pages/Signup/signup";
import Notifications from "./Pages/Notifications/notifications";
import Explore from "./Pages/Explore/explore";

// Get Error Pages
import Error404 from "./Error/error404";

const Routes = () => {
	const [loggedIn, setLoggedIn] = useState(false);
	const [user, setUser] = useState(null);

	if (loggedIn) {
		return (
			<Switch>
				<Route exact path="/createpost">
					<CreatePost setLoggedIn={setLoggedIn} user={user} />
				</Route>
				<Route exact path="/inbox">
					<Main>
						<Inbox setLoggedIn={setLoggedIn} user={user} />
					</Main>
				</Route>
				<Route exact path="/notifications">
					<Main>
						<Notifications setLoggedIn={setLoggedIn} user={user} />
					</Main>
				</Route>
				<Route exact path="/explore">
					<Main>
						<Explore setLoggedIn={setLoggedIn} user={user} />
					</Main>
				</Route>
				<Route exact path="/">
					<Main>
						<Inbox setLoggedIn={setLoggedIn} user={user} />
					</Main>
				</Route>
				<Route component={Error404} />
			</Switch>
		);
	} else {
		return (
			<Switch>
				<Route exact path="/signup">
					<Signup setLoggedIn={setLoggedIn} setUser={setUser} />
				</Route>
				<Route exact path="/login">
					<Login setLoggedIn={setLoggedIn} setUser={setUser} />
				</Route>
				<Route exact path="/">
					<Login setLoggedIn={setLoggedIn} setUser={setUser} />
				</Route>
				<Route component={Error404} />
			</Switch>
		);
	}
};

export default Routes;
