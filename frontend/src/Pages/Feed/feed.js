import { useContext, useState, useEffect } from "react";

import UserContext from "../../userContext";
import axios from "axios";
import "./feed.css";
import InboxPost from "../Inbox/post";

import { Link } from "react-router-dom";

const Feed = () => {
	const { user } = useContext(UserContext);
	const [posts, setPosts] = useState([]);

	useEffect(() => {
		const url = `https://plurr.herokuapp.com/service/author/48409866-0811-4ad8-a1d9-29014b4d316d/posts/`;

		let config = {
			auth: {
				username: "team23",
				password: "password",
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setPosts((oldposts) => [...oldposts, ...response.data.items]);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user]);

	useEffect(() => {
		const url = `https://cmput404f21t17.herokuapp.com/service/connect/public/`;

		let config = {
			auth: {
				username: "1802fb2b-e473-4078-ace3-c205897accf7",
				password: "123456",
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setPosts((oldposts) => [...oldposts, ...response.data.items]);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user]);

	return (
		<div className="inbox_page">
			{posts &&
				posts.map((post, i) => (
					<Link to={{ pathname: "/post", state: post }} key={i}>
						<InboxPost post={post} key={i} />
					</Link>
				))}
		</div>
	);
};

export default Feed;
