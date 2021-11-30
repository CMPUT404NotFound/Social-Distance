import { useState, useEffect, useContext } from "react";
import "./explore.css";
import axios from "axios";
import Profile from "./profile";
import UserContext from "../../userContext";
import { Tabs } from "antd";

const { TabPane } = Tabs;

const Explore = () => {
	const { user } = useContext(UserContext);

	const [people, setPeople] = useState([]);
	const [remotePeople, setRemotePeople] = useState([]);

	// Get Local Users
	useEffect(() => {
		const url = `https://project-api-404.herokuapp.com/api/authors`;

		let config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setPeople(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user]);

	// Get remote users
	useEffect(() => {
		const url = `https://cmput404f21t17.herokuapp.com/service/connect/public/author/`;

		let config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
			auth: {
				username: "1802fb2b-e473-4078-ace3-c205897accf7",
				password: "123456",
			},
		};

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setRemotePeople(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user]);

	return (
		<div className="explore_page">
			{/* Posts and likes */}
			<Tabs defaultActiveKey="1" centered>
				<TabPane tab="Local Users" key="1" style={{ paddingInline: "1rem" }}>
					{people && people.map((person, i) => <Profile person={person} key={i} />)}
				</TabPane>
				<TabPane tab="Remote Users" key="2" style={{ paddingInline: "1rem" }}>
					{remotePeople &&
						remotePeople.items &&
						remotePeople.items.map((person, i) => <Profile person={person} key={i} remoteUser />)}
				</TabPane>
			</Tabs>
		</div>
	);
};

export default Explore;
