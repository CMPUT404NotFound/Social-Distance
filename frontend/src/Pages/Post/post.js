// import React, { createElement, useState } from "react";
import { Row, Col, Avatar, Comment } from "antd";
import { UserOutlined, HeartOutlined } from "@ant-design/icons";
// import { Link } from "react-router-dom";
import ReactCommonmark from "react-commonmark";
import { useLocation } from "react-router";
import "./post.css";

const Post = () => {
	const location = useLocation();
	const post = location.state;

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
						<p>{post.author.displayName}</p>
						<h3>{post.title}</h3>
						<p className="post_description">{post.description}</p>
						<ReactCommonmark source={post.content} className="post_description" />
					</Col>
				</Row>
				<Row justify="end">
					<HeartOutlined style={{ fontSize: "2rem" }} />
				</Row>
			</div>

			{/* Display comments */}
			{post.commentsSrc &&
				post.commentsSrc.comments &&
				post.commentsSrc.comments.map((comment, i) => (
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
						content={comment.comment}
						key={i}
					/>
				))}

			{/* Display option to comment */}
		</div>
	);
};

export default Post;
