import { Alert } from "antd";

const Error401 = () => {
	return (
		<Alert
			message="Error 401: Unauthorized"
			description="You are unauthorized to access page you were trying to reach. Confirm that your URL is correct or contact your system administrator."
			type="error"
			showIcon
			style={{ margin: "2rem" }}
		/>
	);
};

export default Error401;