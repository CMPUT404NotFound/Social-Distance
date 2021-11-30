import { useState, useEffect, useContext } from "react";
import "./profile.css";
import axios from "axios";
import InboxPost from "../Inbox/post";
import UserContext from "../../userContext";
import { useLocation } from "react-router";
import { Link } from "react-router-dom";
import { Row, Col, Avatar, Button, Tabs } from "antd";
import { UserOutlined, PlusOutlined, EditOutlined } from "@ant-design/icons";
import { getIDfromURL } from "../../utils";

const { TabPane } = Tabs;

const Profile = () => {
	const location = useLocation();
	const person = location.state;

	const { user } = useContext(UserContext);

	const [posts, setPosts] = useState([]);
	const [following, setFollowing] = useState(false);
	const [editModalVisible, setEditModalVisible] = useState(false);

	let url = `https://project-api-404.herokuapp.com/api/author/${person.id}/`;

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	useEffect(() => {
		// Get the user's posts
		url += "posts/";

		let config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setPosts(response.data.items);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user, person]);

	const editProfile = () => {
		let data = {
			...user,
		};

		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);
				setPosts(response.data.items);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	// Check if following
	const check_following = () => {
		if (getIDfromURL(person.id) === user.id) return;

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setFollowing(true);
			})
			.catch(function (error) {
				if (error.response.status === 404) {
					Promise.resolve(error);
				} else console.log(error);
			});
	};

	useEffect(() => {
		// On load, check if following
		check_following();
	});

	// Follow
	const follow = () => {
		const data = {};
		axios
			.put(url, data, config)
			.then(function (response) {
				console.log(response);
				setFollowing(true);
			})
			.catch(function (error) {
				if (error.response.status === 404) {
					Promise.resolve(error);
				} else console.log(error);
			});

		// TODO: send follow request to their inbox
	};

	// Unfollow
	const unfollow = () => {
		axios
			.delete(url, config)
			.then(function (response) {
				console.log(response);
				setFollowing(false);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	return (
		<div className="profile_page">
			{/* Profile Info */}
			<Row align="middle" gutter={[16, 16]} className="profile_container">
				<Col>
					{person.profileImage ? (
						<Avatar src={person.profileImage} size={64} />
					) : (
						<Avatar icon={<UserOutlined />} size={64} />
					)}
				</Col>
				<Col flex={1}>
					<strong>Display Name:</strong> {person.displayName} <br />
					<strong>GitHub URL:</strong>{" "}
					{person.github ? <a href={person.github}>{person.github}</a> : "N/A"}
				</Col>
				<Col>
					{getIDfromURL(person.id) !== user.id ? (
						following ? (
							<Button type="primary" icon={<PlusOutlined />} onClick={unfollow} danger>
								Unfollow
							</Button>
						) : (
							<Button type="primary" icon={<PlusOutlined />} onClick={follow}>
								Follow
							</Button>
						)
					) : (
						<Button
							type="primary"
							icon={<EditOutlined />}
							onClick={() => {
								setEditModalVisible(true);
							}}
						>
							Edit Profile
						</Button>
					)}
				</Col>
			</Row>

			{/* Posts and likes */}
			<Tabs defaultActiveKey="1" centered style={{ background: "white" }}>
				<TabPane tab="Posts" key="1">
					{/* User Posts */}
					{posts &&
						posts.map((post, i) => (
							<Link to={{ pathname: "/post", state: post }} key={i}>
								<InboxPost post={post} key={i} />
							</Link>
						))}
				</TabPane>
				<TabPane tab="Likes" key="2">
					{/* User Likes */}
				</TabPane>
			</Tabs>
		</div>
	);
};

export default Profile;
