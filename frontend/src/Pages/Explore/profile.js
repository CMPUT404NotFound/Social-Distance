import React, { useState, useEffect, useContext } from "react";
import { Row, Col, Avatar, Button } from "antd";
import { UserOutlined, PlusOutlined } from "@ant-design/icons";
import UserContext from "../../userContext";
import axios from "axios";
import { getURLID, getIDfromURL } from "../../utils";
import { Link } from "react-router-dom";

const Profile = ({ person }) => {
	const { user } = useContext(UserContext);

	const [following, setFollowing] = useState(false);

	let url = `https://project-api-404.herokuapp.com/api/author/${getURLID(
		person.id
	)}/followers/${getURLID(user.id)}/`;

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	const check_following = () => {
		if (getIDfromURL(person.id) === user.uuid) return;

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
		<div className="profile_container">
			<Row align="middle" gutter={[16, 16]}>
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
							disabled={getIDfromURL(person.id) === user.uuid}
						>
							Follow
						</Button>
					)}
				</Col>
			</Row>
			<div className="source">Source: {person.host}</div>
		</div>
	);
};

export default Profile;
