import React from "react";
import ReactDOM from "react-dom";
import { Router } from "react-router";
import history from "./history";
import Routes from "./Routes";
import "antd/dist/antd.css";

ReactDOM.render(
	<React.StrictMode>
		<Router history={history}>
			<Routes />
		</Router>
	</React.StrictMode>,
	document.getElementById("root")
);