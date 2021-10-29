import React from "react";
import { Row, Col, Divider, Upload, Button, message, Radio, Space, Checkbox } from "antd";
import { UploadOutlined, SendOutlined } from "@ant-design/icons";
import TextArea from "rc-textarea";
import "./create.css";
import history from "./../../history";
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

	render() {
		return (
			<>
				<Row justify="center">
					<Col className="title" type="flex" align="middle">
						<h1>Create a Post</h1>
					</Col>
				</Row>
				<Row justify="center">
					<Col flex={1} type="flex" align="middle">
						<h2>Enter your text</h2>
						<TextArea
							className="textField"
							value={this.state.markdown}
							onChange={(e) => {
								this.updateMarkdown(e.target.value);
							}}
						></TextArea>
						<h2 className="uploadText">...or upload some images</h2>
						<Space>
							<Uploader />
						</Space>
					</Col>
					<Col flex={1}>
						<h2 type="flex" align="middle">
							Preview your post
						</h2>
						<ReactCommonmark source={this.state.markdown} />
						<Divider></Divider>
						<Space direction="vertical">
							<h2>Share your post to: </h2>
							<ShareTo />
							<Button
								type="primary"
								shape="round"
								icon={<SendOutlined />}
								onClick={() => history.push("/Inbox")}
							>
								Send Post
							</Button>
						</Space>
					</Col>
				</Row>
			</>
		);
	}
}
