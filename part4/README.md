# 🏠 HBnB - Simple Web Client

> **Phase 4: Front-End Interface**  
> _Built with 💙 HTML5, CSS3 & JavaScript ES6_

---

## 📖 Overview

Welcome to the **HBnB Web Client** — the front-end layer of the HBnB application, where users can log in, browse places, view details, and leave reviews — all in a seamless, interactive UI.

This phase brings the project to life in the browser using modern web technologies, client-side logic, and API integration.

---

## 🎯 Objectives

- 🎨 Build a responsive and user-friendly interface from provided mockups.
- 🔗 Connect to the existing back-end API using `fetch` and secure JWT-based authentication.
- ⚙️ Enable client-side interactions and session management.
- 🚀 Apply dynamic DOM manipulation to enhance UX without page reloads.

---

## 📚 What You'll Learn

- ✅ HTML5 semantic structuring
- ✅ CSS3 styling and layouting
- ✅ JavaScript ES6 syntax and best practices
- ✅ Fetch API & handling asynchronous requests
- ✅ Storing and reading cookies for sessions
- ✅ Form validation and error feedback
- ✅ Dealing with **CORS** in full-stack apps

---

## 💡 Features

### 🔐 User Authentication
- JWT-based login system
- Session handled with cookies
- Auth-based UI changes (e.g. hide/show login button)

### 🗺️ Places Listing
- Fetch & display all available places from API
- Render as responsive **cards** with name, price, and detail buttons
- Live filtering by price range (10, 50, 100, All)

### 🏡 Place Details
- Load full data via place ID from URL
- Display host info, amenities, description & reviews
- Authenticated users can access the **Add Review** feature

### ✍️ Add a Review
- Auth-only access to submit reviews
- Protected routes: unauthenticated users get redirected
- POST review to the back-end with live feedback

---

## ⚙️ Technologies Used

- **HTML5**
- **CSS3**
- **JavaScript ES6**
- **Fetch API**
- **JWT & Cookies**
- **REST API Integration**
- **Client-side Form Validation**

---

## 📂 Project Structure

```bash
part4/
├── index.html          # List of Places
├── login.html          # Login Page
├── place.html          # Place Details
├── add_review.html     # Review Submission
├── styles.css          # Shared styling
├── scripts.js          # All JS logic here
└── assets/             # Logo, icons, images