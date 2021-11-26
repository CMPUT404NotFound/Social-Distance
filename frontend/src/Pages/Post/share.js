import { ShareAltOutlined } from "@ant-design/icons";
import UserContext from "../../userContext";
import axios from "axios";
import { useContext } from "react";

const Share = ({ post }) => {
	const { user } = useContext(UserContext);

	const url = `https://project-api-404.herokuapp.com/api/author/${user.id}/posts/`;

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	const data = {
		...post,
	};

	// Share the Post
	const sharePost = () => {
		axios
			.post(url, data, config)
			.then(function (response) {
				console.log(response);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	return <ShareAltOutlined style={{ fontSize: "2rem", color: "red" }} />;
};

export default Share;
