import React, { useContext, useEffect, useState } from "react";
// eslint-disable-next-line
import { Row, Col, Avatar, Comment, Button, Tooltip, Popover } from "antd";
import { UserOutlined, LikeOutlined } from "@ant-design/icons";
import { Link } from "react-router-dom";
import ReactCommonmark from "react-commonmark";
import { useLocation } from "react-router";
import "./post.css";
import Share from "./share";
import Like from "./like";
import PostComment from "./comment";
import axios from "axios";
import UserContext from "../../userContext";

const Post = () => {
	const location = useLocation();
	const post = location.state;

	const { user } = useContext(UserContext);

	const [comments, setComments] = useState([]);

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	// Get all the comments
	const getComments = (comment) => {
		// Send to comment author's inbox
		const url = post.comments;

		axios
			.get(url, config)
			.then(function (response) {
				setComments(response.data.comments);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	// like a comment
	const likeComment = (comment) => {
		// Send to comment author's inbox
		const url = `${comment.author.url}/inbox/`;

		const data = {
			type: "Like",
			summary: `${user.displayName} likes your comment`,
			author: user,
			object: comment.id,
		};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response.data.comments);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	// Get list of people who liked the comment
	// eslint-disable-next-line
	const getCommentLikes = (comment) => {
		const url = `${comment.url}/likes/`;

		const config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				return response.data;
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	useEffect(() => {
		getComments();
	}, []);

	return (
		<div className="post_page">
			{/* Display post */}
			<div className="post_container">
				<Row align="top" gutter={[16, 16]} wrap={false}>
					<Col>
						{post.author.profileImage ? (
							<Avatar src={post.author.profileImage} size={64} />
						) : (
							<Avatar icon={<UserOutlined />} size={64} />
						)}
					</Col>
					<Col>
						<Link to={{ pathname: "/profile", state: post.author }}>{post.author.displayName}</Link>
						<h3>{post.title}</h3>
						<p className="post_description">{post.description}</p>
						<ReactCommonmark source={post.content} className="post_description" />
					</Col>
				</Row>
				<Row justify="end">
					{/* Share Button */}
					<Share post={post} />
					{/* Like Button */}
					<Like post={post} />
				</Row>
			</div>

			{/* Display option to comment */}
			<PostComment post={post} />

			{/* Display comments */}
			{comments &&
				comments.map((comment, i) => (
					<Comment
						className="comment_container"
						author={comment.author.displayName}
						avatar={
							comment.author.profileImage ? (
								<Avatar src={comment.author.profileImage} size={64} />
							) : (
								<Avatar icon={<UserOutlined />} size={64} />
							)
						}
						content={
							<>
								{comment.comment}
								<Tooltip key="comment-basic-like" title="Like">
									<Button
										shape="circle"
										icon={<LikeOutlined />}
										danger
										onClick={() => {
											likeComment(comment);
										}}
										style={{ display: "block", marginLeft: "auto" }}
									/>
								</Tooltip>
							</>
						}
						key={i}
					/>
				))}
		</div>
	);
};

export default Post;
