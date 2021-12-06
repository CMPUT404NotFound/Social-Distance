import React, { useState, useContext } from "react";
import { Button, Radio, Space, Checkbox, Tabs, Input, Alert, Divider } from "antd";
import { SendOutlined } from "@ant-design/icons";
import TextArea from "rc-textarea";
import "./create.css";
import axios from "axios";
import UserContext from "../../userContext";

const { TabPane } = Tabs;
let ReactCommonmark = require("react-commonmark");

// Main Create Post Page
const EditPost = ({ setVisible, post }) => {
	const { user } = useContext(UserContext);

	const [content, setContent] = useState(post.content);
	const [title, setTitle] = useState(post.title);
	const [description, setDescription] = useState(post.description);
	const [visibility, setVisibility] = useState(post.visibility);
	const [image, setImage] = useState(null);
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
			title,
			content,
			visibility,
			description,
			contentType: "text/plain",
			unlisted: visibility === "UNLISTED",
		};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);

				// close the modal
				cancel();
			})
			.catch(function (error) {
				console.log(error);
				setError("There was an error sharing your post. Please try again later.");
				setLoading(false);
			});
	};

	const submitImage = () => {
		const data = {
			title,
			content: image,
			visibility,
			description,
			contentType: "image/png;base64",
		};

		const config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);

				// close the modal
				cancel();
			})
			.catch(function (error) {
				console.log(error);
				setError("There was an error sharing your post. Please try again later.");
				setLoading(false);
			});
	};

	const getBase64 = (file) => {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = () => resolve(reader.result);
			reader.onerror = (error) => reject(error);
		});
	};

	const handleImage = async (event) => {
		const imageFile = await getBase64(event.target.files[0]);
		setImage(imageFile);
		console.log(imageFile);
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
		if (image) submitImage();
		if (!content && !image) {
			setError("You must have post content and/or an image");
			setLoading(false);
		}
	};

	return (
		<div className="create_page">
			{error && (
				<Alert message="Error" description={error} type="error" className="error" showIcon />
			)}

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

			{/* Image Upload */}
			<Divider>Upload Image</Divider>
			<input type="file" accept="image/png" name="image" onChange={handleImage} />

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
		</div>
	);
};

export default EditPost;
