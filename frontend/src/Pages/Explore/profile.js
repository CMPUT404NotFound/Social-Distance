import React, { useState, useEffect, useContext } from "react";
import { Row, Col, Avatar, Button } from "antd";
import { UserOutlined, PlusOutlined } from "@ant-design/icons";
import UserContext from "../../userContext";
import axios from "axios";
import { getIDfromURL } from "../../utils";
import { Link } from "react-router-dom";

const Profile = ({ person, remoteUser }) => {
	const { user } = useContext(UserContext);

	const [following, setFollowing] = useState(false);

	let url;

	if (remoteUser) {
		url = `https://project-api-404.herokuapp.com/api/author/${getIDfromURL(person.id)}/followers/${
			user.id
		}/`;
	} else {
		url = `https://project-api-404.herokuapp.com/api/author/${getIDfromURL(person.id)}/followers/${
			user.id
		}/`;
	}

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
		// auth: {
		// 	username: "1802fb2b-e473-4078-ace3-c205897accf7",
		// 	password: "123456",
		// },
	};

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
		<Row align="middle" gutter={[16, 16]} className="profile_container">
			<Col>
				{person.profileImage ? (
					<Avatar src={person.profileImage} />
				) : (
					<Avatar icon={<UserOutlined />} />
				)}
			</Col>
			<Col flex={1}>
				<Link to={{ pathname: "/profile", state: person }}>{person.displayName}</Link>
			</Col>
			<Col>
				{following ? (
					<Button type="primary" icon={<PlusOutlined />} onClick={unfollow} danger>
						Unfollow
					</Button>
				) : (
					<Button
						type="primary"
						icon={<PlusOutlined />}
						onClick={follow}
						disabled={getIDfromURL(person.id) === user.id}
					>
						Follow
					</Button>
				)}
			</Col>
		</Row>
	);
};

export default Profile;
