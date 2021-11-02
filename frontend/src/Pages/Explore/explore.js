import { useState, useEffect, useContext } from "react";
import "./explore.css";
import axios from "axios";
import Profile from "./profile";
import UserContext from "../../userContext";

const Explore = () => {
	const { user } = useContext(UserContext);

	const [people, setPeople] = useState([]);

	useEffect(() => {
		const url = `https://project-api-404.herokuapp.com/api/authors`;

		const data = {};

		let config = {};

		axios
			.get(url, data, config)
			.then(function (response) {
				console.log(response);
				setPeople(response.data);
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
