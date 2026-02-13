# Annona
**Annona**
* A digital marketplace designed to bring order to the Rutgers dining experience.
By transforming long, unformatted menus into a modular, "DoorDash-style" interface, it allows students to navigate campus food options, share custom "creations," and track nutritional goals efficiently.

---

## **Goals/Motivation**

### **Consumer goals**
* **Interactive UI & Navigation**: Create a modular, "DoorDash-style" interface that makes navigating campus dining halls intuitive and visually engaging.
* **User Empowerment & Control**: Provide students with the tools to filter menus by dietary needs (Vegan, Gluten-Free) and categorize items for faster decision-making.
* **Nutritional Transparency**: Implement a "Macro Builder" that gives users control over their dietary planning by viewing calories and protein before entering the hall.
* **Community Engagement**: Enroll at least 5,000 Rutgers students within three months of launch to build a database of community "Creations".

### **Personal goals**
* **Mobile UI/UX Mastery**: Learn mobile-specific design principles (touch targets, gestures) and implement high-fidelity animations using React Native Reanimated or Framer Motion for React Native.
* **Mobile Backend Integration**: Learn to build APIs (FastAPI) specifically for mobile clients, focusing on low data usage and fast response times.
* **Mobile Auth & Security**: Master OAuth2 and JWT implementation within a mobile environment (handling Secure Storage vs. LocalStorage).

---

## **Core Features**

| Category | Feature | Description |
| :--- | :--- | :--- |
| **Dining Features** | **Modular Mobile Grid** | Daily menus formatted into specific blocks and rows for fast mobile browsing. |
| | **Official Item Ratings** | 1-5 star ratings for official dining hall items to provide feedback to Rutgers Dining Services. |
| | **Rarity System** | Items feature tags (e.g., Rare, Legendary) based on frequency. Displays "[Rarity] - Last seen X days ago." |
| | **Social Algorithm** | Upvote-driven community feed for student-created meals. Rankings surfaced and filterable by Day, Week, Month, and Year. |
| **Utility System** | **Macro Builder** | Tool allowing users to select multiple items from a menu to view a live tally of total calories and macros. |
| | **Item Pinning** | Users can pin specific items; receive push notifications and location info when the item returns. |
| **Social & Collection** | **Custom Meals** | An option for sharing and commenting on custom "meal hacks" like Atrium combos or Kilmer's swipes. |
| | **Annona "Dex"** | A collection log where students add foods they have tried to complete a full Rutgers food catalog. |
| **Security** | **Verification** | Implementation of robust privacy controls compliant with university and FERPA standards. |

---

## **Tech Stack**

### **Frontend (Mobile)**
* **Framework**: React Native
* **UI Components**: NativeWind (Tailwind CSS for mobile) for the modular grid layout.
* **State Management**: React Context
* **Navigation**: React Navigation

### **Backend**
* **Language/Framework**: Python / FastAPI.
* **Database**: PostgreSQL (Neon) with SQLAlchemy ORM.
* **Scraper**: Python-based scripts to fetch and categorize Rutgers menu data.

---

## **Scope**

### **In scope**
* **Rutgers-only Auth**: User registration and authentication via Google OAuth restricted to scarletmail@edu emails.
* **Modular Menu Display**: Real-time fetching and categorization of menus from all Rutgers dining halls.
* **User Profiles**: Basic profile display showing student name, level, and a history of their posted creations.
* **Rating & Like System**: Logic for star ratings on official food and "Likes" on student creations.
* **Admin Panel**: Managing menu content, flags on reviews, and user status.

### **Out of scope**
* **Live Ordering**: Direct ordering of food from dining hall staff (initial version is utility-only).
* **Social Media API**: Direct sharing of combos to external platforms like Instagram.

---

## **Mobile Auth & Data Flow**

### **Auth Flow**:
1. **Student Login**: User clicks "Login with Rutgers" in the app.
2. **External Auth**: App opens a system browser for Google OAuth consent (@scarletmail.rutgers.edu).
3. **Verification**: Backend validates ID token signature and Rutgers email domain.
4. **Deep Linking**: Successful login redirects back to the app via a custom URL scheme (e.g., annona://auth?token={jwt_token}).
5. **Secure Storage**: Mobile app extracts the token and stores it in secure device storage for all API calls.
