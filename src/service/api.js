import axios from 'axios'
import config from './config.json'

const authCookies = $cookies.get('auth');

const axiosInstance = axios.create({
    baseURL: config.api,
    headers: {
        "Content-Type": 'application/x-www-form-urlencoded',
    }
});

class databaseService {
    getList(item) {
        const data = {'token': authCookies.token};
        return axiosInstance.post('/list/' + item, data)
                    .then((resp) => localStorage.setItem(item, JSON.stringify(resp.data)));
    }

    retrieveList(item) {
        return localStorage.getItem(item);
    }

    query(data) {
        data.token = authCookies.token;
        return axiosInstance.post('/query', data)
                    .then((resp) => resp.data);
    }

    login(auth) {
        return axiosInstance.post('/login', auth)
                    .then((resp) => resp.data);
    }

    register(auth) {
        return axiosInstance.post('/register', auth)
                    .then((resp) => resp.data);
    }

    checkUpdate() {
        const data = {'token': authCookies.token};
        return axiosInstance.post('/database', data)
                    .then((resp) => resp.data);
    }
}

export { databaseService };
