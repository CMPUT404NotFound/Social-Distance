import React from "react";
import { Row, Col, Upload, Button, message, Radio, Space, Checkbox, Tabs } from "antd";
import { UploadOutlined, SendOutlined } from "@ant-design/icons";
import TextArea from "rc-textarea";
import "./create.css";
import axios from "axios";
import history from "./../../history";

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

function onChange(checkedValues) {
	console.log("checked = ", checkedValues);
}

// example list of authors to send post to
const authors = [
	{ label: "Lee Seokmin", value: "dokyeom" },
	{ label: "Joshua Hong", value: "joshua" },
	{ label: "Wen Junhui", value: "jun" },
];

// For Radio selection of who to share post to
class ShareTo extends React.Component {
	state = {
		value: 1,
	};

	onChange = (e) => {
		console.log("radio checked", e.target.value);
		this.setState({
			value: e.target.value,
		});
	};

	render() {
		const { value } = this.state;
		return (
			<Radio.Group onChange={this.onChange} value={value}>
				<Space direction="vertical">
					<Radio value={1}>Public</Radio>
					<Radio value={2}>Friends Only</Radio>
					<Radio value={3}>
						<Space direction="vertical">
							Specific Authors Only
							{value === 3 ? <Checkbox.Group options={authors} onChange={onChange} /> : null}
						</Space>
					</Radio>
					<Radio value={4}>Unlisted</Radio>
				</Space>
			</Radio.Group>
		);
	}
}

// Main Create Post Page
export default class CreatePost extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			markdown: "# Type your heart out~",
		};
	}

	updateMarkdown(markdown) {
		this.setState({ markdown });
	}

	submitPost = () => {
		const url = "https://project-api-404.herokuapp.com/api/post";

		const data = {
			content: this.state.markdown,
		};

		let config = {};

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

	render() {
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
								<TextArea
									className="textfield"
									value={this.state.markdown}
									onChange={(e) => {
										this.updateMarkdown(e.target.value);
									}}
								></TextArea>
							</TabPane>
							<TabPane tab="Preview" key="2">
								<ReactCommonmark className="preview" source={this.state.markdown} />
							</TabPane>
						</Tabs>
					</Col>
					<Col className="options">
						<Space direction="vertical">
							<Uploader />
							<h2>Share your post to: </h2>
							<ShareTo />
							<Button
								type="primary"
								shape="round"
								icon={<SendOutlined />}
								onClick={this.submitPost}
							>
								Send Post
							</Button>
						</Space>
					</Col>
				</Row>
			</div>
		);
	}
}
