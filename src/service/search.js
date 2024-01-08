class cvService {
    getCV() {
        return fetch('data/cv.json')
        .then((res) => res.json())
        .then((n) => n.name);
    }
};

class circleService {
    getCircle() {
        return fetch('data/circle.json')
        .then((res) => res.json())
        .then((n) => n.name);
    }
};

class tagService {
    getTag() {
        return fetch('data/tag.json')
        .then((res) => res.json())
        .then((n) => n.tags);
    }
}

export { cvService, circleService, tagService };
