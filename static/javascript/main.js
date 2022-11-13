const xhr = new XMLHttpRequest();
const profileBtn = document.getElementById('profile-btn');
const profileBackBtn = document.getElementById('profile-back-btn');
const createChatBtn = document.getElementById('create-chat-btn');
const createChatBackBtn = document.getElementById('create-chat-back-btn')
const editProfileBtn = document.getElementById('edit-profile-btn');
const editProfileBackBtn = document.getElementById('edit-profile-back-btn');
const logOutBtn = document.getElementById('logout-btn');
const displayPicDivElement = document.getElementById('display-pic-placeholder-edit-profile');
const displayPicInput = document.getElementById('display-pic-input');
const displayPicCropOverlay = document.getElementById('display-pic-crop-overlay');
const imagePreview = document.getElementById('image-preview');
const croppedImageSaveBtn = document.getElementById('cropped-image-save-btn');  
const croppedImageCancelBtn = document.getElementById('cropped-image-cancel-btn');
const changePasswordBtn = document.getElementById('change-password-btn');
const changePasswordFieldsContainer = document.getElementById('change-password-fields-container');

addEventListenerIfElementExists(createChatBtn, 'click', switchToCreateChatSideArea);
addEventListenerIfElementExists(profileBtn, 'click', switchToProfileSideArea);
addEventListenerIfElementExists(editProfileBtn, 'click', function() {redirectFromOrigin('/edit-profile')});
addEventListenerIfElementExists(editProfileBackBtn, 'click', function() {redirectFromOrigin('/')});
addEventListenerIfElementExists(logOutBtn, 'click', function() {redirectFromOrigin('/logout')});
addEventListenerIfElementExists(displayPicInput, 'change', buildCropperOnImageInput);
addEventListenerIfElementExists(changePasswordBtn, 'click', toggleChangePasswordFields);
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
            let docSideAreaHeader = document.getElementById('side-area-header');
            let docProfileSideArea = document.getElementById('profile-side-area');

            profileBackBtn.addEventListener('click', function() {         
    
                switchToChatListSideArea(docSideAreaHeader, docProfileSideArea);
            });
    
        };
    };
};

function switchToCreateChatSideArea() {

    //This function switches the chat list side area to the create chat side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the create chat side area from the backend and replaces the chat list side area with it.
    //It sets an event listener on the create chat back button to call the switchToChatListSideArea function.

    xhr.open('GET', window.location.href);
    xhr.responseType = 'document';
    xhr.setRequestHeader('Partial-Template', 'create-chat-side-area');
    xhr.send();
      
    xhr.onload = function() {

        if (xhr.readyState == 4 && xhr.status == 200) {

            let newSideAreaHeader = xhr.responseXML.getElementById('side-area-header');
            let createChatSideArea = xhr.responseXML.getElementById('create-chat-side-area');               
            let sideAreaHeader = document.getElementById('side-area-header');
            let chatListSideArea = document.getElementById('chat-list-side-area');

            sideAreaHeader.parentNode.replaceChild(newSideAreaHeader, sideAreaHeader);
            chatListSideArea.parentNode.replaceChild(createChatSideArea, chatListSideArea);
            
            let createChatBackBtn = document.getElementById('create-chat-back-btn');
            let docSideAreaHeader = document.getElementById('side-area-header');
            let docCreateChatSideArea = document.getElementById('create-chat-side-area');

            createChatBackBtn.addEventListener('click', function() {

                switchToChatListSideArea(docSideAreaHeader, docCreateChatSideArea);
            });
    
        };
    };
};

function switchToChatListSideArea(sideareaheader, sidearea) {

    //This function switches the profile side area to the chat-list side area.
    //It sends a get request to the index route of the application with a custom header.
    //It recieves the rendered html fragment for the chat list side area from the backend and replaces the current side area with it.
    //It sets an event listener on the create chat back button to call the switchToCreateChatSideArea function.
    //It sets an event listener on the profile back button to call the switchToProfileSideArea function.
    //It sets an event listener on the user action button with the addEventListenerToActionsButton function.
    //It sets an event listener on the edit profile button to redirect to the edit profile view.
    //It sets an event listener on the log out button to redirect to the logout view.

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
            createChatBtn.addEventListener('click', switchToCreateChatSideArea);
            profileBtn.addEventListener('click', switchToProfileSideArea);
            editProfileBtn.addEventListener('click', function(){redirectFromOrigin('/edit-profile')});
            logOutBtn.addEventListener('click', function(){redirectFromOrigin('/logout')});
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