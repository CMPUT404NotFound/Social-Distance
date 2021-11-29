import {
	CompassOutlined,
	InboxOutlined,
	LogoutOutlined,
	PlusOutlined,
	GlobalOutlined,
} from "@ant-design/icons";
import { Button, Layout, Menu, Modal } from "antd";
import { useContext } from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";
import UserContext from "../../userContext";
import history from "./../../history";
import "./main.css";
import { useState } from "react";
import CreatePost from "../Create/create";

const { Sider } = Layout;

const Main = ({ children }) => {
	const { setUser } = useContext(UserContext);

	const [postModalVisible, setPostModalVisible] = useState(false);

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
					<Menu.Item key="2" icon={<GlobalOutlined />}>
						<Link to="/feed">Feed</Link>
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

			<Button
				className="create_button"
				shape="circle"
				icon={<PlusOutlined />}
				size="large"
				onClick={() => setPostModalVisible(true)}
			/>

			<Modal
				title="Create a Post"
				visible={postModalVisible}
				style={{ top: 20 }}
				width="80vw"
				footer={null}
				onCancel={() => {
					setPostModalVisible(false);
				}}
				destroyOnClose
			>
				<CreatePost
					cancel={() => {
						setPostModalVisible(false);
					}}
				/>
			</Modal>
		</div>
	);
};

export default Main;
