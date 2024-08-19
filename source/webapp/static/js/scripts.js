async function makeRequest(url) {
    let response = await fetch(url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    });

    if (response.ok) {
        return await response.json();
    } else {
        let errorText = await response.text();
        let error = new Error(errorText);
        console.error(error);
        throw error;
    }
}

async function onClick(event) {
    event.preventDefault();
    let form = event.target.closest('form');
    let url = form.getAttribute('data-url');

    try {
        let data = await makeRequest(url);

        let likeButton = form.querySelector('button');
        let likeIcon = likeButton.querySelector('i');
        let likesCount = form.querySelector('.likes-count');

        if (likeIcon) {
            likeIcon.classList.toggle('bi-heart-fill');
            likeIcon.classList.toggle('bi-heart');
        }

        if (likesCount) {
            likesCount.textContent = `${data.likes_count} Likes`;
        }

        if (likeIcon && likeIcon.classList.contains('bi-heart-fill')) {
            likeButton.textContent = 'Unlike';
        } else {
            likeButton.textContent = 'Like';
        }
    } catch (error) {
        console.error('Ошибка при обработке лайка:', error);
    }
}

async function onLoad() {
    let forms = document.querySelectorAll('form[data-url]');

    forms.forEach(form => {
        form.addEventListener('submit', onClick);
    });
}

document.addEventListener('DOMContentLoaded', onLoad);
