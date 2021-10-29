import React from "react";
import { Row, Col } from "antd";
import { UserOutlined, HeartOutlined, CommentOutlined, ShareAltOutlined } from "@ant-design/icons";
let ReactCommonmark = require("react-commonmark");

const Post = ({ post }) => {
	const sample_text = `# Spooky, scary skeletons
    ## send shivers down your spine
    `;
	const sample_author = "dokyeom";
	const sample_title = "This is a sample post";

	return (
		<div className="post_container">
			<Row justify="center">
				<Col span={10}>
					<UserOutlined />
					<p>{post ? post.author.displayName : sample_author}</p>
				</Col>
			</Row>
			<Row justify="center">
				<Col span={10}>
					<h3>{post ? post.title : sample_title}</h3>
					<ReactCommonmark source={post ? post.content : sample_text} />
				</Col>
			</Row>
			<Row justify="center">
				<Col span={10}>
					<HeartOutlined />
					<CommentOutlined />
					<ShareAltOutlined />
				</Col>
			</Row>
		</div>
	);
};

export default Post;
