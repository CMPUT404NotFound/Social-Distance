import { useContext, useState, useEffect } from "react";

import UserContext from "../../userContext";
import axios from "axios";

const Notifications = () => {
	const { user } = useContext(UserContext);
	const [posts, setPosts] = useState(null);

	useEffect(() => {
		const url = `https://plurr.herokuapp.com/service/author/48409866-0811-4ad8-a1d9-29014b4d316d/posts/`;

		let config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
			auth: {
				username: "team23",
				password: "password",
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setPosts(response.data.items);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user]);

	return <div>Notification Page</div>;
};

export default Notifications;
