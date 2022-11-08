var xhr = new XMLHttpRequest();
var profileBtn = document.getElementById('profile-btn');

if (profileBtn) {
    profileBtn.addEventListener('click', switchToProfileSideArea);
}

function switchToProfileSideArea() {

    //This function switches the chat list side area to the profile side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the profile side area from the backend and replaces the chat list side area with it.
    //It sets an event listener on the profile back button to call the switchToChatListSideArea function.
    //It sets an event listener on the log out button to redirect to the logout view.

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
            let logOutBtn = document.getElementById('logout-btn');

            profileBackBtn.addEventListener('click', switchToChatListSideArea);
            logOutBtn.addEventListener('click', function() {window.location.replace(window.location.href + '/logout')})
    
        }
    }
}

function switchToChatListSideArea() {

    //This function switches the profile side area to the chat-list side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the chat list side area from the backend and replaces the profile side area with it.
    //It sets an event listener on the profile button to call the switchToProfileSideArea function.

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

            let profilekBtn = document.getElementById('profile-btn');

            profilekBtn.addEventListener('click', switchToProfileSideArea);
     
        }
    }
}