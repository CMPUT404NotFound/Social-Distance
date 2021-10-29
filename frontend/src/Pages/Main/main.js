import { Layout, Menu, Button } from "antd";
import {
	InboxOutlined,
	BellOutlined,
	CompassOutlined,
	LogoutOutlined,
	PlusOutlined,
} from "@ant-design/icons";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";
import "./main.css";
import history from "./../../history";

const { Sider } = Layout;

const Main = ({ children, setLoggedIn }) => {
	const logout = () => {
		setLoggedIn(false);
		history.push("");
	};

	return (
		<div className="main_page">
			<Sider
				style={{
					overflow: "auto",
					height: "100vh",
					position: "fixed",
					left: 0,
				}}
			>
				<Menu theme="dark" mode="inline" defaultSelectedKeys={["4"]}>
					<Menu.Item key="0">
						<Link to="/">
							<img src={logo} alt="logo" />
						</Link>
					</Menu.Item>
					<Menu.Item key="1" icon={<InboxOutlined />}>
						<Link to="/inbox">Inbox</Link>
					</Menu.Item>
					<Menu.Item key="2" icon={<BellOutlined />}>
						<Link to="/notifications">Notifications</Link>
					</Menu.Item>
					<Menu.Item key="3" icon={<CompassOutlined />}>
						<Link to="/explore">Explore</Link>
					</Menu.Item>
					<Menu.Item key="4" icon={<LogoutOutlined />} onClick={logout}>
						LogOut
					</Menu.Item>
				</Menu>
			</Sider>
			<main className="content">{children}</main>
			<Link to="/createpost">
				<Button className="create_button" shape="circle" icon={<PlusOutlined />} size="large" />
			</Link>
		</div>
	);
};

export default Main;
