import { useState, useEffect } from "react";
import "./explore.css";
import axios from "axios";
import Profile from "./profile";

const Explore = ({ user }) => {
	const [people, setPeople] = useState([]);

	useEffect(() => {
		// TODO: Remove temporary user id
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
		<div className="inbox_page">
			{people.map((person) => {
				<Profile post={person} />;
			})}
		</div>
	);
};

export default Explore;
