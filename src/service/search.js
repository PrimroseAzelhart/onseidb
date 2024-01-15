class cvService {
    getCV() {
        return fetch('http://api.onsei.fans/list/cv')
        .then((res) => res.json())
        .then((n) => n);
    }
};

class circleService {
    getCircle() {
        return fetch('http://api.onsei.fans/list/circle')
        .then((res) => res.json())
        .then((n) => n);
    }
};

class tagService {
    getTag() {
        return fetch('http://api.onsei.fans/list/tag')
        .then((res) => res.json())
        .then((n) => n);
    }
}

export { cvService, circleService, tagService };
