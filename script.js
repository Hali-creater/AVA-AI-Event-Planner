document.addEventListener('DOMContentLoaded', async () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    let conversationHistory = [];
    let questions = [];
    let currentQuestionIndex = 0;

    async function loadPromptAndQuestions() {
        try {
            const response = await fetch('prompt.md');
            const text = await response.text();

            const systemPrompt = text.split('COMPLETE QUESTIONING SEQUENCE')[0];
            conversationHistory.push({ role: 'system', content: systemPrompt });

            // More robust parser to only get questions from the correct section
            const questioningSection = text.split('COMPLETE QUESTIONING SEQUENCE')[1];
            const lines = questioningSection.split('\n');
            questions = lines
                .filter(line => line.trim().startsWith('"') || /^\d+\.\s*"/.test(line.trim()))
                .map(line => {
                    const match = line.match(/"([^"]*)"/);
                    return match ? match[1] : null;
                })
                .filter(question => question !== null);

            // Remove the "Opening Script" which is incorrectly parsed as the first question
            if (questions.length > 0) {
                questions.shift();
            }

            addMessage('bot', "Hello! I'm Ava, the receptionist assistant for Elite Events Planning. My job is to ask all the right questions so our expert planners have everything they need to create your perfect event. Let's start with the basics!");

        } catch (error) {
            console.error("Failed to load prompt.md:", error);
            addMessage('bot', "I'm sorry, I'm having trouble loading my instructions. Please try again later.");
        }
    }

    function addMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        const senderElement = document.createElement('div');
        senderElement.classList.add('message-sender');
        senderElement.textContent = sender === 'user' ? 'You' : 'Ava';

        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.textContent = message;

        messageElement.appendChild(senderElement);
        messageElement.appendChild(contentElement);

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function getLLMResponse(userMessage) {
        // Simulate a delay
        await new Promise(resolve => setTimeout(resolve, 500));

        let acknowledgement = "";
        // Acknowledge the user's input after the first question has been asked.
        if (currentQuestionIndex > 0) {
            acknowledgement = "Got it, thank you. ";
        }

        if (currentQuestionIndex < questions.length) {
            const nextQuestion = questions[currentQuestionIndex];
            currentQuestionIndex++;
            return `${acknowledgement}${nextQuestion}`;
        } else {
            return "Thank you for providing all the information. Our event planners will be in touch with you shortly!";
        }
    }

    async function handleUserInput() {
        const userMessage = userInput.value.trim();
        if (userMessage === '') return;

        addMessage('user', userMessage);
        conversationHistory.push({ role: 'user', content: userMessage });
        userInput.value = '';

        const botResponse = await getLLMResponse(userMessage);
        addMessage('bot', botResponse);
        conversationHistory.push({ role: 'assistant', content: botResponse });
    }

    sendBtn.addEventListener('click', handleUserInput);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });

    loadPromptAndQuestions();
});
