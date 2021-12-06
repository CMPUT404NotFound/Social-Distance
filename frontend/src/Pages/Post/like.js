import { LikeOutlined } from "@ant-design/icons";
import { useContext, useState, useEffect, useCallback } from "react";
import { Button, Tooltip, Popover } from "antd";
import UserContext from "../../userContext";
import axios from "axios";
import { Link } from "react-router-dom";
import { getURLID } from "../../utils";

const Like = ({ post }) => {
	const { user } = useContext(UserContext);
	const [likes, setLikes] = useState([]);

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	// Get list of people who liked the post
	const getLikes = useCallback(() => {
		const url = `https://project-api-404.herokuapp.com/api/author/${getURLID(
			post.author.id
		)}/posts/${getURLID(post.post_id || post.id)}/likes/`;
		// const url = `${post.post_id}/likes/`;

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);

				setLikes(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});
		// eslint-disable-next-line
	}, [post.id, user.token]);

	// Like the post
	const like = () => {
		// Post to own likes
		const url = `https://project-api-404.herokuapp.com/api/author/${
			user.uuid
		}/likes/posts/${getURLID(post.post_id || post.id)}/`;

		const data = {
			type: "Like",
			summary: `${user.displayName} likes your post`,
			author: user,
			object: post.url,
		};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	useEffect(() => {
		getLikes();
	}, [getLikes]);

	const content = (
		<div>
			{likes &&
				likes.map &&
				likes.map((like, i) => (
					<Link to={{ pathname: "/profile", state: like.author }} key={i}>
						{like.author.displayName}
					</Link>
				))}
		</div>
	);

	return (
		<Tooltip title={"Like"} placement="bottom">
			<Button
				shape="circle"
				icon={<LikeOutlined />}
				danger
				onClick={like}
				style={{ marginLeft: "1rem" }}
			/>
			<Popover title="Likes" trigger="hover" content={content}>
				<span style={{ marginLeft: "0.5rem" }}>{likes.length} likes</span>
			</Popover>
		</Tooltip>
	);
};

export default Like;