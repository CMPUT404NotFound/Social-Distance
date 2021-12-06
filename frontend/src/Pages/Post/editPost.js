import React, { useState, useContext } from "react";
import { Button, Radio, Space, Checkbox, Tabs, Input, Alert, Divider, Modal } from "antd";
import { SendOutlined } from "@ant-design/icons";
import TextArea from "rc-textarea";
import axios from "axios";
import UserContext from "../../userContext";

const { TabPane } = Tabs;
let ReactCommonmark = require("react-commonmark");

// Main Create Post Page
const EditPost = ({ visible, setVisible, post }) => {
	const { user } = useContext(UserContext);

	// post type
	const [contentType, setContentType] = useState(post.contentType);

	// post data
	const [content, setContent] = useState(post.content);
	const [title, setTitle] = useState(post.title);
	const [description, setDescription] = useState(post.description);
	const [visibility, setVisibility] = useState(post.visibility);

	// post state
	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);

	const url = post.id;

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	const submitPost = () => {
		const data = {
			id: post.id,
			title,
			content,
			visibility,
			description,
			contentType,
			unlisted: visibility === "UNLISTED",
		};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);

				// close the modal
				setVisible(false);
			})
			.catch(function (error) {
				console.log(error);
				setError("There was an error sharing your post. Please try again later.");
				setLoading(false);
			});
	};

	const friends = [
		{ label: "Lee Seokmin", value: "dokyeom" },
		{ label: "Joshua Hong", value: "joshua" },
		{ label: "Wen Junhui", value: "jun" },
	];

	const handleSubmit = () => {
		setError("");
		setLoading(true);
		if (content) submitPost();
		else {
			setError("You must have post content");
			setLoading(false);
		}
	};

	const contentTypes = [
		{ label: "Plain Text", value: "text/plain" },
		{ label: "Markdown Text", value: "text/markdown" },
	];

	return (
		<Modal
			title="Edit Post"
			visible={visible}
			onCancel={() => {
				setVisible(false);
			}}
			footer={null}
			className="edit_post_modal"
		>
			{/* Error Heading */}
			{error && (
				<Alert message="Error" description={error} type="error" className="error" showIcon />
			)}

			{/* Post data */}
			<label>Title</label>
			<Input
				placeholder="Post Title"
				allowClear
				onChange={(e) => {
					setTitle(e.target.value);
				}}
				value={title}
			/>

			<label>Description</label>
			<Input.TextArea
				placeholder="Post Description"
				allowClear
				onChange={(e) => {
					setDescription(e.target.value);
				}}
				value={description}
				showCount
			/>

			<Tabs defaultActiveKey="1" centered className="tabs">
				<TabPane tab="Edit Text" key="1">
					{/* Edit Text */}
					<TextArea
						className="textfield"
						value={content}
						onChange={(e) => {
							setContent(e.target.value);
						}}
					></TextArea>
				</TabPane>
				<TabPane tab="Preview" key="2">
					{/* Text Preview */}
					<ReactCommonmark className="preview" source={content} />
				</TabPane>
			</Tabs>

			{/* Visibility */}
			<Divider>Visibility Settings</Divider>
			<Radio.Group
				onChange={(e) => {
					setVisibility(e.target.value);
				}}
				value={visibility}
			>
				<Space align="center" wrap>
					<Radio value="PUBLIC">Public</Radio>
					<Radio value="FRIENDS">Friends Only</Radio>
					<Radio value="SPECIFIC AUTHORS">
						<Space direction="vertical">
							Specific Authors Only
							{visibility === "SPECIFIC AUTHORS" ? <Checkbox.Group options={friends} /> : null}
						</Space>
					</Radio>
					<Radio value="UNLISTED">Unlisted</Radio>
				</Space>
			</Radio.Group>

			{/* Content Type */}
			<Divider>Text Type</Divider>
			<Radio.Group
				onChange={(e) => {
					setContentType(e.target.value);
				}}
				value={contentType}
				options={contentTypes}
			></Radio.Group>

			<Divider />

			{/* Submit Button */}
			<Button
				type="primary"
				icon={<SendOutlined />}
				onClick={handleSubmit}
				loading={loading}
				className="submitButton"
			>
				Send Post
			</Button>
		</Modal>
	);
};

export default EditPost;
