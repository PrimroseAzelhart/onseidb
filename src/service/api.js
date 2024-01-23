import axios from 'axios'

class databaseService {
    get(item) {
        return axios.get('https://api.onsei.fans/list/' + item)
                    .then((resp) => localStorage.setItem(item, JSON.stringify(resp.data)));
    }

    retrieve(item) {
        return localStorage.getItem(item);
    }

    checkUpdate() {
        return axios.get('https://api.onsei.fans/update')
                    .then((resp) => resp.data);
    }
}

export { databaseService };
