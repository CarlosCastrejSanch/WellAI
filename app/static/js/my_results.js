

const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('gpt4');


async function sendText() {


    $.ajax({
        type: 'POST',
        url: `/send_gpt`,
        data: { gpt4: userInput.value },
        success: function (response) {
            // Update the line chart with the filtered data
            var data = response;

            const message = data;
            const words = message.split(' ');
            words.forEach((word, index) => {
                setTimeout(() => {
                    const span = document.createElement('span');
                    span.textContent = word + ' ';
                    span.classList.add('paragraph');
                    chatContainer.appendChild(span);
                }, index * 250);
            });



        },
        error: function (error) {
            console.log(error);
        }
    });




}