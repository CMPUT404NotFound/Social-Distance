import { useState, useEffect } from "react";
import "./inbox.css";
import axios from "axios";
import Post from "./post";

const Inbox = ({ user }) => {
	const [posts, setPosts] = useState([]);

	useEffect(() => {
		// TODO: Remove temporary user id
		const url = `https://project-api-404.herokuapp.com/api/author/${
			user ? user.id : "dc9548ca-801c-4bed-b610-7e9d6e2fb8e0"
		}/posts/`;

		const data = {};

		let config = {};

		axios
			.get(url, data, config)
			.then(function (response) {
				console.log(response);
				setPosts(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user]);

	return (
		<div className="inbox_page">
			{posts.map((post) => (
				<Post post={post} />
			))}
		</div>
	);
};

export default Inbox;
