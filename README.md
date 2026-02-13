# Annona
[cite_start]**Annona** [cite: 421]
[cite_start]A digital marketplace designed to bring order to the Rutgers dining experience. [cite: 422]
[cite_start]By transforming long, unformatted menus into a modular, "DoorDash-style" interface, it allows students to navigate campus food options, share custom "creations," and track nutritional goals efficiently. [cite: 423]

---

## **Goals/Motivation**

### [cite_start]**Consumer goals** [cite: 425]
* [cite_start]**Interactive UI & Navigation**: Create a modular, "DoorDash-style" interface that makes navigating campus dining halls intuitive and visually engaging. [cite: 426]
* [cite_start]**User Empowerment & Control**: Provide students with the tools to filter menus by dietary needs (Vegan, Gluten-Free) and categorize items for faster decision-making. [cite: 427]
* [cite_start]**Nutritional Transparency**: Implement a "Macro Builder" that gives users control over their dietary planning by viewing calories and protein before entering the hall. [cite: 428]
* [cite_start]**Community Engagement**: Enroll at least 5,000 Rutgers students within three months of launch to build a database of community "Creations". [cite: 429]

### [cite_start]**Personal goals** [cite: 430]
* [cite_start]**Mobile UI/UX Mastery**: Learn mobile-specific design principles (touch targets, gestures) and implement high-fidelity animations using React Native Reanimated or Framer Motion for React Native. [cite: 431]
* [cite_start]**Mobile Backend Integration**: Learn to build APIs (FastAPI) specifically for mobile clients, focusing on low data usage and fast response times. [cite: 432]
* [cite_start]**Mobile Auth & Security**: Master OAuth2 and JWT implementation within a mobile environment (handling Secure Storage vs. LocalStorage). [cite: 433]

---

## [cite_start]**Core Features** [cite: 447]

| Category | Feature | Description |
| :--- | :--- | :--- |
| **Dining Features** | **Modular Mobile Grid** | [cite_start]Daily menus formatted into specific blocks and rows for fast mobile browsing. [cite: 448] |
| | **Official Item Ratings** | [cite_start]1-5 star ratings for official dining hall items to provide feedback to Rutgers Dining Services. [cite: 448] |
| | **Rarity System** | Items feature tags (e.g., Rare, Legendary) based on frequency. [cite_start]Displays "[Rarity] - Last seen X days ago." [cite: 448] |
| | **Social Algorithm** | Upvote-driven community feed for student-created meals. [cite_start]Rankings surfaced and filterable by Day, Week, Month, and Year. [cite: 448] |
| **Utility System** | **Macro Builder** | [cite_start]Tool allowing users to select multiple items from a menu to view a live tally of total calories and macros. [cite: 448] |
| | **Item Pinning** | [cite_start]Users can pin specific items; receive push notifications and location info when the item returns. [cite: 448] |
| **Social & Collection** | **Custom Meals** | [cite_start]An option for sharing and commenting on custom "meal hacks" like Atrium combos or Kilmer's swipes. [cite: 448] |
| | **Annona "Dex"** | [cite_start]A collection log where students add foods they have tried to complete a full Rutgers food catalog. [cite: 448] |
| **Security** | **Verification** | [cite_start]Implementation of robust privacy controls compliant with university and FERPA standards. [cite: 448] |

---

## [cite_start]**Tech Stack** [cite: 434]

### [cite_start]**Frontend (Mobile)** [cite: 435]
* [cite_start]**Framework**: React Native [cite: 437]
* [cite_start]**UI Components**: NativeWind (Tailwind CSS for mobile) for the modular grid layout. [cite: 438]
* [cite_start]**State Management**: React Context [cite: 439]
* [cite_start]**Navigation**: React Navigation [cite: 441]

### [cite_start]**Backend** [cite: 442]
* [cite_start]**Language/Framework**: Python / FastAPI. [cite: 443]
* [cite_start]**Database**: PostgreSQL (Neon) with SQLAlchemy ORM. [cite: 444]
* [cite_start]**Scraper**: Python-based scripts to fetch and categorize Rutgers menu data. [cite: 445]

---

## [cite_start]**Scope** [cite: 451]

### [cite_start]**In scope** [cite: 452]
* [cite_start]**Rutgers-only Auth**: User registration and authentication via Google OAuth restricted to scarletmail@edu emails. [cite: 453]
* [cite_start]**Modular Menu Display**: Real-time fetching and categorization of menus from all Rutgers dining halls. [cite: 454]
* [cite_start]**User Profiles**: Basic profile display showing student name, level, and a history of their posted creations. [cite: 455]
* [cite_start]**Rating & Like System**: Logic for star ratings on official food and "Likes" on student creations. [cite: 456]
* [cite_start]**Admin Panel**: Managing menu content, flags on reviews, and user status. [cite: 457]

### [cite_start]**Out of scope** [cite: 458]
* [cite_start]**Live Ordering**: Direct ordering of food from dining hall staff (initial version is utility-only). [cite: 459]
* [cite_start]**Social Media API**: Direct sharing of combos to external platforms like Instagram [cite: 460]

---

## [cite_start]**Mobile Auth & Data Flow** [cite: 461]

### [cite_start]**Auth Flow**: [cite: 462]
1. [cite_start]**Student Login**: User clicks "Login with Rutgers" in the app. [cite: 463]
2. [cite_start]**External Auth**: App opens a system browser for Google OAuth consent (@scarletmail.rutgers.edu). [cite: 464]
3. [cite_start]**Verification**: Backend validates ID token signature and Rutgers email domain. [cite: 465]
4. [cite_start]**Deep Linking**: Successful login redirects back to the app via a custom URL scheme (e.g., annona://auth?token={jwt_token}). [cite: 466]
5. [cite_start]**Secure Storage**: Mobile app extracts the token and stores it in secure device storage for all API calls. [cite: 467]
