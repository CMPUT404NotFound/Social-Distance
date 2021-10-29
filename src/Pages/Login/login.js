import { Form, Input, Button, Checkbox } from "antd";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";
import "./login.css";

const Login = () => {
	// Inspired by AntD docs
	// https://ant.design/components/form/

	const onFinish = (values) => {
		console.log("Success:", values);
	};

	const onFinishFailed = (errorInfo) => {
		console.log("Failed:", errorInfo);
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
						<Button type="primary" htmlType="submit">
							Submit
						</Button>
					</Form.Item>
				</Form>
			</main>
		</div>
	);
};

export default Login;
