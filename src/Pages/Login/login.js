import { Form, Input, Button, Checkbox, Alert } from "antd";
import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";
import "./login.css";
import axios from "axios";

const Login = () => {
	// Inspired by AntD docs
	// https://ant.design/components/form/

	// states
	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);

	const onFinish = (values) => {
		setLoading(true);

		const url = "https://project-api-404.herokuapp.com/api/login";
		const data = {
			userName: values.username,
			password: values.password,
		};
		let config = {};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);
			})
			.catch(function (error) {
				console.log(error);
				setError("There was an error logging you in.");
			});
	};

	const onFinishFailed = (errorInfo) => {
		console.log(errorInfo);
	};

	return (
		<div className="login_page">
			<header className="header">
				<div className="menu">
					<Link to="/">
						<img src={logo} alt="logo" />
					</Link>
					<Link to="/signup">Sign Up</Link>
				</div>
			</header>

			<main className="content">
				<h1>Log In</h1>

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
					name="login"
					labelCol={{ span: 8 }}
					wrapperCol={{ span: 16 }}
					initialValues={{ remember: true }}
					onFinish={onFinish}
					onFinishFailed={onFinishFailed}
					autoComplete="off"
				>
					<Form.Item
						label="Username"
						name="username"
						rules={[{ required: true, message: "Please input your username!" }]}
					>
						<Input />
					</Form.Item>

					<Form.Item
						label="Password"
						name="password"
						rules={[{ required: true, message: "Please input your password!" }]}
					>
						<Input.Password />
					</Form.Item>

					<Form.Item name="remember" valuePropName="checked" wrapperCol={{ offset: 8, span: 16 }}>
						<Checkbox>Remember me</Checkbox>
					</Form.Item>

					<Form.Item wrapperCol={{ offset: 8, span: 16 }}>
						<Button type="primary" htmlType="submit" loading={loading}>
							Submit
						</Button>
					</Form.Item>
				</Form>
			</main>
		</div>
	);
};

export default Login;