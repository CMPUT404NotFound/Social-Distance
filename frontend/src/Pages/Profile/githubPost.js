import React from "react";

const GithubPost = ({ event }) => {
	return (
		<div className="github_post">
			<p>
				<strong>Activity Type: </strong>
				{event.type}
			</p>
			<p>
				<strong>Activity Actor: </strong>
				<a href={"https://github.com/" + event.actor}>{event.actor}</a>
			</p>
			<p>
				<strong>Repository: </strong>
				<a href={"https://github.com/" + event.repo}>{event.repo}</a>
			</p>
		</div>
	);
};

export default GithubPost;
