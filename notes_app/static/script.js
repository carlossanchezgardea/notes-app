function toggleTheme() {
    let htmlElement = document.querySelector('html[data-bs-theme]');
    let currentTheme = htmlElement.getAttribute('data-bs-theme');

    if (currentTheme === 'light') {
        htmlElement.setAttribute('data-bs-theme', 'dark');
    } else {
        htmlElement.setAttribute('data-bs-theme', 'light');
    }
}

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
                        return res.json(); // Parse JSON from the response
                    } else {
                        console.error('Error:', res.status, res.statusText);
                        throw new Error('Error in creating note');
                    }
                })
                .then((data) => {
                    console.log(data); // Log the parsed JSON data
                    const noteId = data['note_id']; // Extract note_id from the response data

                    newNotesContainer.innerHTML = `
                            <div class="new-notes">
                                <h1>${title}</h1>
                                <h4>${description}</h4>
                                <p class="display-body">${body}</p>
                                <div class="d-flex">
                                    <button class="btn btn-outline-info editNote">Edit Note</button>
                                </div>
                            </div>  
                        `;

                    updateNotesList(lastClickedFolderId || firstFolderId);

                    const editButton = document.querySelector('.editNote');
                    editButton.addEventListener('click', (e) => {
                        e.preventDefault();

                        newNotesContainer.innerHTML = `
                            <div class="new-notes">
                                <form id="editNoteForm" method="POST">
                                    <input type="hidden" name="note_id" value="${noteId}">
                                    <div class="mb-3">
                                        <label for="title" class="form-label">Title</label>
                                        <input type="text" class="form-control" name="title" value="${title}">
                                    </div>
                                    <div class="mb-3">
                                        <label for="description" class="form-label">Description</label>
                                        <input type="text" class="form-control" name="description" value="${description}">
                                    </div>
                                    <div class="mb-3">
                                        <label for="body" class="form-label">Body</label>
                                        <textarea class="form-control" name="body" rows="3">${body}</textarea>
                                    </div>
                                    <div class="d-flex">
                                        <button class="btn btn-outline-info confirmEditNote">Save</button>
                                        <button class="btn btn-outline-danger cancelEditNote">Cancel</button>
                                    </div>
                                </form>
                            </div>`;

                        const editNoteForm = document.querySelector('#editNoteForm');

                        // Handle the submit event of the "Edit Note" form
                        editNoteForm.addEventListener('submit', async (e) => {
                            e.preventDefault();

                            const formData = new FormData(editNoteForm);

                            try {
                                const res = await fetch('http://127.0.0.1:9000/api/update_note', {
                                    method: 'POST',
                                    body: formData
                                });

                                if (res.ok) {
                                    console.log('Note updated successfully');
                                    await showNoteDetails(noteId);
                                    updateNotesList(lastClickedFolderId);
                                    // If there are additional tasks to do after updating a note, you can add them here
                                    // e.g. refreshing the note display, showing a success message, etc.
                                } else {
                                    console.error('Error updating note', res.status, res.statusText);
                                }
                            } catch (err) {
                                console.error('Error sending update request', err);
                            }
                        });

                        // Handle the click event of the "Cancel" button of the "Edit Note" form
                        const cancelEditButton = document.querySelector('.cancelEditNote');
                        cancelEditButton.addEventListener('click', (e) => {
                            e.preventDefault();
                            // If there are additional tasks to do after canceling the edit, you can add them here
                            // e.g. reverting the form values, hiding the form, etc.
                        });
                    });
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
        noteDetailsContainer.innerHTML = `
                <div class="new-notes">
                    <h1>${title}</h1>
                    <h4>${description}</h4>
                    <p class="display-body">${body}</p>
                
                    <div class="d-flex">
                        <button class="btn btn-outline-info editNote">Edit Note</button>
                        <button class="btn btn-outline-info sendNote" type="button" data-bs-toggle="modal"
                        data-bs-target="#noteEmailModal">Send Note</button>
                    </div>
                </div>  
                `
        const sendNoteButton = document.querySelector('.sendNote');
        sendNoteButton.addEventListener('click', () => {
            // Set the values of the modal's fields with the note's title, description, and body
            document.querySelector('#noteEmailModal [name="title"]').value = title;
            document.querySelector('#noteEmailModal [name="description"]').value = description;
            document.querySelector('#noteEmailModal [name="body"]').value = body;
        });

        const editButton = document.querySelector('.editNote');
        editButton.addEventListener('click', (e) => {
            e.preventDefault();
            noteDetailsContainer.innerHTML = `
                <div class="new-notes">
                    <form id="editNoteForm" method="POST">
                        <input type="hidden" name="note_id" value="${noteId}">
                        <div class="mb-3">
                            <label for="title" class="form-label">Title</label>
                            <input type="text" class="form-control" name="title" value="${title}">
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <input type="text" class="form-control" name="description" value="${description}">
                        </div>
                        <div class="mb-3">
                            <label for="body" class="form-label">Body</label>
                            <textarea class="form-control" name="body" rows="3">${body}</textarea>
                        </div>
                        <div class="d-flex">
                            <button class="btn btn-outline-info confirmNote">Save</button>
                            <button class="btn btn-outline-danger cancelNote">Cancel</button>
                        </div>
                    </form>
                </div>`;

            const editNoteForm = document.querySelector('#editNoteForm')
            editNoteForm.addEventListener('submit', async (e) => {
                e.preventDefault()

                const formData = new FormData(editNoteForm)
                console.log(formData)
                try {
                    const res = await fetch('http://127.0.0.1:9000/api/update_note', {
                        method: 'POST',
                        body: formData
                    });
                    if (res.ok) {
                        console.log('Note updated successfully');
                        await showNoteDetails(noteId);
                        updateNotesList(lastClickedFolderId);
                    } else {
                        console.error('Error updating note', res.status, res.statusText);
                    }
                } catch (err) {
                    console.error('Error sending update request', err);
                }

            })

        })

        const cancelButton = document.querySelector('.cancelNote');
        cancelButton.addEventListener('click', (e) => {
            e.preventDefault(); // To prevent any default action
            noteDetailsContainer.innerHTML = ''; // Clear the container
        });
    } catch (err) {
        console.log(err)
    }
}
document.addEventListener('DOMContentLoaded', (event) => {
    const sendNoteForm = document.getElementById('sendNoteForm');

    if (sendNoteForm) {
        sendNoteForm.addEventListener('submit', async function (e) {
            e.preventDefault(); // Prevent default form submission

            const formData = new FormData(sendNoteForm);

            try {
                const response = await fetch(sendNoteForm.action, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error('Error sending note');

                console.log('Note sent successfully');

                const noteEmailModal = new bootstrap.Modal(document.getElementById('noteEmailModal'));
                noteEmailModal.hide();

            } catch (error) {
                console.error('There was an error sending the note', error);
            }
        });
    }
});

// Initiate the process
populateFolders().then(() => {
    updateNotesList(firstFolderId); // Load notes for the first folder by default
});


