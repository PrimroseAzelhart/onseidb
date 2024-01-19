class searchService {
    get(item) {
        return fetch('https://api.onsei.fans/list/' + item)
        .then((res) => res.json())
        .then((data) => {
            localStorage.setItem(item, JSON.stringify(data));
            data;
        });
    }

    retrieve(item) {
        return localStorage.getItem(item);
    }
}

export { searchService };
