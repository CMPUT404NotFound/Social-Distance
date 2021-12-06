import { ShareAltOutlined } from "@ant-design/icons";
import UserContext from "../../userContext";
import axios from "axios";
import { useContext, useState } from "react";
import { Button } from "antd";

const Share = ({ post }) => {
	const { user } = useContext(UserContext);
	// eslint-disable-next-line
	const [shared, setShared] = useState(false);

	const url = `https://project-api-404.herokuapp.com/api/author/${user.uuid}/posts/`;

	const config = {
		headers: {
			Authorization: `Token ${user.token}`,
		},
	};

	const data = {
		...post,
	};

	// Share the Post
	// eslint-disable-next-line
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

	return <Button type="primary" shape="circle" icon={<ShareAltOutlined />}></Button>;
};

export default Share;
