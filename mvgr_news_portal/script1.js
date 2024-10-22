// script1.js

// Function to open the login modal
function openLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
    document.getElementById('loginModal').setAttribute('aria-hidden', 'false');
}

// Function to close all modals
function closeModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    });
}

// Close modals when clicking outside the modal content
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target == modal) {
            modal.style.display = 'none';
            modal.setAttribute('aria-hidden', 'true');
        }
    });
}

// Login function
function login(event) {
    event.preventDefault();
    const password = document.getElementById('adminPassword').value;
    // Replace 'yourpassword' with your actual admin password
    if (password === 'admin123') {
        closeModals();
        document.getElementById('adminPanel').style.display = 'block';
        document.getElementById('adminPanel').setAttribute('aria-hidden', 'false');
    } else {
        alert('Incorrect password. Please try again.');
    }
}

// Logout function
function logout() {
    closeModals();
    alert('You have been logged out.');
}

// Function to show change password modal
function showChangePasswordModal() {
    closeModals();
    document.getElementById('changePasswordModal').style.display = 'block';
    document.getElementById('changePasswordModal').setAttribute('aria-hidden', 'false');
}

// Change password function
function changePassword(event) {
    event.preventDefault();
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmNewPassword = document.getElementById('confirmNewPassword').value;
    
    // Replace 'yourpassword' with your actual current password
    if (currentPassword !== 'yourpassword') {
        alert('Current password is incorrect.');
        return;
    }

    if (newPassword !== confirmNewPassword) {
        alert('New passwords do not match.');
        return;
    }

    // Implement password update logic here (e.g., send to server)
    alert('Password changed successfully.');
    closeModals();
}

// Function to upload image
// Function to upload image
async function uploadImage(event) {
    event.preventDefault();

    const image = document.getElementById('imageUpload').files[0];  // Get the selected image
    const description = document.getElementById('imageDescription').value;  // Get the description
    const category = document.getElementById('imageCategory').value;  // Get the category

    if (!image || !category || !description) {
        alert("Please select an image, category, and provide a description.");
        return;
    }

    // Create a FormData object to hold the image, category, and description
    const formData = new FormData();
    formData.append("file", image);  // This key should match the FastAPI parameter
    formData.append("category", category);
    formData.append("description", description);  // Include description in the form data

    try {
        // Send the image, description, and category to the FastAPI server using fetch
        const response = await fetch('http://127.0.0.1:8000/upload-image/', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.info);  // Show success message from the server
            document.getElementById('uploadForm').reset();  // Reset the form after successful upload
            closeModals();  // Close the modal after upload
        } else {
            alert("Failed to upload image. Please try again.");
        }
    } catch (error) {
        console.error("Error uploading image:", error);
        alert("An error occurred while uploading the image.");
    }
}

// Function to filter images by category
async function filterImages(category) {
    const imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = '';  // Clear the existing images

    try {
        // Fetch images from the FastAPI server by category
        const response = await fetch(`http://127.0.0.1:8000/images/?category=${category}`);
        
        if (!response.ok) {
            alert("Failed to load images for the selected category.");
            return;
        }

        const data = await response.json();

        if (data.images && data.images.length > 0) {
            data.images.forEach(imageData => {
                const imgElement = document.createElement('img');
                imgElement.src = `http://127.0.0.1:8000/images/${category}/${imageData.name}`;
                imgElement.alt = imageData.name;
                imgElement.classList.add('gallery-image');  // Add a class for CSS styling

                const descriptionElement = document.createElement('p');
                descriptionElement.textContent = imageData.description || "No description available";  // Show description

                const imageWrapper = document.createElement('div');
                imageWrapper.classList.add('image-wrapper');  // Add a wrapper div for CSS styling
                imageWrapper.appendChild(imgElement);
                imageWrapper.appendChild(descriptionElement);

                imageContainer.appendChild(imageWrapper);
            });
        } else {
            imageContainer.innerHTML = `<p>No images found in '${category}' category.</p>`;
        }

    } catch (error) {
        console.error("Error loading images:", error);
        alert("An error occurred while loading images.");
    }
}

// async function showAllImages() {
//     const categories = ['sports', 'cultural', 'academic', 'clubs', 'announcements', 'others'];
//     const imageContainer = document.getElementById('image-container');
//     imageContainer.innerHTML = '';  // Clear existing images

//     try {
//         for (const category of categories) {
//             // Fetch images for each category
//             const response = await fetch(`http://127.0.0.1:8000/images/?category=${category}`);
//             const data = await response.json();

//             if (data.images && data.images.length > 0) {
//                 data.images.forEach(imageData => {
//                     const imgElement = document.createElement('img');
//                     imgElement.src = `http://127.0.0.1:8000/images/${category}/${imageData.image_name}`;
//                     imgElement.alt = imageData.image_name;
//                     imgElement.classList.add('gallery-image');  // Add a class for CSS styling

//                     // Create a description element
//                     const descElement = document.createElement('p');
//                     descElement.innerText = imageData.description || 'No description available';
                    
//                     const imageWrapper = document.createElement('div');
//                     imageWrapper.classList.add('image-wrapper');  // Add a wrapper for image and description
//                     imageWrapper.appendChild(imgElement);
//                     imageWrapper.appendChild(descElement);

//                     imageContainer.appendChild(imageWrapper);
//                 });
//             }
//         }
//     } catch (error) {
//         console.error("Error loading images:", error);
//         alert("An error occurred while loading images.");
//     }
// }
// Function to show all images (reset the gallery)
async function showAllImages() {
    const categories = ['sports', 'cultural', 'academic', 'clubs', 'announcements', 'others'];
    const imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = '';  // Clear existing images

    try {
        // Loop through each category and fetch images
        for (const category of categories) {
            // Fetch images for the current category
            const response = await fetch(`http://127.0.0.1:8000/images/?category=${category}`);
            
            if (!response.ok) {
                console.error(`Failed to load images for category: ${category}`);
                continue;  // Skip this category if there's an error
            }

            const data = await response.json();

            // If there are images, display them along with the descriptions
            if (data.images && data.images.length > 0) {
                data.images.forEach(imageData => {
                    // Create img element for each image
                    const imgElement = document.createElement('img');
                    imgElement.src = `http://127.0.0.1:8000/images/${category}/${imageData.name}`;
                    imgElement.alt = imageData.name;
                    imgElement.classList.add('gallery-image');

                    // Create description element for each image
                    const descriptionElement = document.createElement('p');
                    descriptionElement.textContent = imageData.description || "No description available";

                    // Create a wrapper div for both image and description
                    const imageWrapper = document.createElement('div');
                    imageWrapper.classList.add('image-wrapper');
                    imageWrapper.appendChild(imgElement);
                    imageWrapper.appendChild(descriptionElement);

                    imageContainer.appendChild(imageWrapper);
                });
            }
        }
    } catch (error) {
        console.error("Error loading images:", error);
        alert("An error occurred while loading all images.");
    }
}
