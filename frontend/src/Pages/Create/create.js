import React, { useState, useContext } from "react";
import { Row, Col, Upload, Button, message, Radio, Space, Checkbox, Tabs, Input } from "antd";
import { UploadOutlined, SendOutlined } from "@ant-design/icons";
import TextArea from "rc-textarea";
import "./create.css";
import axios from "axios";
import history from "./../../history";
import UserContext from "../../userContext";

const { TabPane } = Tabs;
let ReactCommonmark = require("react-commonmark");

// To verify only PNG files are uploaded
const Uploader = () => {
	const props = {
		beforeUpload: (file) => {
			if (file.type !== "image/png") {
				message.error(`${file.name} is not a png file`);
			}
			return file.type === "image/png" ? true : Upload.LIST_IGNORE;
		},
		onChange: (info) => {
			console.log(info.fileList);
		},
	};

	return (
		<Upload {...props}>
			<Button icon={<UploadOutlined />}>Upload PNGs only</Button>
		</Upload>
	);
};

// For Radio selection of who to share post to
// class ShareTo extends React.Component {
// 	state = {
// 		value: 1,
// 	};

// 	onChange = (e) => {
// 		console.log("radio checked", e.target.value);
// 		this.setState({
// 			value: e.target.value,
// 		});
// 	};

// 	render() {
// 		const { value } = this.state;
// 		return (
// 			<Radio.Group onChange={this.onChange} value={value}>
// 				<Space direction="vertical">
// 					<Radio value={"PUBLIC"}>Public</Radio>
// 					<Radio value={"FRIENDS"}>Friends Only</Radio>
// 					<Radio value={3}>
// 						<Space direction="vertical">
// 							Specific Authors Only
// 							{value === 3 ? <Checkbox.Group options={authors} onChange={onChange} /> : null}
// 						</Space>
// 					</Radio>
// 					<Radio value={4}>Unlisted</Radio>
// 				</Space>
// 			</Radio.Group>
// 		);
// 	}
// }

// Main Create Post Page
const CreatePost = () => {
	const { user } = useContext(UserContext);

	const [content, setContent] = useState("# Type your heart out~");
	const [title, setTitle] = useState("");
	const [description, setDescription] = useState("");
	const [visibility, setVisibility] = useState("PUBLIC");

	const submitPost = () => {
		const url = `https://project-api-404.herokuapp.com/api/author/${user.id}/posts/`;

		const data = {
			title,
			content,
			visibility,
			description,
			contentType: "text/plain",
		};

		axios
			.post(url, data)
			.then(function (response) {
				console.log(response);

				// redirect to inbox
				history.push("inbox");
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	const authors = [
		{ label: "Lee Seokmin", value: "dokyeom" },
		{ label: "Joshua Hong", value: "joshua" },
		{ label: "Wen Junhui", value: "jun" },
	];

	return (
		<div className="create_page">
			<Row justify="center">
				<Col className="title" type="flex" align="middle">
					<h1>Create a Post</h1>
				</Col>
			</Row>

			<Row justify="center" className="editor">
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
						<Uploader />

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
											<Checkbox.Group options={authors} />
										) : null}
									</Space>
								</Radio>
								<Radio value="UNLISTED">Unlisted</Radio>
							</Space>
						</Radio.Group>

						{/* Submit Button */}
						<Button type="primary" shape="round" icon={<SendOutlined />} onClick={submitPost}>
							Send Post
						</Button>
					</Space>
				</Col>
			</Row>
		</div>
	);
};

export default CreatePost;
