import { useState, useEffect, useContext } from "react";
import "./profile.css";
import axios from "axios";
import InboxPost from "../Inbox/post";
import UserContext from "../../userContext";
import { useLocation } from "react-router";
import { Link } from "react-router-dom";
import { Row, Col, Avatar, Button, Tabs } from "antd";
import { UserOutlined, PlusOutlined, EditOutlined } from "@ant-design/icons";
import { getIDfromURL, getURLID } from "../../utils";
import EditProfile from "./editProfile";

const { TabPane } = Tabs;

const Profile = () => {
	const location = useLocation();
	const person = location.state;

	const { user } = useContext(UserContext);

	const [posts, setPosts] = useState([]);

	const [likes, setLikes] = useState([]);
	const [following, setFollowing] = useState(false);
	const [editModalVisible, setEditModalVisible] = useState(false);

	let url = `https://project-api-404.herokuapp.com/api/author/${getURLID(person.id)}/`;

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	useEffect(() => {
		// Get the user's posts
		axios
			.get(url + "posts/", config)
			.then(function (response) {
				console.log(response);
				setPosts(response.data.data || response.data);
			})
			.catch(function (error) {
				console.log(error);
			});
		// eslint-disable-next-line
	}, [user, person]);

	const getLikes = () => {
		// Get the user's likes
		axios
			.get(url + "liked/", config)
			.then(function (response) {
				console.log(response);

				response.data.items.forEach((item) => {
					axios
						.get(item.object, config)
						.then(function (response) {
							console.log(response);

							if (response.data.type === "post")
								setLikes((oldLikes) => [...oldLikes, response.data]);
						})
						.catch(function (error) {
							console.log(error);
						});
				});
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	// Check if following
	const check_following = () => {
		if (getIDfromURL(person.id) === user.uuid) return;

		axios
			.get(url + `followers/${getURLID(user.id)}/`, config)
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
		getLikes();
		// eslint-disable-next-line
	}, []);

	// Follow
	const follow = () => {
		const data = {};

		axios
			.put(url + `followers/${getURLID(user.id)}/`, data, config)
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
			.delete(url + `followers/${getURLID(user.id)}/`, config)
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
					{getIDfromURL(person.id) !== user.uuid ? (
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
					{likes &&
						likes.map((like, i) => (
							<Link to={{ pathname: "/post", state: like }} key={i}>
								<InboxPost post={like} key={i} />
							</Link>
						))}
				</TabPane>
			</Tabs>

			{/* Edit Profile Modal */}
			<EditProfile visible={editModalVisible} setVisible={setEditModalVisible} />
		</div>
	);
};

export default Profile;
