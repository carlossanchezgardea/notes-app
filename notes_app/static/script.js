let firstFolderId = ''

let lastClickedFolderId = null;


// Function to fetch data asynchronously
async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Failed to fetch ${url}`);
    }
    return await response.json();
}

async function updateNotesList(folderId = firstFolderId) {
    const notesContainer = document.querySelector('.note-list');
    notesContainer.innerHTML = '';
git
    try {
        const notesData = await fetchData(`http://127.0.0.1:9000/api/load_notes?folder_id=${folderId}`);

        for (const folder in notesData) {
            const title = notesData[folder].title;
            const description = notesData[folder].description;
            const note_id = notesData[folder].id;
            const noteElement = `
                <div class="ind-note" data-id="${note_id}">
                    <p>${title}</p>
                    <p class="description">${description}</p>
                </div>`;
            notesContainer.innerHTML += noteElement;
        }
        handleNoteClicks();


    } catch (err) {
        console.log(err);
    }
}

// Function to handle folder buttons
async function handleFolderClicks() {
    const notesButtons = document.querySelectorAll('.notesButton');

    notesButtons.forEach((button) => {
        button.addEventListener('click', async (e) => {
            lastClickedFolderId = e.target.value;
            await updateNotesList(lastClickedFolderId);
        });
    });
}

// Function to populate folders
async function populateFolders() {
    const folderList = document.querySelector('.list-of-folders');

    try {
        const folderData = await fetchData('http://127.0.0.1:9000/api/load_folders');

        for (const f in folderData) {
            const folderName = folderData[f].name;
            const folderId = folderData[f].id;
            if (!firstFolderId) firstFolderId = folderId;
            console.log(firstFolderId);

            const folderElem = `
                    <li class="nav-item ind-folder">
                        <button class="nav-link notesButton" aria-current="page" value=${folderId}>${folderName}</button>
                    </li>`;
            folderList.innerHTML += folderElem;
        }

        handleFolderClicks();  // Attach click handlers to folder buttons

    } catch (err) {
        console.log(err);
    }
}

//update notes area when clicking on create new note
const createNoteButton = document.querySelectorAll('.new-note-button');
const newNotesContainer = document.querySelector('.note-area');

createNoteButton.forEach((button) => {
    button.addEventListener('click', (e) => {
        newNotesContainer.innerHTML = `
                <div class="new-notes">
                    <form id="newNoteForm" method="POST">
                    <input type="hidden" name="folder_id" value=${lastClickedFolderId} name="folder_id">
                        <div class="mb-3">
                            <label for="exampleFormControlInput1" class="form-label">Title</label>
                            <input type="text" class="form-control" name="title">
                        </div>
                        <div class="mb-3">
                            <label for="exampleFormControlInput1" class="form-label">Description</label>
                            <input type="text" class="form-control" name="description">
                        </div>  
                        <div class="mb-3">
                            <label for="exampleFormControlTextarea1" class="form-label">Body</label>
                            <textarea class="form-control note-text-area" id="exampleFormControlTextarea1" rows="3" name="body"></textarea>
                        </div>
                        <div class="d-flex">
                            <button class="btn btn-outline-info confirmNote">Create Note</button>
                            <button class="btn btn-outline-danger cancelNote">Cancel</button> <!-- Cancel Button -->
                         </div>
                    </form>
                </div>
                 `;
        const cancelButton = document.querySelector('.cancelNote');
        cancelButton.addEventListener('click', (e) => {
            e.preventDefault(); // To prevent any default action
            newNotesContainer.innerHTML = ''; // Clear the container
        });

        const newNoteForm = document.querySelector('#newNoteForm')
        newNoteForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(newNoteForm);
            const title = formData.get('title')
            const description = formData.get('description')
            const body = formData.get('body')
            fetch('http://127.0.0.1:9000/create_note', {method: 'POST', body: formData})
                .then((res) => {
                    if (res.ok) {
                        console.log("success");
                        newNotesContainer.innerHTML = `
                            <div class="new-notes">
                                <h1>${title}</h1>
                                <h4>${description}</h4>
                                <p class="display-body">${body}</p>
                            </div>  
                            `;
                        updateNotesList(lastClickedFolderId || firstFolderId);  // Update notes list after successfully creating a new note
                    } else {
                        console.error('Error:', res.status, res.statusText);
                    }
                })
                .catch((err) => console.log(err));
        });
    });
});

async function handleNoteClicks() {
    const noteSelector = document.querySelectorAll('.ind-note');

    noteSelector.forEach((note) => {
        note.addEventListener('click', async (e) => {
            const noteId = e.currentTarget.getAttribute('data-id');
            console.log(noteId);
            await showNoteDetails(noteId);
        });
    });
}

async function showNoteDetails(noteId) {
    const noteDetailsContainer = document.querySelector('.note-area')
    noteDetailsContainer.innerHTML = ''
    try {
        const noteData = await fetchData(`http://127.0.0.1:9000/api/load_single_note?note_id=${noteId}`)
        console.log(noteData)
        const title = noteData.title
        const description = noteData.description
        const body = noteData.body
        noteDetailsContainer.innerHTML =`
        <div class="new-notes">
            <h1>${title}</h1>
            <h4>${description}</h4>
            <p class="display-body">${body}</p>
        </div>  
        `
    }
    catch (err) {
        console.log(err)
    }
}


// Initiate the process
populateFolders().then(() => {
    updateNotesList(firstFolderId); // Load notes for the first folder by default
});


