# PROPOSAL

## FOREIGN LANGUAGE TUTOR CHATBOT

### OVERVIEW
The foreign language tutor app leverages the OpenAI API to generate lifelike conversation scenarios, allowing language learners to practice their skills in immersive contexts and save conversations for future review for a personalized language learning experience.
### GOALS
The goal of this website is to provide language learners with a user friendly platform to develop and improve their conversational skills through immersive conversation scenarios with a foreign language chatbot tutor.
### TARGET USERS
Intermediate to advanced language learners who want to enhance their conversational skills will get the most out of the app, although beginners with some knowledge of their target language could still benefit.
### DATA
This app will utilize the OpenAI API to generate conversation scenarios. The specific data requirements would involve sending text prompts to the API and receiving generated responses. The app will also incorporate user data such as previous conversations and target language preferences.
### APPROACH
#### Database Schema
![databaseschema](/static/images/db_schema.png)
#### API Issues
Potential issues with the OpenAI API could include rate limits, handling API errors and responses. 
#### Functionality
User registration and login. Users can create new chat bots based on their target language preference, level of proficiency, and conversation topic preferences. The app will generate lifelike conversations for users to practice their language skills. Users will be able to view save their chats and access saved conversations for review.
### USER FLOW
1. Login/Sign up
2. User homepage to create a new chat bot, set preferences, view previous chats
3. Chat page where users interact with the chat bot
### FEATURES BEYOND CRUD
Personalization: Users can customize their chat bots based on language preferences, proficiency level preferences, and conversational preferences. The app generates conversation scenarios tailored to each user's preferences, providing a personalized language learning experience.
### STRETCH GOAL
A feature to select and save from each conversation relevant vocabulary and its translations for future review.
