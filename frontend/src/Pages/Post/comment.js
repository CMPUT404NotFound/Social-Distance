import { useState, useContext } from "react";
import { Input, Button } from "antd";
import UserContext from "../../userContext";
import axios from "axios";
import { SendOutlined } from "@ant-design/icons";

const { TextArea } = Input;

const PostComment = ({ post }) => {
	const { user } = useContext(UserContext);

	const [comment, setComment] = useState("");

	// Get list of people who liked the post
	const sendComment = () => {
		const url = `${post.id}/comments`;

		const config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		const data = {
			type: "comment",
			author: user,
			comment,
			contentType: "text/plain",
		};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	return (
		<div className="comment_area">
			<TextArea
				placeholder="Comment..."
				allowClear
				value={comment}
				onChange={(e) => {
					setComment(e.target.value);
				}}
			/>
			<Button type="primary" icon={<SendOutlined />} onClick={sendComment} className="button">
				Comment
			</Button>
		</div>
	);
};

export default PostComment;
