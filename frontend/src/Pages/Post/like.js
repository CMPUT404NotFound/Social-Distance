import { LikeOutlined } from "@ant-design/icons";
import { useContext, useState, useEffect } from "react";
import { Button, Tooltip, Popover } from "antd";
import UserContext from "../../userContext";
import axios from "axios";

const Like = ({ post }) => {
	const { user } = useContext(UserContext);
	const [likes, setLikes] = useState([]);

	useEffect(() => {
		getLikes();
	}, [likes]);

	// Get list of people who liked the post
	const getLikes = () => {
		const url = `${post.id}/likes/`;

		const config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);

				setLikes(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	// Like the post
	const like = () => {
		// Send to post author's inbox
		const url = `https://project-api-404.herokuapp.com/api/author/${post.author.id}/inbox/`;

		const config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		const data = {
			type: "Like",
			summary: `${user.displayName} likes your post`,
			author: user,
			object: post.id,
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

	const content = <div>{likes && likes.map((like, i) => <p>{like.author.displayName}</p>)}</div>;

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
