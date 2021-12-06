import { useState, useContext } from "react";
import "./profile.css";
import axios from "axios";
import UserContext from "../../userContext";
import { Alert, Button, Form, Input, Modal } from "antd";

const EditProfile = ({ visible, setVisible }) => {
	const { setUser, user } = useContext(UserContext);

	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");

	let url = `https://project-api-404.herokuapp.com/api/author/${user.uuid}/`;

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	// Edit the user's profile
	const onFinish = (values) => {
		setLoading(true);

		const data = {
			id: user.url + "/",
			github: values.github || user.github,
			displayName: values.displayName || user.displayName,
			profileImage: values.profileImage || user.profileImage,
		};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);

				setUser({
					...user,
					github: values.github || user.github,
					displayName: values.displayName || user.displayName,
					profileImage: values.profileImage || user.profileImage,
				});

				setVisible(false);
			})
			.catch(function () {
				setError("The profile information you used is invalid. Please check and try again.");
				setLoading(false);
			});
	};

	const onFinishFailed = (errorInfo) => {
		console.log("Failed:", errorInfo);
		setError("An error occurred. Please check that you filled in the form correctly.");
	};

	return (
		<Modal
			title="Edit Profile"
			visible={visible}
			onCancel={() => {
				setVisible(false);
			}}
			footer={null}
		>
			{error && (
				<Alert
					message="Error"
					// description="Either your username or your password is incorrect. Please try again or contact the server administrator."
					description={error}
					type="error"
					className="error"
					showIcon
				/>
			)}

			<Form
				name="signup"
				initialValues={{
					github: user.github,
					profileImage: user.profileImage,
					displayName: user.displayName,
				}}
				onFinish={onFinish}
				onFinishFailed={onFinishFailed}
				autoComplete="off"
			>
				<Form.Item
					label="Github URL"
					name="github"
					rules={[{ type: "url", message: "Github is not a valid URL!" }]}
				>
					<Input placeholder="eg. https://github.com/adalovelace" />
				</Form.Item>

				<Form.Item label="Display Name" name="displayName" rules={[]}>
					<Input placeholder="eg. Ada Lovelace" />
				</Form.Item>

				<Form.Item
					label="Profile Image URL"
					name="profileImage"
					rules={[{ type: "url", message: "Profile Image is not a valid URL!" }]}
				>
					<Input placeholder="eg. https://images.com/adalovelace.png" />
				</Form.Item>

				<Form.Item wrapperCol={{ offset: 10, span: 16 }}>
					<Button type="primary" htmlType="submit" loading={loading}>
						Submit
					</Button>
				</Form.Item>
			</Form>
		</Modal>
	);
};

export default EditProfile;
