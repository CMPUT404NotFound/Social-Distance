import { Alert, Button, Checkbox, Form, Input } from "antd";
import axios from "axios";
import { useState, useContext } from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";
import history from "./../../history";
import "./signup.css";
import UserContext from "../../userContext";

const Signup = () => {
	// Inspired by AntD docs
	// https://ant.design/components/form/

	const { setUser } = useContext(UserContext);

	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);

	const onFinish = (values) => {
		setLoading(true);

		const url = "https://project-api-404.herokuapp.com/api/signup";

		const data = {
			userName: values.username,
			password: values.password,
			github: values.github,
			displayName: values.displayName,
			profileImage: values.profileImage,
		};

		let config = {};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);

				// TODO: get author from signup
				setUser(true); // if successful, confirm that we're logged in
				// redirect to inbox
				history.push("inbox");
			})
			.catch(function (error) {
				console.log(error);
				setLoading(false);
				setError("There was an error logging you in.");
			});
	};

	const onFinishFailed = (errorInfo) => {
		console.log("Failed:", errorInfo);
		setError("An error occurred. Please check that you filled in the form correctly.");
	};

	return (
		<div className="signup_page">
			<header className="header">
				<div className="menu">
					<Link to="/">
						<img src={logo} alt="logo" />
					</Link>
					<Link to="/login">Log In</Link>
				</div>
			</header>

			<main className="content">
				<h1>Sign Up</h1>

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
					labelCol={{ span: 10 }}
					initialValues={{ remember: true }}
					onFinish={onFinish}
					onFinishFailed={onFinishFailed}
					autoComplete="off"
				>
					<Form.Item
						label="Username"
						name="username"
						rules={[
							{ required: true, message: "Please input your username!" },
							{ max: 40, message: "Username too long!" },
						]}
						tooltip="This is a required field and must be between 1 and 40 characters"
					>
						<Input placeholder="eg. adalovelace" />
					</Form.Item>

					<Form.Item
						label="Password"
						name="password"
						rules={[{ required: true, message: "Please input your password!" }]}
					>
						<Input.Password />
					</Form.Item>

					<Form.Item
						name="confirm"
						label="Confirm Password"
						dependencies={["password"]}
						hasFeedback
						rules={[
							{
								required: true,
								message: "Please confirm your password!",
							},
							({ getFieldValue }) => ({
								validator(_, value) {
									if (!value || getFieldValue("password") === value) {
										return Promise.resolve();
									}
									return Promise.reject(
										new Error("The two passwords that you entered do not match!")
									);
								},
							}),
						]}
					>
						<Input.Password />
					</Form.Item>

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

					<Form.Item name="remember" valuePropName="checked" wrapperCol={{ offset: 8, span: 16 }}>
						<Checkbox>Remember me</Checkbox>
					</Form.Item>

					<Form.Item wrapperCol={{ offset: 10, span: 16 }}>
						<Button type="primary" htmlType="submit" loading={loading}>
							Submit
						</Button>
					</Form.Item>
				</Form>
			</main>
		</div>
	);
};

export default Signup;
