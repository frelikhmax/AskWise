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

const items = document.getElementsByClassName('like-section');

for (let item of items) {
    const [button, counter] = item.children;

    button.addEventListener('click', async () => {

        const formData = new FormData();

        formData.append('question_id', button.dataset.id)



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
                console.log({data});
                counter.innerHTML = data.count;
            })


    });
}


/*function getCookie(name) {
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

        const headers = new Headers({
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        });

        const body = JSON.stringify({'count': 'heyyyy'});

        const request = new Request('like/', {
            method: 'POST',
            headers: headers,
            body: body,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({data});
                counter.innerHTML = data.count;
            })


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
