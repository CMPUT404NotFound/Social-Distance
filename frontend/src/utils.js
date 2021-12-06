export const setStorageSessionExpire = (key, value, ttl) => {
	const now = new Date();

	const item = {
		value: value,
		expiry: now.getTime() + ttl,
	};

	try {
		sessionStorage.setItem(key, JSON.stringify(item));
	} catch {
		console.warn("Failed to save", key, "to session storage");
		return null;
	}
};

export const getSessionStorage = (key) => {
	let item;

	try {
		item = sessionStorage.getItem(key);
	} catch {
		console.warn("Failed to load", key, "from session storage");
		return null;
	}

	if (!item) {
		console.warn(key, "is not in session storage");
		return null;
	}

	let now = new Date();
	let data = JSON.parse(item);

	if (now.getTime() > data.expiry) {
		console.warn(key, "has expired in session storage");
		return null;
	}

	return JSON.parse(item);
};

export const removeSessionStorage = (key) => {
	try {
		sessionStorage.removeItem(key);
	} catch {
		console.warn("Failed to remove", key, "from session storage");
		return null;
	}

	return true;
};

export const getIDfromURL = (url) => {
	// assumes that the url is of the form
	// http://host/something/.../id
	return url.split("/").pop();
};

export const getURLID = (url) => {
	// assumes that the url is of the form
	// http://host/something/.../id

	// remove schema
	url = url.replace("https://", "");
	url = url.replace("http://", "");

	// replace / with ~
	url = url.replaceAll("/", "~");

	return url;
};
