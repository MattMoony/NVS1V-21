const sock = new WebSocket("ws://127.0.0.1:6789");

sock.getId = () => sock.send(JSON.stringify({ action: 'get_id', }));
sock.saveNote = (id, title, body) => sock.send(JSON.stringify({ action: 'save', id, title, body, }));
sock.deleteNote = id => sock.send(JSON.stringify({ action: 'delete', id, }));

function onUpdateUserCount(data) {
    const count = document.getElementById('no-users');
    const icon = document.getElementById('users-icon');
    count.innerHTML = data.count;
    icon.classList.remove('fa-user', 'fa-users');
    if (data.count === 1) icon.classList.add('fa-user');
    else icon.classList.add('fa-users');
}

function onUpdateNotes(data) {
    const space = document.querySelector('.notes');
    space.querySelectorAll('.note').forEach(n => !n.classList.contains('not-saved') ? space.removeChild(n) : null);
    data.notes.forEach(n => addNote(false, n.id, n.title, n.body));
}

function onNewId(data) {
    addNote(true, data.id);
}

const hndlr = {
    'users': onUpdateUserCount,
    'id': onNewId,
    'notes': onUpdateNotes,
};

function createNote() {
    sock.getId();
}

function addNote(fresh, id, _title, _body) {
    /*
     * <div class="note">
     *     <h1 contenteditable autocomplete="off" spellcheck="false">Title</h1>
     *     <div class="body" contenteditable autocomplete="off" spellcheck="false">Body</div>
     *     <div>
     *         <i class="fas fa-trash-alt"></i>
     *         <button>Done</button>
     *     </div>
     * </div>
     */
    const space = document.querySelector('.notes');
    const note = document.createElement('div');
    note.setAttribute('note-id', id);
    note.classList.add('note');
    if (fresh) note.classList.add('editable', 'not-saved');
    const title = document.createElement('h1');
    title.toggleAttribute('contenteditable');
    title.setAttribute('autocomplete', 'off');
    title.setAttribute('spellcheck', 'false');
    title.textContent = _title || 'What\'s this note\'s title?';
    note.appendChild(title);
    const body = document.createElement('div');
    body.classList.add('body');
    body.toggleAttribute('contenteditable');
    body.setAttribute('autocomplete', 'off');
    body.setAttribute('spellcheck', 'false');
    body.textContent = _body || 'What should this note be about?';
    note.appendChild(body);
    const div = document.createElement('div');
    const trash = document.createElement('i');
    trash.classList.add('far', 'fa-trash-alt');
    trash.onclick = () => deleteNote(note);
    div.appendChild(trash);
    const button = document.createElement('button');
    button.innerHTML = 'Done';
    button.onclick = e => {
        e.stopPropagation();
        saveNote(note);
    }
    div.appendChild(button);
    note.appendChild(div);
    note.onclick = () => editNote(note);
    if (fresh || !space.querySelector('.not-saved')) space.appendChild(note);
    else space.insertBefore(note, space.querySelector('.not-saved'));
    if (fresh) title.focus();
}

function editNote(note) {
    note.classList.add('editable');
}

function saveNote(note) {
    note.classList.remove('editable');
    sock.saveNote(+note.getAttribute('note-id'), 
                  note.querySelector('h1').textContent, 
                  note.querySelector('.body').textContent);
    note.classList.remove('not-saved');
}

function deleteNote(note) {
    const space = document.querySelector('.notes');
    space.removeChild(note);
    sock.deleteNote(+note.getAttribute('note-id'));
}

window.onload = () => {
    const create = document.getElementById('create-button');
    create.onclick = () => createNote();

    sock.onmessage = e => {
        const data = JSON.parse(e.data);
        hndlr[data.type](data);
    };
};