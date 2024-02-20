import axios from 'axios'
import config from './config.json'

const axiosInstance = axios.create({
    baseURL: config.api,
    headers: {
        "Content-Type": 'application/x-www-form-urlencoded',
    }
});

class databaseService {
    getList(item) {
        return axiosInstance.get('/list/' + item)
                    .then((resp) => localStorage.setItem(item, JSON.stringify(resp.data)));
    }

    retrieveList(item) {
        return localStorage.getItem(item);
    }

    query(data) {
        return axiosInstance.post('/query', data)
                    .then((resp) => resp.data);
    }

    login(auth) {
        return axiosInstance.post('/login', auth)
                    .then((resp) => resp.data);
    }

    checkUpdate() {
        return axiosInstance.get('/database')
                    .then((resp) => resp.data);
    }
}

export { databaseService };
