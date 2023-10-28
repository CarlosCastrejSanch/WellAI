

function submutAnswers() {
    const tableBody = document.querySelector('table tbody');
    const numRows = tableBody.rows.length;
    console.log(numRows)
    let data = []
    for(var i=1; i<numRows+1; i++){
      questionAnswer = document.querySelector(`input[name="q${i}"]:checked`);
      if(questionAnswer){
      data.push({"answer":questionAnswer.value,"question_id":i,"choice_id":questionAnswer.id})
      }
    }
    console.log(data)
    fetch('/submit_answers', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('La respuesta de la red no ha sido correcta');
      }
      return response.json();
    })
    .then(data => {

        var submitMessageModal = document.getElementById("submitMessageModal");
        submitMessageModal.style.display = "block";
        var span = document.getElementById("closeMessageModal");
        span.onclick = function() {
            submitMessageModal.style.display = "none";

            var radioButtons = document.querySelectorAll('input[type="radio"]');
            for (var i = 0; i < radioButtons.length; i++) {
              radioButtons[i].checked = false;
            }


        }

        window.onclick = function(event) {
         
            if (event.target == submitMessageModal) {
                submitMessageModal.style.display = "none";
                var radioButtons = document.querySelectorAll('input[type="radio"]');
                for (var i = 0; i < radioButtons.length; i++) {
                  radioButtons[i].checked = false;
                }
                

            }
          }

        console.log(data.message);


        submitbtn =  document.getElementById('submitBTN');
        submitbtn.innerHTML = `<h1 style="color: brown;">Solo puedes responder un cuestionario por semana </h1>`;


    })
    .catch(error => {
      console.error('Ha habido un error procesando los datos:', error);
    });
  }