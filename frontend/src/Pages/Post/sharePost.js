import React, { useState, useContext } from "react";
import { Button, Radio, Alert, Divider, Modal } from "antd";
import { SendOutlined } from "@ant-design/icons";
import axios from "axios";
import UserContext from "../../userContext";

let ReactCommonmark = require("react-commonmark");

// Main Create Post Page
const SharePost = ({ visible, setVisible, post }) => {
	const { user } = useContext(UserContext);

	// post visibility
	const [visibility, setVisibility] = useState("PUBLIC");

	// post data

	//TODO: make this route to the author's profile
	const content = `[${post.author.displayName}](${post.author.url}):\n>` + post.content;
	const title = "FWD: " + post.title;
	const description = post.description;
	const contentType = "text/markdown";
	const source = post.author.url;
	const origin = post.source || post.author.url;

	// post state
	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);

	const url = `https://project-api-404.herokuapp.com/api/author/${user.uuid}/posts/`;

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
			source,
			origin,
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

	const handleSubmit = () => {
		setError("");
		setLoading(true);
		if (content) submitPost();
		else {
			setError("You must have post content");
			setLoading(false);
		}
	};

	const visibilityOptions = [{ value: "FRIENDS", label: "Friends Only" }];

	if (post.visibility === "PUBLIC") {
		visibilityOptions.push({ value: "PUBLIC", label: "Public" });
	}

	return (
		<Modal
			title="Share Post"
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

			{/* Text Preview */}
			<Divider>Preview</Divider>
			<p>
				<strong>Title: </strong>
				{title}
			</p>

			<p>
				<strong>Description: </strong>
				{description}
			</p>
			<ReactCommonmark className="preview" source={content} />

			{/* Visibility */}
			<Divider>Visibility Settings</Divider>
			<Radio.Group
				onChange={(e) => {
					setVisibility(e.target.value);
				}}
				value={visibility}
				options={visibilityOptions}
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
				Share Post
			</Button>
		</Modal>
	);
};

export default SharePost;
