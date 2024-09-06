function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function get_language(){
    const language = getCookie("django_language");
    return language || 'az';
}

document.addEventListener('DOMContentLoaded', function() {
    const chatbotIcon = document.getElementById('chatbot-icon');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotHeader = document.getElementById('chatbot-header'); // Selecting the chatbot header
    const closeChatbot = document.getElementById('close-chatbot');
    // const sendMessageButton = document.getElementById('send-message');
    // const userInput = document.getElementById('user-input');
    const chatbotMessages = document.getElementById('chatbot-messages');


    let offsetX = 0;
    let offsetY = 0;
    let isDragging = false;
    let hasShownWelcomeMessage = false;

    const faqCategories = {
    };

    const translations = {
        en: {
            welcomeMessage: "Hello! How can I assist you today?",
            askAnotherQuestion: "Ask Another Question",
            returnToCategories: "Return to Categories",
            endChat: "Thank you for chatting with me. Have a great day!",
            nextStep: "What would you like to do next?",
            learnMore: "Learn more about our services.",
            goBack: "Going back to the previous step.",
            joinChat: "Join the chat",
            frequentlyAskedQuestions: "Frequently asked questions"
        },
        az: {
            welcomeMessage: "Salam! Sizə necə kömək edə bilərəm?",
            askAnotherQuestion: "Başqa bir sual verin",
            returnToCategories: "Kateqoriyalara geri dön",
            endChat: "Mənimlə söhbət etdiyiniz üçün təşəkkür edirəm. Gözəl bir gün arzulayıram!",
            nextStep: "Növbəti nə etmək istəyirsiniz?",
            learnMore: "Xidmətlərimiz haqqında daha çox öyrənin.",
            goBack: "Əvvəlki mərhələyə qayıdın.",
            joinChat: "Çata qoşul",
            frequentlyAskedQuestions: "Tez-tez soruşulan suallar"
        },
        ru: {
            welcomeMessage: "Здравствуйте! Чем могу помочь?",
            askAnotherQuestion: "Задать другой вопрос",
            returnToCategories: "Вернуться к категориям",
            endChat: "Спасибо за беседу. Хорошего дня!",
            nextStep: "Что бы вы хотели сделать дальше?",
            learnMore: "Узнать больше о наших услугах.",
            goBack: "Вернуться на предыдущий шаг.",
            joinChat: "Присоединяйтесь к чату",
            frequentlyAskedQuestions: "Часто задаваемые вопросы"
        }
    };

    let currentLanguage = get_language(); // Set the default language

    function translateText(key) {
        return translations[currentLanguage][key];
    }

    // API'den FAQ kategorilerini al
    async function getFaqCategories() {
        try {
            const response = await fetch('/api/v1/chat_bot/faqs/', {
                method: 'GET', // or 'POST', 'PUT', etc. based on your needs
                headers: {
                  'Content-Type': 'application/json', // Example header
                  'Accept-Language': currentLanguage
                }
              });
            if (!response.ok) {
                throw new Error('FAQ kategorileri alınamadı. Sunucu yanıtı: ' + response.status);
            }
            const apiData = await response.json(); 
            
            apiData.forEach(category => {
                faqCategories[category.name] = category.faqs.map(faq => ({
                    question: faq.question,
                    answer: faq.answer
                }));
            });
            
            
        } catch (error) {
            console.error('Hata:', error);
            // Hata mesajını kullanıcıya göster
        }
    }

    // Show chatbot window when the icon is clicked
    chatbotIcon.addEventListener('click', function() {
        chatbotIcon.classList.add('display-none');
        chatbotWindow.classList.remove('display-none');
        if (!hasShownWelcomeMessage) {
            showWelcomeMessage();
            hasShownWelcomeMessage = true;
        }
    });

    // Close chatbot window
    closeChatbot.addEventListener('click', function() {
        chatbotWindow.classList.add('display-none');
        chatbotIcon.classList.remove('display-none');
    });

    // Welcome message logic
    function showWelcomeMessage() {
        setTimeout(function() {
            addMessage(translateText('welcomeMessage'), 'bot-message');
            addDynamicOptions([translateText('frequentlyAskedQuestions'), translateText('joinChat')]);
        }, 500);
    }

    // Display FAQ categories
    function showCategories() {
        const existingOptions = document.querySelector('.options-container');
        if (existingOptions) {
            existingOptions.remove();
        }

        Object.keys(faqCategories).forEach(category => {
            const categoryElement = document.createElement('div');
            categoryElement.classList.add('faq-category');
            categoryElement.textContent = category;
            categoryElement.addEventListener('click', function() {
                addMessage(category, 'user-message');
                setTimeout(function() {
                    showQuestions(category);
                }, 500);
            });
            chatbotMessages.appendChild(categoryElement);
        });

        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Display questions within the selected category
    function showQuestions(category) {
        const existingOptions = document.querySelector('.options-container');
        if (existingOptions) {
            existingOptions.remove();
        }

        const questions = faqCategories[category];
        questions.forEach(faq => {
            const questionElement = document.createElement('div');
            questionElement.classList.add('faq-question');
            questionElement.textContent = faq.question;
            questionElement.addEventListener('click', function() {
                addMessage(faq.question, 'user-message');
                setTimeout(function() {
                    addMessage(faq.answer, 'bot-message');
                    setTimeout(() => {
                        addDynamicOptions([translateText('askAnotherQuestion'), translateText('joinChat')]);
                    }, 500);
                }, 500);
            });
            chatbotMessages.appendChild(questionElement);
        });

        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Add a new message (either from user or bot)
    function addMessage(text, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(className);
        messageElement.textContent = text;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Add dynamic buttons for user options
    function addDynamicOptions(options) {
        const optionsContainer = document.createElement('div');
        optionsContainer.classList.add('options-container');

        options.forEach(option => {
            const button = document.createElement('button');
            button.classList.add('option-button');
            button.textContent = option;
            button.addEventListener('click', function() {
                addMessage(option, 'user-message');
                setTimeout(() => {
                    handleOptionSelection(option);
                }, 500);
            });
            optionsContainer.appendChild(button);
        });

        chatbotMessages.appendChild(optionsContainer);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    async function joinChat() {
        const link = await getChatLink();  // Wait for the link to be fetched
        if (link) {
            window.location.href = link;  // Redirect to the fetched link
        } else {
            console.log('Failed to fetch the chat link.');
        }
    }

    async function getChatLink(){
        try {
            const response = await fetch('/api/v1/chat_bot/chat-link/', {
                method: 'GET', // or 'POST', 'PUT', etc. based on your needs
                headers: {
                  'Content-Type': 'application/json'// Example header
                }
              });
            if (!response.ok) {
                throw new Error('Chat link not found: ' + response.status);
            }
            const apiData = await response.json(); 
            const link = apiData[0]["link"];
            return link;
        } catch (error) {
            console.error('Hata:', error);
            // Hata mesajını kullanıcıya göster
        }
    }
    
    // Handle the selected option after dynamic options appear
    function handleOptionSelection(option) {
        switch(option) {
            case translateText('askAnotherQuestion'):
                showCategories();
                break;
            case translateText('frequentlyAskedQuestions'):
                showCategories();
                break;
            case translateText('joinChat'):
                joinChat();
                break;
            case translateText('endChat'):
                addMessage(translateText('endChat'), 'bot-message');
                break;
            case translateText('nextStep'):
                addMessage(translateText('nextStep'), 'bot-message');
                break;
            case translateText('learnMore'):
                addMessage(translateText('learnMore'), 'bot-message');
                break;
            case translateText('goBack'):
                addMessage(translateText('goBack'), 'bot-message');
                break;
            default:
                addMessage('You selected: ' + option, 'bot-message');
                break;
        }
    }

    // Dragging functionality for chatbot window
    chatbotHeader.addEventListener('mousedown', function(e) {
        isDragging = true;
        offsetX = e.clientX - chatbotWindow.offsetLeft;
        offsetY = e.clientY - chatbotWindow.offsetTop;
        document.addEventListener('mousemove', dragChatbot);
        document.addEventListener('mouseup', stopDragging);
    });

    function dragChatbot(e) {
        if (isDragging) {
            chatbotWindow.style.left = `${e.clientX - offsetX}px`;
            chatbotWindow.style.top = `${e.clientY - offsetY}px`;
        }
    }

    function stopDragging() {
        isDragging = false;
        document.removeEventListener('mousemove', dragChatbot);
        document.removeEventListener('mouseup', stopDragging);
    }

    // Fetch FAQ categories on page load
    getFaqCategories();
});
