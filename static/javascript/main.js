var xhr = new XMLHttpRequest();
var profileBtn = document.getElementById('profile-btn');
var profileBackBtn = document.getElementById('profile-back-btn');
var logOutBtn = document.getElementById('logout-btn')

addEventListenerIfElementExists(profileBtn, 'click', switchToProfileSideArea);
addEventListenerIfElementExists(logOutBtn, 'click', function() {redirectFromOrigin('/logout')});
addEventListenerToActionsButtons();

function addEventListenerToActionsButtons() {

    //This function adds an event listener to all of the action buttons to execute the addEventListenerToActionsButton function.

    let actionsButtonList = document.getElementsByClassName('action-btn');

    for (let index = 0; index < actionsButtonList.length; index++) {

        let actionsButton = actionsButtonList[index];

        addEventListenerToActionsButton(actionsButton);

    };
};

function addEventListenerToActionsButton(element) {

    //This function adds an event listerner to an action button which allows it to toggle its respective dropdown.
    
    element.addEventListener('click', function() {

        let dropdown = this.parentNode.getElementsByClassName('dropdown')[0];

        dropdown.classList.toggle('hide');

    });  
};

function addEventListenerIfElementExists(element, action, func) {

    //This function adds an event listener on an element if the element exists.

    if (element) {
        element.addEventListener(action, func);
    };
};

function switchToProfileSideArea() {

    //This function switches the chat list side area to the profile side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the profile side area from the backend and replaces the chat list side area with it.
    //It sets an event listener on the profile back button to call the switchToChatListSideArea function.

    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'profile-side-area');
    xhr.send();
      
    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let newSideAreaHeader = xhr.responseXML.getElementById('side-area-header');
            let profileSideArea = xhr.responseXML.getElementById('profile-side-area');               
            let sideAreaHeader = document.getElementById('side-area-header');
            let chatListSideArea = document.getElementById('chat-list-side-area');

            sideAreaHeader.parentNode.replaceChild(newSideAreaHeader, sideAreaHeader);
            chatListSideArea.parentNode.replaceChild(profileSideArea, chatListSideArea);

            let profileBackBtn = document.getElementById('profile-back-btn');

            profileBackBtn.addEventListener('click', switchToChatListSideArea);
    
        };
    };
};

function switchToChatListSideArea() {

    //This function switches the profile side area to the chat-list side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the chat list side area from the backend and replaces the profile side area with it.
    //It sets an event listener on the profile back button to call the switchToProfileSideArea function
    //It sets an event listener on the user action button with the addEventListenerToActionsButton function.
    //It sets an event listener on the log out button to redirect to the logout view.

    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'chat-list-side-area');
    xhr.send();
      
    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let newSideAreaHeader = xhr.responseXML.getElementById('side-area-header');
            let chatListSideArea = xhr.responseXML.getElementById('chat-list-side-area');  
            let sideAreaHeader = document.getElementById('side-area-header');
            let profileSideArea = document.getElementById('profile-side-area');

            sideAreaHeader.parentNode.replaceChild(newSideAreaHeader, sideAreaHeader);
            profileSideArea.parentNode.replaceChild(chatListSideArea, profileSideArea);

            let userActionsButton = document.getElementById('user-actions-btn');
            let profileBtn = document.getElementById('profile-btn')
            let logOutBtn = document.getElementById('logout-btn');
            
            addEventListenerToActionsButton(userActionsButton);
            profileBtn.addEventListener('click', switchToProfileSideArea);
            logOutBtn.addEventListener('click', function(){redirectFromOrigin('/logout')});
        };
    };
};

function redirectFromOrigin(path) {

    //This function redirects to the given path from the pages origin.

    window.location.replace(window.location.origin + path);
}