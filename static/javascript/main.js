const xhr = new XMLHttpRequest();
const profileBtn = document.getElementById('profile-btn');
const profileBackBtn = document.getElementById('profile-back-btn');
const createChatBtn = document.getElementById('create-chat-btn');
const createChatBackBtn = document.getElementById('create-chat-back-btn');
const createChatFormButton = document.getElementById('create-chat-form-button');
const editProfileBtn = document.getElementById('edit-profile-btn');
const editProfileBackBtn = document.getElementById('edit-profile-back-btn');
const logOutBtn = document.getElementById('logout-btn');
const sideAreaHeader = document.getElementById('side-area-header');
const chatListSideArea = document.getElementById('chat-list-side-area');
const displayPicDivElement = document.getElementById('display-pic-placeholder-edit-profile');
const displayPicInput = document.getElementById('display-pic-input');
const displayPicCropOverlay = document.getElementById('display-pic-crop-overlay');
const imagePreview = document.getElementById('image-preview');
const croppedImageSaveBtn = document.getElementById('cropped-image-save-btn');  
const croppedImageCancelBtn = document.getElementById('cropped-image-cancel-btn');
const changePasswordBtn = document.getElementById('change-password-btn');
const changePasswordFieldsContainer = document.getElementById('change-password-fields-container');

var openSocket = null;

addEventListenerIfElementExists(createChatBtn, 'click', function() {switchToCreateChatSideArea(sideAreaHeader, chatListSideArea);});
addEventListenerIfElementExists(profileBtn, 'click', function () {switchToProfileSideArea(sideAreaHeader, chatListSideArea);});
addEventListenerIfElementExists(editProfileBtn, 'click', function() {redirectFromOrigin('/edit-profile')});
addEventListenerIfElementExists(editProfileBackBtn, 'click', function() {redirectFromOrigin('/')});
addEventListenerIfElementExists(logOutBtn, 'click', function() {redirectFromOrigin('/logout')});
addEventListenerIfElementExists(displayPicInput, 'change', buildCropperOnImageInput);
addEventListenerIfElementExists(changePasswordBtn, 'click', toggleChangePasswordFields);
addEventListenerToActionsButtons();
addEventListenerToChats();

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

function switchToProfileSideArea(sideareaheader, sidearea) {

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

            sideareaheader.parentNode.replaceChild(newSideAreaHeader, sideareaheader);
            sidearea.parentNode.replaceChild(profileSideArea, sidearea);

            let profileBackBtn = document.getElementById('profile-back-btn');
            let docSideAreaHeader = document.getElementById('side-area-header');
            let docProfileSideArea = document.getElementById('profile-side-area');

            profileBackBtn.addEventListener('click', function() {         
    
                switchToChatListSideArea(docSideAreaHeader, docProfileSideArea);
            });
    
        };
    };
};

function switchToCreateChatSideArea(sideareaheader, sidearea) {

    //This function switches the chat list side area to the create chat side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the create chat side area from the backend and replaces the chat list side area with it.
    //It sets an event listener on the create chat back button to call the switchToChatListSideArea function.
    //It sets an event listener on the create chat form button to call the submitCreateChatForm function.

    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'create-chat-side-area');
    xhr.send();
      
    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let newSideAreaHeader = xhr.responseXML.getElementById('side-area-header');
            let createChatSideArea = xhr.responseXML.getElementById('create-chat-side-area');

            sideareaheader.parentNode.replaceChild(newSideAreaHeader, sideareaheader);
            sidearea.parentNode.replaceChild(createChatSideArea, sidearea);
            
            let createChatBackBtn = document.getElementById('create-chat-back-btn');
            let createChatFormButton = document.getElementById('create-chat-form-button')
            let docSideAreaHeader = document.getElementById('side-area-header');
            let docCreateChatSideArea = document.getElementById('create-chat-side-area');

            createChatBackBtn.addEventListener('click', function() {

                switchToChatListSideArea(docSideAreaHeader, docCreateChatSideArea);
            });

            createChatFormButton.addEventListener('click', function(event) {

                submitCreateChatForm(event);
            });
    
        };
    };
};

function switchToChatListSideArea(sideareaheader, sidearea, callBack) {

    //This function switches the profile side area to the chat-list side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the chat list side area from the backend and replaces the current side area with it.
    //It sets an event listener on the create chat back button to call the switchToCreateChatSideArea function.
    //It sets an event listener on all chats to call the switchChatWindow function.
    //It sets an event listener on the profile back button to call the switchToProfileSideArea function.
    //It sets an event listener on the user action button with the addEventListenerToActionsButton function.
    //It sets an event listener on the edit profile button to redirect to the edit profile view.
    //It sets an event listener on the log out button to redirect to the logout view.
    //It calls a callBack function passed to it.

    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'chat-list-side-area');
    xhr.send();
      
    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let newSideAreaHeader = xhr.responseXML.getElementById('side-area-header');
            let chatListSideArea = xhr.responseXML.getElementById('chat-list-side-area');  

            sideareaheader.parentNode.replaceChild(newSideAreaHeader, sideareaheader);
            sidearea.parentNode.replaceChild(chatListSideArea, sidearea);

            let userActionsButton = document.getElementById('user-actions-btn');
            let createChatBtn = document.getElementById('create-chat-btn');
            let profileBtn = document.getElementById('profile-btn');
            let editProfileBtn = document.getElementById('edit-profile-btn');
            let logOutBtn = document.getElementById('logout-btn');
            
            addEventListenerToActionsButton(userActionsButton);
            addEventListenerToChats()
            
            let docSideAreaHeader = document.getElementById('side-area-header');
            let docChatListSideArea = document.getElementById('chat-list-side-area');

            createChatBtn.addEventListener('click', function() {

                switchToCreateChatSideArea(docSideAreaHeader, docChatListSideArea);
            });

            profileBtn.addEventListener('click', function() {

                switchToProfileSideArea(docSideAreaHeader, docChatListSideArea);
            });

            editProfileBtn.addEventListener('click', function(){redirectFromOrigin('/edit-profile')});
            logOutBtn.addEventListener('click', function(){redirectFromOrigin('/logout')});

            if (callBack) {
                
                callBack();
            };
        };
    };
};

function redirectFromOrigin(path) {

    //This function redirects to the given path from the pages origin.

    window.location.replace(window.location.origin + path);
};

function buildCropperOnImageInput() {
 
    //This function builds a new cropper using cropperjs.
    //It sets an event listener to the cropper save button to swap the image input file with the cropped image.
    //The event listener opens the cropper overlay.
    //The event listener also adds a display image element to the edit profile form if it dosent aldready exist.
    //The event listener also destroys the old cropper instance.
    //It sets an event listener on the cropper cancel button to destroy the cropper instance.
    //The event listener also closes the cropper overlay and set the value of the image input and image preview source to null.


    var imageData = displayPicInput.files[0];
    var imageUrl = URL.createObjectURL(imageData);
    let Cropper = window.Cropper;
    
    displayPicCropOverlay.classList.remove('hide');
    imagePreview.src = imageUrl;

    let cropper = new Cropper(imagePreview, {aspectRatio: 9 / 9});
        
    croppedImageSaveBtn.addEventListener('click', function () {
        
        let croppedCanvas = cropper.getCroppedCanvas();

        if (croppedCanvas) {

            croppedCanvas.toBlob(function (blob) {
                
                let croppedImageName = 'cropped_' + imageData.name;
                let croppedImage = new File([blob], croppedImageName,{type:'image/*', lastModified:new Date().getTime()});
                let imageContainer = new DataTransfer();

                imageContainer.items.add(croppedImage);        
                displayPicInput.files = imageContainer.files;
                imageData = displayPicInput.files[0];
                imageUrl = URL.createObjectURL(imageData);
       
                let displayPicImgElement = document.getElementById('display-pic-edit-profile');
                    
                if (displayPicImgElement) {

                    displayPicImgElement.src = imageUrl;

                } else {

                    let croppedImageElement = document.createElement('img');

                    croppedImageElement.src = imageUrl;
                    croppedImageElement.classList.add('display-pic-img-large');
                    croppedImageElement.setAttribute('id', 'display-pic-edit-profile');
                    displayPicDivElement.replaceWith(croppedImageElement);
                }
                    
                imagePreview.cropper.destroy();
                displayPicCropOverlay.classList.add('hide');  
            }); 
        };
    });

    croppedImageCancelBtn.addEventListener('click', function() {

        if (imagePreview.classList.contains("cropper-hidden")) {

            imagePreview.src= "";
            imagePreview.cropper.destroy();
            displayPicInput.value = null;
            displayPicCropOverlay.classList.add('hide');
        };
    });
};

function toggleChangePasswordFields() {
    
    //This function toggles the change password fields of the edit profile form.

    let newPasswordField = document.getElementById('id_new_password');
    let confirmPasswordField = document.getElementById('id_confirm_password');

    if ((newPasswordField.readOnly == true) && (confirmPasswordField.readOnly == true)) {

        newPasswordField.readOnly = false;
        confirmPasswordField.readOnly = false;

    } else {

        newPasswordField.readOnly = true;
        confirmPasswordField.readOnly = true;
    };

    changePasswordFieldsContainer.classList.toggle('hide');
};

function submitCreateChatForm(event) {

    //This function submits the create chat form.
    //It prevents the submit button default which is to reload the page on submit.
    //It sends a post request to the index route of the application with a custom header.
    //It receives status code 200 from the backend if valid form data is submitted else it receives status code 400.
    //If the status code is 200 it calls the switchToChatListSideArea function.
    //If the status code is 400 it receivies a json dictionary with an error message, it displays this error in the form error element.

    let createChatForm = document.getElementById('create-chat-form');
    let formData = new FormData(createChatForm); 

    xhr.open('POST', window.location.href);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Index-Page-Form', 'create-chat-form');
    xhr.send(formData);

    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let sideAreaHeader = document.getElementById('side-area-header');
            let createChatSideArea = document.getElementById('create-chat-side-area');
            
            switchToChatListSideArea(sideAreaHeader, createChatSideArea);
        }
        
        else if (xhr.readyState == 4 && xhr.status == 400) {
            
            let error = xhr.response['error'];
            let createChatFormError = document.getElementById('create-chat-form-error');

            createChatFormError.innerHTML = error;
        };
    };  

    event.preventDefault();
};

function resizeMessageTextArea() {

    //This function resizes message text area to fit the text inside.

    this.rows = 1;
    this.rows = Math.floor((this.scrollHeight - 32) / 16);
};

function addEventListenerToChats() {

    let chatsList = document.getElementsByClassName('chat');

    for (let index = 0; index < chatsList.length; index++) {

        let chat = chatsList[index];

        chat.addEventListener('click', switchChatWindow);
    };  
};

function switchChatWindow() {
    
    //This function switches the chat area to the chat area that was selected.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the chat area from the backend and replaces the current chat area with it.
    //It sets an event listener on the user action button with the addEventListenerToActionsButton function.
    //It sets an event listener on the chat window back button to call the switchToChatWindowClosed function.
    //It sets an event listener on the chat window profile button to call the switchToChatParticipantProfileSideArea function.
    //It sets an event listener on the chat window edit chat button to call the switchToEditChatSideArea function.
    //It sets an event listener on the message text input to call the resizeMessageTextArea function.
    //It closes a existing socket and opens a new web socket.
    
    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'chat-window');
    xhr.setRequestHeader('Chat-Id', this.getAttribute('data-chat-id'));
    xhr.send();

    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let chatAreaHeader = document.getElementById('chat-area-header');
            let chatArea = document.getElementById('chat-area');
            let newChatAreaHeader = xhr.responseXML.getElementById('chat-area-header');
            let newChatArea = xhr.responseXML.getElementById('chat-area');  

            chatAreaHeader.parentNode.replaceChild(newChatAreaHeader, chatAreaHeader);
            chatArea.parentNode.replaceChild(newChatArea, chatArea); 
            
            let chatWindowActionsButton = document.getElementById('chat-window-actions-btn');
            let chatWindowBackBtn = document.getElementById('chat-window-back-btn');
            let chatWindowProfileBtn = document.getElementById('chat-window-profile-btn');
            let chatWindowEditChatBtn = document.getElementById('chat-window-edit-chat-btn');
            let chatWindowDeleteChatBtn = document.getElementById('chat-window-delete-chat-btn');
            let messageTextInput = document.querySelector('#message-form textarea');  
                    
            chatWindowProfileBtn.addEventListener('click', function() {
           
                let docSideAreaHeader = document.getElementById('side-area-header');
                let docProfileSideArea = document.getElementById('profile-side-area');    
                let docCreateChatSideArea = document.getElementById('create-chat-side-area');
                let docChatListSideArea = document.getElementById('chat-list-side-area'); 
                let docEditChatSideArea = document.getElementById('edit-chat-side-area'); 

                if (docProfileSideArea) { 
                    
                    docSideAreaHeader = document.getElementById('side-area-header');
                    docProfileSideArea = document.getElementById('profile-side-area');    
                    
                    switchToChatParticipantProfileSideArea(this, docSideAreaHeader, docProfileSideArea, switchToProfileSideArea);
                }
                else if (docCreateChatSideArea) { 
                        
                    docSideAreaHeader = document.getElementById('side-area-header');
                    docCreateChatSideArea = document.getElementById('create-chat-side-area');
                    
                    switchToChatParticipantProfileSideArea(this, docSideAreaHeader, docCreateChatSideArea, switchToCreateChatSideArea);
                }
                else if (docChatListSideArea) { 
                    
                    docSideAreaHeader = document.getElementById('side-area-header');
                    docChatListSideArea = document.getElementById('chat-list-side-area');    
                            
                    switchToChatParticipantProfileSideArea(this, docSideAreaHeader, docChatListSideArea, switchToChatListSideArea);
                }
                else if (docEditChatSideArea) { 
                    
                    docSideAreaHeader = document.getElementById('side-area-header');
                    docEditChatSideArea = document.getElementById('edit-chat-side-area'); 
                            
                    switchToChatParticipantProfileSideArea(this, docSideAreaHeader, docEditChatSideArea, switchToChatListSideArea);
                };
            });

            chatWindowEditChatBtn.addEventListener('click', function() {
           
                let docSideAreaHeader = document.getElementById('side-area-header');
                let docProfileSideArea = document.getElementById('profile-side-area');    
                let docCreateChatSideArea = document.getElementById('create-chat-side-area');
                let docChatListSideArea = document.getElementById('chat-list-side-area'); 
                let docChatParticipantProfileSideArea = document.getElementById('chat-participant-profile-side-area'); 

                if (docProfileSideArea) { 
                    
                    docSideAreaHeader = document.getElementById('side-area-header');
                    docProfileSideArea = document.getElementById('profile-side-area');    
                    
                    switchToEditChatSideArea(this, docSideAreaHeader, docProfileSideArea, switchToProfileSideArea);
                }
                else if (docCreateChatSideArea) { 
                        
                    docSideAreaHeader = document.getElementById('side-area-header');
                    docCreateChatSideArea = document.getElementById('create-chat-side-area');
                    
                    switchToEditChatSideArea(this, docSideAreaHeader, docCreateChatSideArea, switchToCreateChatSideArea);
                }
                else if (docChatListSideArea) { 
                    
                    docSideAreaHeader = document.getElementById('side-area-header');
                    docChatListSideArea = document.getElementById('chat-list-side-area');    
                            
                    switchToEditChatSideArea(this, docSideAreaHeader, docChatListSideArea, switchToChatListSideArea);
                }
                else if (docChatParticipantProfileSideArea) { 
                    
                    docSideAreaHeader = document.getElementById('side-area-header');  
                    docChatParticipantProfileSideArea = document.getElementById('chat-participant-profile-side-area'); 
                            
                    switchToEditChatSideArea(this, docSideAreaHeader, docChatParticipantProfileSideArea, switchToChatListSideArea);
                };
            });

            chatWindowDeleteChatBtn.addEventListener('click', function() {

                deleteChat(this);
            });

            addEventListenerToActionsButton(chatWindowActionsButton);
            chatWindowBackBtn.addEventListener('click', switchToChatWindowClosed);
            messageTextInput.addEventListener('input', resizeMessageTextArea);
              
            if (openSocket) {

                openSocket.close();     
            };

            chatSocket();
        };
    };  
};

function switchToChatWindowClosed() {

    //This function switches the chat area to its default closed state.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the chat area from the backend and replaces the current chat area with it.
    //It closes the open socket.

    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'chat-window-closed');
    xhr.send();

    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let chatAreaHeader = document.getElementById('chat-area-header');
            let chatArea = document.getElementById('chat-area');
            let newChatAreaHeader = xhr.responseXML.getElementById('chat-area-header');
            let newChatArea = xhr.responseXML.getElementById('chat-area');  

            chatAreaHeader.parentNode.replaceChild(newChatAreaHeader, chatAreaHeader);
            chatArea.parentNode.replaceChild(newChatArea, chatArea); 

                  
            if (openSocket) {

                openSocket.close();     
            };
        };
    };
};

function switchToChatParticipantProfileSideArea(element, sideareaheader, sidearea, switchfunction = null) {

    //This function switches the current side area to the chat participant profile side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the chat participant profile side area from the backend and replaces the current side area with it.
    //It sets an event listener on the profile back button to call the switch function.

    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'chat-participant-profile-side-area');
    xhr.setRequestHeader('Chat-Id', element.getAttribute('data-chat-id'));
    xhr.send();
      
    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let newSideAreaHeader = xhr.responseXML.getElementById('side-area-header');
            let newChatParticipantProfileSideArea = xhr.responseXML.getElementById('chat-participant-profile-side-area');             
                        
            sideareaheader.parentNode.replaceChild(newSideAreaHeader, sideareaheader);
            sidearea.parentNode.replaceChild(newChatParticipantProfileSideArea, sidearea);
            
            let chatParticipantProfileBackBtn = document.getElementById('chat-participant-profile-back-btn');
            let docSideAreaHeader = document.getElementById('side-area-header'); 
            let docChatParticipantProfileSideArea = document.getElementById('chat-participant-profile-side-area');

            chatParticipantProfileBackBtn.addEventListener('click', function() {switchfunction(docSideAreaHeader, docChatParticipantProfileSideArea);});                
        };
    };
};

function switchToEditChatSideArea(element, sideareaheader, sidearea, switchfunction = null) {

    //This function switches the current side area to the edit chat side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the edit chat side area from the backend and replaces the current side area with it.
    //It sets an event listener on the profile back button to call the switch function.
    //It sets an event listener on the edit chat form button to call the submitEditChatForm function.

    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'edit-chat-side-area');
    xhr.setRequestHeader('Chat-Id', element.getAttribute('data-chat-id'));
    xhr.send();
      
    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let newSideAreaHeader = xhr.responseXML.getElementById('side-area-header');
            let newEditChatSideArea = xhr.responseXML.getElementById('edit-chat-side-area');             
            
            sideareaheader.parentNode.replaceChild(newSideAreaHeader, sideareaheader);
            sidearea.parentNode.replaceChild(newEditChatSideArea, sidearea);
            
            let editChatBackBtn = document.getElementById('edit-chat-back-btn');
            let docSideAreaHeader = document.getElementById('side-area-header'); 
            let docEditChatSideArea = document.getElementById('edit-chat-side-area');
            let editChatFormBtn = document.getElementById('edit-chat-form-button');

            editChatBackBtn.addEventListener('click', function() {
                
                switchfunction(docSideAreaHeader, docEditChatSideArea);
            });

            editChatFormBtn.addEventListener('click', function(event) {

                submitEditChatForm(event, this)
            });
        };
    };
};

function submitEditChatForm(event, element) {

    //This function submits the edit chat form.
    //It prevents the submit button default which is to reload the page on submit.
    //It sends a post request to the index route of the application with a custom header.
    //It receives status code 200 from the backend if valid form data is submitted else it receives status code 400.
    //If the status code is 200 it receivies a json dictionary with a new display name, it replaces the chat window title with it.
    //It also calls the switchToChatListSideArea function,
    //If the status code is 400 it receivies a json dictionary with an error message, it displays this error in the form error element.

    let editChatForm = document.getElementById('edit-chat-form');
    let formData = new FormData(editChatForm); 

    xhr.open('POST', window.location.href);
    xhr.responseType = 'json';
    xhr.setRequestHeader('Index-Page-Form', 'edit-chat-form');
    xhr.setRequestHeader('Chat-Id', element.getAttribute('data-chat-id'));
    xhr.send(formData);

    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let sideAreaHeader = document.getElementById('side-area-header');
            let editChatSideArea = document.getElementById('edit-chat-side-area');
            let display_name = xhr.response['display_name'];
            let chatAreaHeaderTitle = document.querySelector('#chat-area-header #title');

            chatAreaHeaderTitle.innerHTML = display_name

            switchToChatListSideArea(sideAreaHeader, editChatSideArea);
        }
        
        else if (xhr.readyState == 4 && xhr.status == 400) {
            
            let error = xhr.response['error'];
            let editChatFormError = document.getElementById('edit-chat-form-error');

            editChatFormError.innerHTML = error;
        };
    };  

    event.preventDefault();
};

function deleteChat(element) {

    //This function switches sends a request to the index route of the application with a cutom header to delete a chat.
    //Once it recieves confirmation that deletion is complete it calles the switchToChatListSideArea function with switchToChatWindowClosed as a callback.  
    
    Cookies = window.Cookies;

    const csrftoken = Cookies.get('csrftoken');

    xhr.open('DELETE', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.setRequestHeader('Chat-Id', element.getAttribute('data-chat-id'));
    xhr.send();

    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {
            
            let sideAreaHeader = document.getElementById('side-area-header');
            let chatListSideArea = document.getElementById('chat-list-side-area');
            
            switchToChatListSideArea(sideAreaHeader, chatListSideArea, switchToChatWindowClosed);               
        };
    };
};

function chatSocket() {

    let messageForm = document.getElementById('message-form');
    let messageFormTextInput = document.getElementById('message-text-input');
    let messageFormSendBtn = document.getElementById('message-form-send-btn');
    let chatId = messageFormSendBtn.getAttribute('data-chat-Id');
    let url = `ws://${window.location.host}/ws/chat/${chatId}`;

    openSocket = new WebSocket(url);

    openSocket.onmessage = function(event) {
        let data = JSON.parse(event.data);
        console.log(data.message)        
    };

    openSocket.onclose = function(event) {
        console.error('Chat socket closed unexpectedly');
    };

    messageFormSendBtn.addEventListener('click', function(event) {

        event.preventDefault();

        let message = messageFormTextInput.value;
        let messageJSON = JSON.stringify({'message': message});
        
        messageForm.reset()
        messageFormTextInput.focus();
        messageFormTextInput.rows = 1;

        openSocket.send(messageJSON);
    });

    messageFormTextInput.addEventListener('keypress', function(event) {

        if (event.key == 'Enter') {
            
            event.preventDefault();
            messageFormSendBtn.click();
        };
    });
};