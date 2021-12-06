import { useState, useContext } from "react";
import { Input, Button } from "antd";
import UserContext from "../../userContext";
import axios from "axios";
import { SendOutlined } from "@ant-design/icons";
import { getURLID } from "../../utils";

const { TextArea } = Input;

const PostComment = ({ post }) => {
	const { user } = useContext(UserContext);

	const [comment, setComment] = useState("");

	const sendComment = () => {
		const url = `https://project-api-404.herokuapp.com/api/author/${getURLID(
			post.author.id
		)}/posts/${getURLID(post.id)}/comments/`;

		const config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		const data = {
			type: "Comment",
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
