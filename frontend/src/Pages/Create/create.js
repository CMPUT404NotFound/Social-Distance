import React, { useState, useContext } from "react";
import { Row, Col, Button, Radio, Space, Checkbox, Tabs, Input, Alert } from "antd";
import { SendOutlined } from "@ant-design/icons";
import TextArea from "rc-textarea";
import "./create.css";
import axios from "axios";
import history from "./../../history";
import UserContext from "../../userContext";

const { TabPane } = Tabs;
let ReactCommonmark = require("react-commonmark");

// Main Create Post Page
const CreatePost = () => {
	const { user } = useContext(UserContext);

	const [content, setContent] = useState("");
	const [title, setTitle] = useState("");
	const [description, setDescription] = useState("");
	const [visibility, setVisibility] = useState("PUBLIC");
	const [image, setImage] = useState(null);
	const [error, setError] = useState("");

	const submitPost = () => {
		const url = `https://project-api-404.herokuapp.com/api/author/${user.id}/posts/`;

		const data = {
			title,
			content,
			visibility,
			description,
			contentType: "text/plain",
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

				// redirect to inbox
				history.push("inbox");
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	const submitImage = () => {
		const url = `https://project-api-404.herokuapp.com/api/author/${user.id}/posts/`;

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

				// redirect to inbox
				history.push("inbox");
			})
			.catch(function (error) {
				console.log(error);
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
		if (content) submitPost();
		if (image) submitImage();
		if (!content && !image) setError("You must have post content and/or an image");
	};

	return (
		<div className="create_page">
			<Row justify="center">
				<Col className="title" type="flex" align="middle">
					<h1>Create a Post</h1>
				</Col>
			</Row>

			<Row justify="center" className="editor">
				{error && (
					<Alert message="Error" description={error} type="error" className="error" showIcon />
				)}

				<Col flex={1} type="flex" align="middle">
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
				</Col>

				<Col className="options">
					<Space direction="vertical">
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

						{/* Image Upload */}
						{/* <Uploader /> */}
						<input type="file" accept="image/png" name="image" onChange={handleImage} />

						{/* Visibility */}
						<h2>Share your post to: </h2>
						<Radio.Group
							onChange={(e) => {
								setVisibility(e.target.value);
							}}
							value={visibility}
						>
							<Space direction="vertical">
								<Radio value="PUBLIC">Public</Radio>
								<Radio value="FRIENDS">Friends Only</Radio>
								<Radio value="SPECIFIC AUTHORS">
									<Space direction="vertical">
										Specific Authors Only
										{visibility === "SPECIFIC AUTHORS" ? (
											<Checkbox.Group options={friends} />
										) : null}
									</Space>
								</Radio>
								<Radio value="UNLISTED">Unlisted</Radio>
							</Space>
						</Radio.Group>

						{/* Submit Button */}
						<Button type="primary" shape="round" icon={<SendOutlined />} onClick={handleSubmit}>
							Send Post
						</Button>
					</Space>
				</Col>
			</Row>
		</div>
	);
};

export default CreatePost;
