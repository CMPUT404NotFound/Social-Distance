import React, { useState, useEffect, useContext } from "react";
import { Row, Col, Avatar, Button } from "antd";
import { UserOutlined, PlusOutlined } from "@ant-design/icons";
import UserContext from "../../userContext";
import axios from "axios";
import { getIDfromURL } from "../../utils";

const Profile = ({ person }) => {
	const { user } = useContext(UserContext);

	const [following, setFollowing] = useState(false);

	const url = `https://project-api-404.herokuapp.com/api/author/${getIDfromURL(
		person.id
	)}/followers/${user.id}`;

	const check_following = () => {
		axios
			.get(url)
			.then(function (response) {
				console.log(response);
				setFollowing(true);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	useEffect(() => {
		// On load, check if following
		check_following();
	});

	const follow = () => {
		axios
			.put(url)
			.then(function (response) {
				console.log(response);
				setFollowing(true);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	const unfollow = () => {
		axios
			.delete(url)
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
				{/* TODO: add a link to profile page */}
				<a href={person.url}>{person.displayName}</a>
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
