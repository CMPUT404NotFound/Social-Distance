import { Alert } from "antd";

const Error404 = () => {
	return (
		<Alert
			message="Error 404: Page Not Found"
			description="The page you were trying to reach does not exist or was taken down. Confirm that your URL is correct or contact your system administrator."
			type="error"
			showIcon
			style={{ margin: "2rem" }}
		/>
	);
};

export default Error404;
