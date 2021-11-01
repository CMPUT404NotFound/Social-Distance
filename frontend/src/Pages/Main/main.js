import {
	BellOutlined,
	CompassOutlined,
	InboxOutlined,
	LogoutOutlined,
	PlusOutlined,
} from "@ant-design/icons";
import { Button, Layout, Menu } from "antd";
import { useContext } from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";
import UserContext from "../../userContext";
import history from "./../../history";
import "./main.css";

const { Sider } = Layout;

const Main = ({ children }) => {
	const { setUser } = useContext(UserContext);

	const logout = () => {
		setUser(null);
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
				<Menu theme="dark" mode="inline" defaultSelectedKeys={["0"]}>
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
