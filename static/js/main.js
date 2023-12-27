
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const items = document.getElementsByClassName('vote-section');

for (let item of items) {
    const [likeButton, dislikeButton, counter] = item.children;
    const questionId = likeButton.dataset.id;
    const csrfToken = getCookie('csrftoken');
    const url = item.dataset.url;  // Get the URL from the data-url attribute

    likeButton.addEventListener('click', async () => {
        handleVote(1, questionId, url, csrfToken, counter);
    });

    dislikeButton.addEventListener('click', async () => {
        handleVote(-1, questionId, url, csrfToken, counter);
    });
}

function handleVote(voteType, questionId, url, csrfToken, counter) {
    const formData = new FormData();
    formData.append('question_id', questionId);
    formData.append('vote_type', voteType);

    const request = new Request(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
        },
    });

    fetch(request)
        .then((response) => response.json())
        .then((data) => {
            console.log({ data });
            counter.innerHTML = data.count;
        });
}


/*function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const items = document.getElementsByClassName('like-section');

for (let item of items) {
    const [likeButton, dislikeButton, counter] = item.children;

    likeButton.addEventListener('click', async () => {
        handleVote(1, likeButton, counter);
    });

    dislikeButton.addEventListener('click', async () => {
        handleVote(-1, dislikeButton, counter);
    });
}

function handleVote(voteType, button, counter) {
    const formData = new FormData();
    formData.append('question_id', button.dataset.id);
    formData.append('vote_type', voteType);

    const request = new Request('like/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    fetch(request)
        .then((response) => response.json())
        .then((data) => {
            console.log({ data });
            counter.innerHTML = data.count;
        });
}*/


/*
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const items = document.getElementsByClassName('like-section');

for (let item of items) {
    const [button, counter] = item.children;

    button.addEventListener('click', async () => {
        const csrftoken = getCookie('csrftoken');

        const response = await fetch('like/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'count': 'heyyyy'}),
        });

        const data = await response.json();
        console.log({data});

        counter.innerHTML = data.count;

    });
}*/
