import React, { useContext, useEffect, useState } from "react";
// eslint-disable-next-line
import { Row, Col, Avatar, Comment, Button, Tooltip } from "antd";
import {
	UserOutlined,
	LikeOutlined,
	DeleteOutlined,
	EditOutlined,
	ShareAltOutlined,
} from "@ant-design/icons";
import { Link } from "react-router-dom";
import ReactCommonmark from "react-commonmark";
import { useLocation } from "react-router";
import "./post.css";
import Like from "./like";
import PostComment from "./comment";
import axios from "axios";
import UserContext from "../../userContext";
import { getURLID } from "../../utils";
import DeletePost from "./deletePost";
import EditPost from "./editPost";
import SharePost from "./sharePost";

const Post = () => {
	const location = useLocation();
	const post = location.state;

	const { user } = useContext(UserContext);

	const [comments, setComments] = useState([]);
	const [self, setSelf] = useState(false); // whether the author is us

	// Modal Visibilities
	const [editModalVisible, setEditModalVisible] = useState(false);
	const [deleteModalVisible, setDeleteModalVisible] = useState(false);
	const [shareModalVisible, setShareModalVisible] = useState(false);

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
		const url = `https://project-api-404.herokuapp.com/api/author/${
			user.uuid
		}/likes/comments/${getURLID(comment.id)}/`;

		const data = {
			type: "Like",
			summary: `${user.displayName} likes your comment`,
			author: user,
			object: comment,
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

	// Get list of people who liked the comment
	// eslint-disable-next-line
	const getCommentLikes = (comment) => {
		let url = comment.url;
		if (url.slice(-1) === "/") url += "likes/";
		else url += "/likes/";

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
		if (post.author.id === user.id) setSelf(true);
		// eslint-disable-next-line
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
						{post.contentType === "image/png;base64" || post.contentType === "image/jpeg;base64" ? (
							<img
								src={
									post.content.includes(post.contentType)
										? post.content
										: "data:" + post.contentType + "," + post.content
								}
								className="post_content"
								alt={post.description}
							/>
						) : post.contentType === "text/markdown" ? (
							<ReactCommonmark source={post.content} className="post_content" />
						) : (
							<p>{post.content}</p>
						)}
					</Col>
				</Row>
				<Row justify="end">
					{self ? (
						/* Delete and Edit Buttons */
						<>
							<Tooltip title="Delete">
								<Button
									type="primary"
									shape="circle"
									icon={<DeleteOutlined />}
									onClick={() => {
										setDeleteModalVisible(true);
									}}
									danger
								/>
							</Tooltip>

							{/* Only be able to edit if it's not a reshared post */}
							{post.origin === post.id && (
								<Tooltip key="comment-basic-like" title="Edit">
									<Button
										type="primary"
										shape="circle"
										icon={<EditOutlined />}
										style={{ marginLeft: "1rem" }}
										onClick={() => {
											setEditModalVisible(true);
										}}
									/>
								</Tooltip>
							)}
						</>
					) : (
						/* Share Button */
						<Button
							type="primary"
							shape="circle"
							icon={<ShareAltOutlined />}
							onClick={() => {
								setShareModalVisible(true);
							}}
						/>
					)}
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

			{/* Delete Modal */}
			<DeletePost visible={deleteModalVisible} setVisible={setDeleteModalVisible} post={post} />

			{/* Edit Modal */}
			<EditPost visible={editModalVisible} setVisible={setEditModalVisible} post={post} />

			{/* Share Modal */}
			<SharePost visible={shareModalVisible} setVisible={setShareModalVisible} post={post} />
		</div>
	);
};

export default Post;
