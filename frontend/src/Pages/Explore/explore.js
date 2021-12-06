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
	// const [remotePeople, setRemotePeople] = useState([]);

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	// Get Local Users
	useEffect(() => {
		const url = `https://project-api-404.herokuapp.com/api/nodes/authors/`;

		axios
			.get(url, config)
			.then(function (response) {
				console.log(response);
				setPeople(response.data.items);
			})
			.catch(function (error) {
				console.log(error);
			});
	}, [user]);

	return (
		<div className="explore_page">
			{people && people.map((person, i) => <Profile person={person} key={i} />)}
		</div>
	);
};

export default Explore;
