import React, { useState, useEffect } from "react";
import { Route, Switch, Redirect } from "react-router";

// Get Pages
import Login from "./Pages/Login/login";
import CreatePost from "./Pages/Create/create";
import Main from "./Pages/Main/main";
import Inbox from "./Pages/Inbox/inbox";
import Signup from "./Pages/Signup/signup";
import Feed from "./Pages/Feed/feed";
import Explore from "./Pages/Explore/explore";
import Post from "./Pages/Post/post";

// Get Error Pages
import Error404 from "./Error/error404";
import UserContext from "./userContext";
import Profile from "./Pages/Profile/profile";
import { getSessionStorage } from "./utils";

// User context tutorial resource
// https://www.youtube.com/watch?v=lhMKvyLRWo0
// https://medium.com/geekculture/how-to-use-context-api-and-jwt-to-maintain-user-sessions-eb5602e83a03

const Routes = () => {
	const [user, setUser] = useState(null);

	useEffect(() => {
		// get stored user from api
		const storedUser = getSessionStorage("user");
		if (storedUser) setUser(storedUser.value);
	}, []);

	return (
		<UserContext.Provider value={{ user, setUser }}>
			{user ? (
				// If the User is logged in
				<Switch>
					<Route exact path="/createpost">
						<CreatePost />
					</Route>
					<Route exact path="/inbox">
						<Main>
							<Inbox />
						</Main>
					</Route>
					<Route exact path="/explore">
						<Main>
							<Explore />
						</Main>
					</Route>
					<Route exact path="/post">
						<Main>
							<Post />
						</Main>
					</Route>
					<Route exact path="/profile">
						<Main>
							<Profile />
						</Main>
					</Route>
					<Route exact path="/">
						<Main>
							<Inbox />
						</Main>
					</Route>
					<Route component={Error404} />
				</Switch>
			) : (
				// If the User is not logged in
				<Switch>
					<Route exact path="/signup">
						<Signup />
					</Route>
					<Route exact path="/">
						<Login />
					</Route>
					<Redirect to="/" />
				</Switch>
			)}
		</UserContext.Provider>
	);
};

export default Routes;
