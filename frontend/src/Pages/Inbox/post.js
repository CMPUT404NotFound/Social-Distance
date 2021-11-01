import React from "react";
import { Row, Col, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
// import { Link } from "react-router-dom";

const InboxPost = ({ post }) => {
	return (
		<Row align="middle" gutter={[16, 16]} className="post_container">
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
			</Col>
		</Row>
	);
};

export default InboxPost;
