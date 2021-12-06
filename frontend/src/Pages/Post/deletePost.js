import { useContext } from "react";
import axios from "axios";
import UserContext from "../../userContext";
import { Modal } from "antd";
import { ExclamationCircleOutlined } from "@ant-design/icons";
import history from "./../../history";

const DeletePost = ({ visible, setVisible, post }) => {
	const { user } = useContext(UserContext);

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	const deletePost = () => {
		axios
			.delete(post.id, config)
			.then(function (response) {
				console.log(response);
				setVisible(false);
				history.push("");
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	return (
		<Modal
			title="Delete Post"
			visible={visible}
			onCancel={() => {
				setVisible(false);
			}}
			okText="Delete Post"
			okButtonProps={{ danger: true }}
			icon={<ExclamationCircleOutlined />}
			onOk={deletePost}
		>
			Are you sure you would like to delete this post?
		</Modal>
	);
};

export default DeletePost;
