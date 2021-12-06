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

	useEffect(() => {
		const config = {
			headers: {
				Authorization: `Token ${user.token}`,
			},
		};

		// Get Local Users
		let url = `https://project-api-404.herokuapp.com/api/authors`;

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setPeople(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});

		// Get remote users
		url = `https://project-api-404.herokuapp.com/api/nodes/authors/`;

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
