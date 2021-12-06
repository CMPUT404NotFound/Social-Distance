import { useState, useEffect, useContext } from "react";
import React from "react";
import { Row, Col, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
import axios from "axios";
import UserContext from "../../userContext";
import { Link } from "react-router-dom";

const InboxLike = ({ like }) => {
	const { user } = useContext(UserContext);

	const [post, setPost] = useState(null);

	useEffect(() => {
		const url = like.object;

		let config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setPost(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user, like]);

	return (
		<Row align="middle" gutter={[16, 16]} className="post_container">
			<Col>
				{like.author.profileImage ? (
					<Avatar src={like.author.profileImage} size={64} />
				) : (
					<Avatar icon={<UserOutlined />} size={64} />
				)}
			</Col>
			<Col>
				<p>{like.author.displayName} likes your post</p>
				{post !== null && (
					<Link to={{ pathname: "/post", state: post }}>
						{post.title || post.description ? (
							<>
								<h3>{post.title}</h3>
								<p className="post_description">{post.description}</p>
							</>
						) : (
							"Go to post"
						)}
					</Link>
				)}
			</Col>
		</Row>
	);
};

export default InboxLike;
